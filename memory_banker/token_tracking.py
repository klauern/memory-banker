"""Token usage tracking for Memory Banker agents"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class AgentTokenUsage:
    """Token usage for a single agent execution"""

    agent_name: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    start_time: datetime | None = None
    end_time: datetime | None = None
    success: bool = True
    error: str | None = None

    @property
    def duration_seconds(self) -> float:
        """Calculate execution duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "agent_name": self.agent_name,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "model": self.model,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "success": self.success,
            "error": self.error,
        }


@dataclass
class TokenUsageReport:
    """Complete token usage report for a memory bank generation session"""

    session_id: str
    project_path: str
    model: str
    command: str  # init, update, refresh
    start_time: datetime
    end_time: datetime | None = None
    agent_usage: list[AgentTokenUsage] = field(default_factory=list)
    total_cost_usd: float = 0.0

    @property
    def total_prompt_tokens(self) -> int:
        """Sum of all prompt tokens across agents"""
        return sum(usage.prompt_tokens for usage in self.agent_usage)

    @property
    def total_completion_tokens(self) -> int:
        """Sum of all completion tokens across agents"""
        return sum(usage.completion_tokens for usage in self.agent_usage)

    @property
    def total_tokens(self) -> int:
        """Sum of all tokens across agents"""
        return sum(usage.total_tokens for usage in self.agent_usage)

    @property
    def successful_agents(self) -> int:
        """Count of successfully completed agents"""
        return sum(1 for usage in self.agent_usage if usage.success)

    @property
    def failed_agents(self) -> int:
        """Count of failed agents"""
        return sum(1 for usage in self.agent_usage if not usage.success)

    @property
    def total_duration_seconds(self) -> float:
        """Total session duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    def add_agent_usage(self, usage: AgentTokenUsage):
        """Add agent usage to the report"""
        self.agent_usage.append(usage)

    def calculate_cost(self, pricing_config: dict[str, dict[str, float]] | None = None):
        """Calculate total cost based on token usage and pricing config"""
        if not pricing_config:
            pricing_config = self._get_default_pricing()

        total_cost = 0.0
        model_key = self._normalize_model_name(self.model)

        if model_key in pricing_config:
            prices = pricing_config[model_key]
            prompt_cost = (self.total_prompt_tokens / 1000) * prices.get(
                "prompt_per_1k", 0
            )
            completion_cost = (self.total_completion_tokens / 1000) * prices.get(
                "completion_per_1k", 0
            )
            total_cost = prompt_cost + completion_cost

        self.total_cost_usd = total_cost
        return total_cost

    def _normalize_model_name(self, model: str) -> str:
        """Normalize model name for pricing lookup"""
        # Handle common model name variations
        model_lower = model.lower()
        if "gpt-4o" in model_lower:
            return "gpt-4o"
        elif "gpt-4" in model_lower and "mini" in model_lower:
            return "gpt-4o-mini"
        elif "gpt-4" in model_lower:
            return "gpt-4"
        elif "gpt-3.5" in model_lower:
            return "gpt-3.5-turbo"
        elif "claude-3" in model_lower and "haiku" in model_lower:
            return "claude-3-haiku"
        elif "claude-3" in model_lower and "sonnet" in model_lower:
            return "claude-3-sonnet"
        elif "claude-3" in model_lower and "opus" in model_lower:
            return "claude-3-opus"
        return model_lower

    def _get_default_pricing(self) -> dict[str, dict[str, float]]:
        """Default pricing configuration (USD per 1K tokens)"""
        return {
            "gpt-4o": {"prompt_per_1k": 0.0025, "completion_per_1k": 0.01},
            "gpt-4o-mini": {"prompt_per_1k": 0.00015, "completion_per_1k": 0.0006},
            "gpt-4": {"prompt_per_1k": 0.03, "completion_per_1k": 0.06},
            "gpt-3.5-turbo": {"prompt_per_1k": 0.0015, "completion_per_1k": 0.002},
            "claude-3-haiku": {"prompt_per_1k": 0.00025, "completion_per_1k": 0.00125},
            "claude-3-sonnet": {"prompt_per_1k": 0.003, "completion_per_1k": 0.015},
            "claude-3-opus": {"prompt_per_1k": 0.015, "completion_per_1k": 0.075},
        }

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "session_id": self.session_id,
            "project_path": self.project_path,
            "model": self.model,
            "command": self.command,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_duration_seconds": self.total_duration_seconds,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost_usd,
            "successful_agents": self.successful_agents,
            "failed_agents": self.failed_agents,
            "agent_usage": [usage.to_dict() for usage in self.agent_usage],
        }

    def save_to_file(self, file_path: Path):
        """Save report to JSON file"""
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, file_path: Path) -> "TokenUsageReport":
        """Load report from JSON file"""
        with open(file_path) as f:
            data = json.load(f)

        report = cls(
            session_id=data["session_id"],
            project_path=data["project_path"],
            model=data["model"],
            command=data["command"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"])
            if data.get("end_time")
            else None,
            total_cost_usd=data.get("total_cost_usd", 0.0),
        )

        # Reconstruct agent usage
        for agent_data in data.get("agent_usage", []):
            usage = AgentTokenUsage(
                agent_name=agent_data["agent_name"],
                prompt_tokens=agent_data.get("prompt_tokens", 0),
                completion_tokens=agent_data.get("completion_tokens", 0),
                total_tokens=agent_data.get("total_tokens", 0),
                model=agent_data.get("model", ""),
                start_time=datetime.fromisoformat(agent_data["start_time"])
                if agent_data.get("start_time")
                else None,
                end_time=datetime.fromisoformat(agent_data["end_time"])
                if agent_data.get("end_time")
                else None,
                success=agent_data.get("success", True),
                error=agent_data.get("error"),
            )
            report.add_agent_usage(usage)

        return report


class TokenTracker:
    """Main token tracking class for managing usage across agent executions"""

    def __init__(self, session_id: str, project_path: str, model: str, command: str):
        self.report = TokenUsageReport(
            session_id=session_id,
            project_path=project_path,
            model=model,
            command=command,
            start_time=datetime.now(),
        )

    def start_agent(self, agent_name: str) -> AgentTokenUsage:
        """Start tracking an agent execution"""
        usage = AgentTokenUsage(
            agent_name=agent_name, model=self.report.model, start_time=datetime.now()
        )
        return usage

    def finish_agent(
        self, usage: AgentTokenUsage, result: Any = None, error: str | None = None
    ):
        """Finish tracking an agent execution"""
        usage.end_time = datetime.now()
        usage.success = error is None
        usage.error = error

        # Extract token usage from result if available
        if (
            result
            and hasattr(result, "context_wrapper")
            and hasattr(result.context_wrapper, "usage")
        ):
            # OpenAI Agents framework format
            agent_usage = result.context_wrapper.usage
            usage.prompt_tokens = getattr(agent_usage, "input_tokens", 0)
            usage.completion_tokens = getattr(agent_usage, "output_tokens", 0)
            usage.total_tokens = getattr(agent_usage, "total_tokens", 0)
        elif result and hasattr(result, "usage") and result.usage:
            # Direct usage format
            usage.prompt_tokens = getattr(result.usage, "prompt_tokens", 0)
            usage.completion_tokens = getattr(result.usage, "completion_tokens", 0)
            usage.total_tokens = getattr(result.usage, "total_tokens", 0)
        elif result and hasattr(result, "token_usage"):
            # Alternative token usage format
            token_usage = result.token_usage
            usage.prompt_tokens = getattr(token_usage, "prompt_tokens", 0)
            usage.completion_tokens = getattr(token_usage, "completion_tokens", 0)
            usage.total_tokens = getattr(token_usage, "total_tokens", 0)

        self.report.add_agent_usage(usage)

    def finish_session(
        self, pricing_config: dict[str, dict[str, float]] | None = None
    ) -> TokenUsageReport:
        """Finish the tracking session and calculate costs"""
        self.report.end_time = datetime.now()
        self.report.calculate_cost(pricing_config)
        return self.report

    def save_report(self, directory: Path, filename: str | None = None):
        """Save the token usage report to a file"""
        if not filename:
            timestamp = self.report.start_time.strftime("%Y%m%d_%H%M%S")
            filename = f"token_usage_{timestamp}.json"

        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / filename
        self.report.save_to_file(file_path)
        return file_path
