import asyncio
import os
from pathlib import Path

import click
from agents.extensions.models.litellm_model import LitellmModel
from rich.console import Console

from .agents import MemoryBankAgents
from .memory_bank import MemoryBank
from .progress import create_simple_tracker


class MemoryBankerCLI:
    def __init__(
        self,
        project_path: Path,
        model: str,
        api_key: str | None = None,
        api_base: str | None = None,
        timeout: int = 300,
    ):
        self.project_path = project_path
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE")
        self.timeout = timeout
        self.console = Console()

        if not self.api_key:
            raise ValueError(
                "API key must be provided via --api-key or OPENAI_API_KEY environment variable"
            )

        # Enable LiteLLM debugging
        os.environ["LITELLM_LOG"] = "DEBUG"

        # Warn about custom API base (tracing disabled in main() function)
        if self.api_base:
            self.console.print(
                f"⚠️  Custom API base detected: {self.api_base}", style="yellow"
            )
            self.console.print(
                "📡 OpenAI Agents tracing disabled to prevent data leakage", style="dim"
            )

        self.llm_model = LitellmModel(
            model=self.model, api_key=self.api_key, base_url=self.api_base
        )
        self.memory_bank = MemoryBank(self.project_path)
        self.agents = MemoryBankAgents(self.llm_model, timeout=self.timeout)

    async def init(self):
        """Initialize a new memory bank"""
        self.console.print(
            f"🚀 Initializing memory bank for project at: {self.project_path}",
            style="bold blue",
        )

        # Create memory-bank directory
        with create_simple_tracker(self.console).track_operation(
            "Creating memory bank directory"
        ):
            memory_bank_path = self.memory_bank.create_directory()

        self.console.print(
            f"📁 Created memory bank directory: {memory_bank_path}", style="green"
        )

        # Analyze the project
        self.console.print("🔍 Starting project analysis...", style="bold")
        self.console.print(f"⏱️  Using {self.timeout}s timeout per agent", style="dim")

        analysis = await self.agents.analyze_project(self.project_path, command="init")

        # Generate memory bank files
        with create_simple_tracker(self.console).track_operation(
            "Writing memory bank files", total=len(analysis)
        ) as tracker:
            await self.memory_bank.create_files(analysis, tracker)

        # Generate and display token usage report
        token_report = self.agents.get_token_usage_report()
        if token_report:
            self._display_token_usage_report(token_report)
            # Save token usage report
            report_file = self.agents.save_token_usage_report(self.project_path)
            if report_file:
                self.console.print(
                    f"📊 Token usage saved to: {report_file}", style="dim"
                )

        self.console.print(
            "✅ Memory bank initialized successfully!", style="bold green"
        )
        self.console.print(f"📄 Files created in: {memory_bank_path}", style="dim")

    async def update(self):
        """Update existing memory bank files"""
        self.console.print(
            f"🔄 Updating memory bank for project at: {self.project_path}",
            style="bold blue",
        )

        if not self.memory_bank.exists():
            self.console.print(
                "❌ No existing memory bank found. Use 'init' command first.",
                style="red",
            )
            return

        # Re-analyze project and update files
        self.console.print("🔍 Re-analyzing project...", style="bold")
        analysis = await self.agents.analyze_project(
            self.project_path, command="update"
        )

        with create_simple_tracker(self.console).track_operation(
            "Updating memory bank files", total=len(analysis)
        ) as tracker:
            await self.memory_bank.update_files(analysis, tracker)

        # Generate and display token usage report
        token_report = self.agents.get_token_usage_report()
        if token_report:
            self._display_token_usage_report(token_report)
            # Save token usage report
            report_file = self.agents.save_token_usage_report(self.project_path)
            if report_file:
                self.console.print(
                    f"📊 Token usage saved to: {report_file}", style="dim"
                )

        self.console.print("✅ Memory bank updated successfully!", style="bold green")

    async def refresh(self):
        """Completely refresh the memory bank"""
        self.console.print(
            f"🔄 Refreshing memory bank for project at: {self.project_path}",
            style="bold blue",
        )

        if self.memory_bank.exists():
            with create_simple_tracker(self.console).track_operation(
                "Removing existing memory bank"
            ):
                self.memory_bank.remove()

        self.console.print("🗑️  Existing memory bank removed", style="yellow")

        # Reinitialize
        await self.init()

    def _display_token_usage_report(self, report):
        """Display token usage report in a formatted way"""
        self.console.print("\n" + "=" * 60, style="blue")
        self.console.print("📊 TOKEN USAGE REPORT", style="bold blue")
        self.console.print("=" * 60, style="blue")

        # Summary
        self.console.print(f"Model: {report.model}", style="cyan")
        self.console.print(
            f"Total Duration: {report.total_duration_seconds:.1f}s", style="cyan"
        )
        self.console.print(
            f"Successful Agents: {report.successful_agents}/{len(report.agent_usage)}",
            style="green" if report.failed_agents == 0 else "yellow",
        )

        # Token totals
        self.console.print(
            f"\n📝 Total Prompt Tokens: {report.total_prompt_tokens:,}", style="white"
        )
        self.console.print(
            f"💬 Total Completion Tokens: {report.total_completion_tokens:,}",
            style="white",
        )
        self.console.print(
            f"🔢 Total Tokens: {report.total_tokens:,}", style="bold white"
        )

        # Cost
        if report.total_cost_usd > 0:
            self.console.print(
                f"💰 Estimated Cost: ${report.total_cost_usd:.4f} USD",
                style="bold green",
            )
        else:
            self.console.print("💰 Cost calculation not available", style="dim")

        # Per-agent breakdown
        if report.agent_usage:
            self.console.print("\n🤖 Per-Agent Breakdown:", style="bold")
            for usage in report.agent_usage:
                status_emoji = "✅" if usage.success else "❌"
                duration = (
                    f"{usage.duration_seconds:.1f}s"
                    if usage.duration_seconds > 0
                    else "N/A"
                )
                self.console.print(
                    f"  {status_emoji} {usage.agent_name:<16} | "
                    f"Tokens: {usage.total_tokens:>6,} | "
                    f"Duration: {duration:>6}",
                    style="white" if usage.success else "red",
                )
                if not usage.success and usage.error:
                    self.console.print(f"     Error: {usage.error}", style="red dim")

        self.console.print("=" * 60 + "\n", style="blue")


@click.group()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path.cwd(),
    help="Path to project directory (default: current directory)",
)
@click.option(
    "--model", default="gpt-4.1-mini", help="LLM model to use (default: gpt-4.1-mini)"
)
@click.option(
    "--api-key",
    envvar="OPENAI_API_KEY",
    help="API key for the model (will use OPENAI_API_KEY env var if not provided)",
)
@click.option(
    "--api-base",
    envvar="OPENAI_API_BASE",
    help="Base URL for the API (will use OPENAI_API_BASE env var if not provided)",
)
@click.option(
    "--timeout",
    type=int,
    default=300,
    help="Timeout in seconds for agent processing (default: 300)",
)
@click.pass_context
def cli(
    ctx,
    project_path: Path,
    model: str,
    api_key: str | None,
    api_base: str | None,
    timeout: int,
):
    """Memory Banker - Agentically create Cline-style memory banks

    Commands:
      init     Initialize a new memory bank
      update   Update existing memory bank files
      refresh  Completely refresh/rebuild the memory bank
      tokens   View token usage reports and costs
    """
    ctx.ensure_object(dict)
    # Store parameters in context, don't instantiate CLI until needed
    ctx.obj["project_path"] = project_path
    ctx.obj["model"] = model
    ctx.obj["api_key"] = api_key
    ctx.obj["api_base"] = api_base
    ctx.obj["timeout"] = timeout


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize a new memory bank for the project"""
    cli_instance = MemoryBankerCLI(
        project_path=ctx.obj["project_path"],
        model=ctx.obj["model"],
        api_key=ctx.obj["api_key"],
        api_base=ctx.obj["api_base"],
        timeout=ctx.obj["timeout"],
    )
    asyncio.run(cli_instance.init())


@cli.command()
@click.pass_context
def update(ctx):
    """Update existing memory bank files"""
    cli_instance = MemoryBankerCLI(
        project_path=ctx.obj["project_path"],
        model=ctx.obj["model"],
        api_key=ctx.obj["api_key"],
        api_base=ctx.obj["api_base"],
        timeout=ctx.obj["timeout"],
    )
    asyncio.run(cli_instance.update())


@cli.command()
@click.pass_context
def refresh(ctx):
    """Completely refresh/rebuild the memory bank"""
    cli_instance = MemoryBankerCLI(
        project_path=ctx.obj["project_path"],
        model=ctx.obj["model"],
        api_key=ctx.obj["api_key"],
        api_base=ctx.obj["api_base"],
        timeout=ctx.obj["timeout"],
    )
    asyncio.run(cli_instance.refresh())


@cli.command()
@click.option(
    "--list-all", "-l", is_flag=True, help="List all available token usage reports"
)
@click.option(
    "--report-file",
    "-f",
    type=click.Path(exists=True, path_type=Path),
    help="Specific report file to display",
)
@click.pass_context
def tokens(ctx, list_all: bool, report_file: Path):
    """View token usage reports and costs"""
    from .token_tracking import TokenUsageReport

    project_path = ctx.obj["project_path"]
    console = Console()

    if report_file:
        # Display specific report file
        try:
            report = TokenUsageReport.load_from_file(report_file)
            cli_instance = MemoryBankerCLI(
                project_path=project_path,
                model=ctx.obj["model"],
                api_key=ctx.obj["api_key"] or "dummy",  # Just for display, no API calls
                api_base=ctx.obj["api_base"],
                timeout=ctx.obj["timeout"],
            )
            cli_instance._display_token_usage_report(report)
        except Exception as e:
            console.print(f"❌ Error loading report: {e}", style="red")
        return

    # Find and display available reports
    reports_dir = project_path / "memory-bank" / "token-reports"

    if not reports_dir.exists():
        console.print("📊 No token usage reports found.", style="yellow")
        console.print(f"Reports are saved to: {reports_dir}", style="dim")
        return

    report_files = list(reports_dir.glob("*.json"))

    if not report_files:
        console.print(
            "📊 No token usage reports found in reports directory.", style="yellow"
        )
        return

    if list_all:
        # List all available reports
        console.print(
            f"📊 Available Token Usage Reports ({len(report_files)} found):",
            style="bold blue",
        )
        console.print(f"Directory: {reports_dir}", style="dim")
        console.print()

        for report_file in sorted(
            report_files, key=lambda f: f.stat().st_mtime, reverse=True
        ):
            try:
                report = TokenUsageReport.load_from_file(report_file)
                console.print(f"📄 {report_file.name}", style="cyan")
                console.print(
                    f"   Command: {report.command} | "
                    f"Model: {report.model} | "
                    f"Tokens: {report.total_tokens:,} | "
                    f"Cost: ${report.total_cost_usd:.4f} | "
                    f"Date: {report.start_time.strftime('%Y-%m-%d %H:%M')}",
                    style="white",
                )
            except Exception as e:
                console.print(
                    f"   ❌ Error reading {report_file.name}: {e}", style="red dim"
                )

        console.print(
            "\nTo view a specific report: memory-banker tokens -f <report-file>",
            style="dim",
        )
    else:
        # Display the most recent report
        latest_report = max(report_files, key=lambda f: f.stat().st_mtime)
        console.print(
            f"📊 Displaying latest token usage report: {latest_report.name}",
            style="cyan",
        )

        try:
            report = TokenUsageReport.load_from_file(latest_report)
            cli_instance = MemoryBankerCLI(
                project_path=project_path,
                model=ctx.obj["model"],
                api_key=ctx.obj["api_key"] or "dummy",  # Just for display, no API calls
                api_base=ctx.obj["api_base"],
                timeout=ctx.obj["timeout"],
            )
            cli_instance._display_token_usage_report(report)
        except Exception as e:
            console.print(f"❌ Error loading latest report: {e}", style="red")


def main():
    """Entry point for the memory-banker CLI tool"""

    # Check if custom API base is being used and disable tracing preemptively
    # This must be done before any openai-agents imports
    api_base = os.getenv("OPENAI_API_BASE")
    if api_base:
        os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"

    cli()
