import rich_click as click

import api
import cli.ui as ui
from config import Config

DEMO_CLIENT_ID = 17
DEMO_CLIENT_NAME = "demo"
DEMO_CLIENT_USER = "demo@ackee.xyz"


@click.command("config")
@click.pass_context
def config(ctx):
    config: Config = ctx.obj.get("config")
    project_api: api.ProjectApi = ctx.obj.get("project_api")

    active_client = config.get_active_client()
    active_project = config.get_active_project()

    if not active_client or not active_project or not project_api:
        ui.error(f"Configuration not complete, please use INIT command first")
        return

    project = {}
    with ui.spinner("Checking current configuration"):
        project = project_api.get_project(active_project)

    ui.config(
        app=config.get_active().get("client"),
        client=active_client.get("user"),
        project=project.get("name"),
        project_id=project.get("id"),
    )
