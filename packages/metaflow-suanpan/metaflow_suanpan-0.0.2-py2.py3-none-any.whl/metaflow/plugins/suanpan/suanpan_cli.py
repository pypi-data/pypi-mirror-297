import base64
import json
import platform
import re
import sys
from hashlib import sha1

from metaflow import JSONType, Run, current, decorators, parameters
from metaflow._vendor import click
from metaflow.client.core import get_metadata
from metaflow.exception import (
    MetaflowException,
    MetaflowInternalError,
    MetaflowNotFound,
)
from metaflow.metaflow_config import (
    ARGO_WORKFLOWS_UI_URL,
    KUBERNETES_NAMESPACE,
    SERVICE_VERSION_CHECK,
    UI_URL,
)
from metaflow.package import MetaflowPackage

# TODO: Move production_token to utils
from metaflow.plugins.aws.step_functions.production_token import (
    load_token,
    new_token,
    store_token,
)
from metaflow.plugins.environment_decorator import EnvironmentDecorator
from metaflow.plugins.kubernetes.kubernetes_decorator import KubernetesDecorator
from metaflow.tagging_util import validate_tags
from metaflow.util import get_username, to_bytes, to_unicode, version_parse

from .suanpan import Suanpanflows

VALID_NAME = re.compile(r"^[a-z0-9]([a-z0-9\.\-]*[a-z0-9])?$")

unsupported_decorators = {
    "snowpark": "Step *%s* is marked for execution on Snowpark with Argo Workflows which isn't currently supported.",
    "slurm": "Step *%s* is marked for execution on Slurm with Argo Workflows which isn't currently supported.",
    "nvidia": "Step *%s* is marked for execution on Nvidia with Argo Workflows which isn't currently supported.",
}


class IncorrectProductionToken(MetaflowException):
    headline = "Incorrect production token"


class RunIdMismatch(MetaflowException):
    headline = "Run ID mismatch"


class IncorrectMetadataServiceVersion(MetaflowException):
    headline = "Incorrect version for metaflow service"


class ArgoWorkflowsNameTooLong(MetaflowException):
    headline = "Argo Workflows name too long"


class UnsupportedPythonVersion(MetaflowException):
    headline = "Unsupported version of Python"


@click.group()
def cli():
    pass


@cli.group(help="Commands related to suanpan.")
@click.option(
    "--name",
    default=None,
    type=str,
    help="Argo Workflow name. The flow name is used instead if "
    "this option is not specified.",
)
@click.pass_obj
def suanpan(obj, name=None):
    obj.check(obj.graph, obj.flow, obj.environment, pylint=obj.pylint)
    (
        obj.workflow_name,
        obj.token_prefix,
        obj.is_project,
    ) = resolve_workflow_name(obj, name)


@suanpan.command(help="Deploy a new version of this workflow to Argo Workflows.")
@click.pass_obj
def create(
    obj,
):
    for node in obj.graph:
        for decorator, error_message in unsupported_decorators.items():
            if any([d.name == decorator for d in node.decorators]):
                raise MetaflowException(error_message % node.name)

    obj.echo("Deploying *%s* to Suanpan Workflows..." % obj.workflow_name, bold=True)

    flow = make_flow(
        obj,
        obj.workflow_name,
    )

    print(flow.to_json())
    with open('graph.json', 'w', encoding='utf-8') as f:
        json.dump(flow.to_json(), f, ensure_ascii=False)

    # obj.echo_always(str(flow), err=False, no_bold=True)


def resolve_workflow_name(obj, name):
    project = current.get("project_name")
    obj._is_workflow_name_modified = False
    if project:
        if name:
            raise MetaflowException(
                "--name is not supported for @projects. Use --branch instead."
            )
        workflow_name = current.project_flow_name
        project_branch = to_bytes(".".join((project, current.branch_name)))
        token_prefix = (
            "mfprj-%s"
            % to_unicode(base64.b32encode(sha1(project_branch).digest()))[:16]
        )
        is_project = True
        # Argo Workflow names can't be longer than 253 characters, so we truncate
        # by default. Also, while project and branch allow for underscores, Argo
        # Workflows doesn't (DNS Subdomain names as defined in RFC 1123) - so we will
        # remove any underscores as well as convert the name to lower case.
        # Also remove + and @ as not allowed characters, which can be part of the
        # project branch due to using email addresses as user names.
        if len(workflow_name) > 253:
            name_hash = to_unicode(
                base64.b32encode(sha1(to_bytes(workflow_name)).digest())
            )[:8].lower()
            workflow_name = "%s-%s" % (workflow_name[:242], name_hash)
            obj._is_workflow_name_modified = True
        if not VALID_NAME.search(workflow_name):
            workflow_name = sanitize_for_argo(workflow_name)
            obj._is_workflow_name_modified = True
    else:
        if name and not VALID_NAME.search(name):
            raise MetaflowException(
                "Name '%s' contains invalid characters. The "
                "name must consist of lower case alphanumeric characters, '-' or '.'"
                ", and must start and end with an alphanumeric character." % name
            )

        workflow_name = name if name else current.flow_name
        token_prefix = workflow_name
        is_project = False

        if len(workflow_name) > 253:
            msg = (
                "The full name of the workflow:\n*%s*\nis longer than 253 "
                "characters.\n\n"
                "To deploy this workflow to Argo Workflows, please "
                "assign a shorter name\nusing the option\n"
                "*argo-workflows --name <name> create*." % workflow_name
            )
            raise ArgoWorkflowsNameTooLong(msg)

        if not VALID_NAME.search(workflow_name):
            workflow_name = sanitize_for_argo(workflow_name)
            obj._is_workflow_name_modified = True

    return workflow_name, token_prefix.lower(), is_project


def make_flow(
    obj,
    name,
):

    decorators._init_step_decorators(
        obj.flow, obj.graph, obj.environment, obj.flow_datastore, obj.logger
    )

    # Save the code package in the flow datastore so that both user code and
    # metaflow package can be retrieved during workflow execution.
    obj.package = MetaflowPackage(
        obj.flow, obj.environment, obj.echo, obj.package_suffixes
    )
    package_url, package_sha = obj.flow_datastore.save_data(
        [obj.package.blob], len_hint=1
    )[0]

    return Suanpanflows(
        name,
        obj.graph,
        obj.flow,
        package_sha,
        package_url,
        obj.metadata,
        obj.flow_datastore,
        obj.environment,
        obj.event_logger,
        obj.monitor,
    )


def sanitize_for_argo(text):
    """
    Sanitizes a string so it does not contain characters that are not permitted in Argo Workflow resource names.
    """
    return (
        re.compile(r"^[^A-Za-z0-9]+")
        .sub("", text)
        .replace("_", "")
        .replace("@", "")
        .replace("+", "")
        .lower()
    )
