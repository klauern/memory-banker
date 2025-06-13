"""Interactive progress display for Memory Banker operations"""

import threading
import time
from contextlib import contextmanager
from typing import Any

from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text


class AgentProgressTracker:
    """Tracks progress of multiple agents with live terminal updates"""

    def __init__(self):
        self.console = Console()
        self.agents: dict[str, dict[str, Any]] = {}
        self.live: Live | None = None
        self.start_time = None
        self._timer: threading.Timer | None = None

    def add_agent(self, agent_name: str, description: str):
        """Add an agent to track"""
        self.agents[agent_name] = {
            "description": description,
            "status": "pending",
            "start_time": None,
            "end_time": None,
            "details": "",
            "error": None,
        }
        # Refresh display if live to show new agent immediately
        self.refresh()

    def start_agent(self, agent_name: str, details: str = ""):
        """Mark an agent as started"""
        if agent_name in self.agents:
            self.agents[agent_name]["status"] = "running"
            self.agents[agent_name]["start_time"] = time.time()
            self.agents[agent_name]["details"] = details
            self.refresh()

    def update_agent(self, agent_name: str, details: str):
        """Update agent details/status"""
        if agent_name in self.agents:
            self.agents[agent_name]["details"] = details
            self.refresh()

    def complete_agent(self, agent_name: str, success: bool = True, error: str = None):
        """Mark an agent as completed"""
        if agent_name in self.agents:
            self.agents[agent_name]["status"] = "completed" if success else "failed"
            self.agents[agent_name]["end_time"] = time.time()
            if error:
                self.agents[agent_name]["error"] = error
            self.refresh()

    def _create_display(self) -> Panel:
        """Create the live display layout"""
        # Create main table
        table = Table(
            title="🤖 Memory Bank Agent Progress",
            show_header=True,
            header_style="bold magenta",
            border_style="blue",
            expand=True,
        )

        table.add_column(
            "Agent", style="cyan", no_wrap=True, min_width=15, max_width=20
        )
        table.add_column(
            "Status", style="bold", no_wrap=True, min_width=12, max_width=15
        )
        table.add_column("Description", style="white", min_width=35, max_width=45)
        table.add_column("Details", style="dim white", min_width=25, max_width=35)
        table.add_column("Time", style="green", no_wrap=True, min_width=8, max_width=12)

        for agent_name, info in self.agents.items():
            # Status with emoji
            if info["status"] == "pending":
                status = Text("⏳ Pending", style="yellow")
            elif info["status"] == "running":
                status = Text("🔄 Running", style="blue bold")
            elif info["status"] == "completed":
                status = Text("✅ Done", style="green bold")
            else:  # failed
                status = Text("❌ Failed", style="red bold")

            # Calculate time
            if info["start_time"]:
                if info["end_time"]:
                    duration = info["end_time"] - info["start_time"]
                else:
                    duration = time.time() - info["start_time"]
                time_str = f"{duration:.1f}s"
            else:
                time_str = "-"

            # Details with error handling
            details = info["details"]
            if info["error"]:
                details = f"Error: {info['error'][:30]}..."
            elif len(details) > 32:
                details = details[:29] + "..."

            table.add_row(agent_name, status, info["description"], details, time_str)

        # Add summary stats
        total_agents = len(self.agents)
        completed = sum(
            1 for info in self.agents.values() if info["status"] == "completed"
        )
        running = sum(1 for info in self.agents.values() if info["status"] == "running")
        failed = sum(1 for info in self.agents.values() if info["status"] == "failed")

        if self.start_time:
            total_time = time.time() - self.start_time
            time_info = f"Total time: {total_time:.1f}s"
        else:
            time_info = "Starting..."

        summary = f"Progress: {completed}/{total_agents} completed"
        if failed > 0:
            summary += f" ({failed} failed)"
        if running > 0:
            summary += f" ({running} running)"

        footer = Columns(
            [
                Align.left(Text(summary, style="bold")),
                Align.right(Text(time_info, style="dim")),
            ]
        )

        # Create a container with table and footer properly structured
        from rich.console import Group

        content = Group(table, footer)

        return Panel(
            content,
            title="Memory Banker Status",
            border_style="bright_blue",
        )

    @contextmanager
    def live_display(self):
        """Context manager for live display"""
        self.start_time = time.time()
        # Create the Live object with initial display
        live = Live(
            self._create_display(),
            refresh_per_second=10,  # High refresh rate for responsiveness
            console=self.console,
            transient=False,
        )

        with live:
            self.live = live
            # Show initial display immediately
            self.refresh()
            # Give a brief moment for the display to render
            time.sleep(0.1)
            # Start timer for regular time updates
            self._start_timer()
            try:
                yield self
            finally:
                # Stop timer
                self._stop_timer()
                self.live = None

    def refresh(self):
        """Manually refresh the display"""
        if self.live:
            self.live.update(self._create_display())

    def _start_timer(self):
        """Start timer for regular time updates"""

        def timer_refresh():
            if self.live:
                self.refresh()
                # Schedule next refresh
                self._timer = threading.Timer(1.0, timer_refresh)
                self._timer.start()

        self._timer = threading.Timer(1.0, timer_refresh)
        self._timer.start()

    def _stop_timer(self):
        """Stop the timer"""
        if self._timer:
            self._timer.cancel()
            self._timer = None


class SimpleProgressTracker:
    """Simple progress tracker for basic operations"""

    def __init__(self, console: Console | None = None):
        self.console = console or Console()
        self.progress = None
        self.task_id = None

    @contextmanager
    def track_operation(self, description: str, total: int = None):
        """Track a simple operation with spinner or progress bar"""
        if total:
            # Use progress bar for operations with known total
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console,
                transient=True,
            ) as progress:
                task_id = progress.add_task(description, total=total)
                self.progress = progress
                self.task_id = task_id
                try:
                    yield self
                finally:
                    self.progress = None
                    self.task_id = None
        else:
            # Use simple spinner for operations without known total
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=True,
            ) as progress:
                task_id = progress.add_task(description)
                self.progress = progress
                self.task_id = task_id
                try:
                    yield self
                finally:
                    self.progress = None
                    self.task_id = None

    def update(self, advance: int = 1, description: str = None):
        """Update progress"""
        if self.progress and self.task_id is not None:
            if description:
                self.progress.update(self.task_id, description=description)
            self.progress.advance(self.task_id, advance)


# Convenience functions for common use cases
def create_agent_tracker() -> AgentProgressTracker:
    """Create a new agent progress tracker"""
    return AgentProgressTracker()


def create_simple_tracker(console: Console | None = None) -> SimpleProgressTracker:
    """Create a simple progress tracker"""
    return SimpleProgressTracker(console)
