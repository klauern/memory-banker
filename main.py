import asyncio
from pathlib import Path
from typing import Optional

import click

from memory_banker.cli import MemoryBankerCLI


@click.group()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path.cwd(),
    help="Path to project directory (default: current directory)"
)
@click.option(
    "--model",
    default="gpt-4.1-mini",
    help="LLM model to use (default: gpt-4.1-mini)"
)
@click.option(
    "--api-key",
    envvar="OPENAI_API_KEY",
    help="API key for the model (will use OPENAI_API_KEY env var if not provided)"
)
@click.option(
    "--timeout",
    type=int,
    default=300,
    help="Timeout in seconds for agent processing (default: 300)"
)
@click.pass_context
def cli(ctx, project_path: Path, model: str, api_key: Optional[str], timeout: int):
    """Memory Banker - Agentically create Cline-style memory banks"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = MemoryBankerCLI(
        project_path=project_path,
        model=model,
        api_key=api_key,
        timeout=timeout
    )


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize a new memory bank for the project"""
    cli_instance = ctx.obj["cli"]
    asyncio.run(cli_instance.init())


@cli.command()
@click.pass_context
def update(ctx):
    """Update existing memory bank files"""
    cli_instance = ctx.obj["cli"]
    asyncio.run(cli_instance.update())


@cli.command()
@click.pass_context
def refresh(ctx):
    """Completely refresh/rebuild the memory bank"""
    cli_instance = ctx.obj["cli"]
    asyncio.run(cli_instance.refresh())


if __name__ == "__main__":
    cli()
