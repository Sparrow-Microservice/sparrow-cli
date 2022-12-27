import typer
from pathlib import Path
from sparrow_cli.consoles import console
from sparrow_cli.templating.fetchers import TemplateFetcher
from sparrow_cli.templating.processors import TemplateProcessor
from sparrow_cli.api import app


@app.command("http")
def new_project(path: Path) -> None:
    """
    Create a new Sparrow http project.
    """
    console.print(":wrench: Creating new Project...\n")
    fetcher = TemplateFetcher.from_name("project-init")

    # console.print("fetcher: ", fetcher)
    processor = TemplateProcessor.from_fetcher(fetcher, path.absolute(), defaults={"project_name": path.name})
    processor.render()
