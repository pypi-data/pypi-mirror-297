from typing import Annotated, Any

import toml
import typer
from beaupy import confirm, prompt, select
from typer_config import conf_callback_factory
from typer_config.decorators import use_config
from typer_config.loaders import toml_loader

from trainwave_cli.api import Api
from trainwave_cli.config.config import config
from trainwave_cli.utils import async_command, ensure_api_key

app = typer.Typer()


def pyproject_loader(param_value: str) -> dict[str, Any]:
    if not param_value:  # set a default path to read from
        param_value = "trainwave.toml"
    try:
        pyproject = toml_loader(param_value)
    except FileNotFoundError:
        return {}
    return pyproject


pyproject_callback = conf_callback_factory(pyproject_loader)


_CREATE_NEW_PROJECT_OPTION = "( Create a new project )"


async def _run_setup_guide(
    existing_org: str,
    existing_project: str,
) -> dict[str, str | int] | None:
    typer.echo("Running setup\n")

    api_client = Api(config.api_key, config.endpoint)

    # Step 1: Select an organization that user is part of
    organizations = await api_client.list_organizations()
    if not organizations:
        typer.echo("You are not part of any organization.\n")
        typer.echo("Please visit the Trainwave web app to create an organization.\n")
        return

    formatted_org_selection = [f"{org.name}" for org in organizations]

    typer.echo("1. Select which organization to use.\n")
    select_org = select(formatted_org_selection)

    selected_org = next(org for org in organizations if org.name == select_org)

    # Step 2: Select or create a project to use

    projects = await api_client.list_projects(selected_org.id)
    project_options = [f"{project.name}" for project in projects]
    project_options.append(_CREATE_NEW_PROJECT_OPTION)

    typer.echo("2. Select which project to use.\n")
    typer.echo(
        "A project groups together all the jobs you run and allows you to enforce spending limits and default configurations for all jobs run in the project.\n"
    )

    selected_project = select(project_options)

    if selected_project == _CREATE_NEW_PROJECT_OPTION:
        project_name = prompt("Enter the name of the new project")
        project = await api_client.create_project(selected_org.id, project_name)
    else:
        project = next(
            project for project in projects if project.name == selected_project
        )

    typer.echo("Give your job a name. Example: 'Training a LLM'\n")

    name = prompt("Enter the name of the job")

    # TODO: Ask for GPU type and count
    # SETUP COMMAND and RUN COMMAND
    return {
        "organization": selected_org.rid,
        "project": project.rid,
        "name": name,
    }


@app.callback(invoke_without_command=True)
@async_command
@use_config(pyproject_callback)
@ensure_api_key
async def default(
    organization: Annotated[str, typer.Option()] = "",
    project: Annotated[str, typer.Option()] = "",
    name: Annotated[str, typer.Option()] = "",
) -> None:
    # Stuff is not set
    if not organization:
        typer.echo("No config file found.\n")

        if confirm(
            "Would you like to create a new Trainwave configuration (trainwave.toml)?"
        ):
            new_config = await _run_setup_guide(organization, project, name)

            typer.echo(new_config)

            with open("trainwave.toml", "w") as f:
                toml.dump(new_config, f)

    # Ask user if they want to switch org or project
    else:
        pass
