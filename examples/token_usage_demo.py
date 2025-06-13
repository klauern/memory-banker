#!/usr/bin/env python3
"""
Demonstration of the Memory Banker token usage tracking feature.

This script shows how to use the new token tracking and cost calculation features.
"""

import uuid
from pathlib import Path

from memory_banker.token_tracking import TokenTracker, TokenUsageReport


def demo_token_tracking():
    """Demonstrate token tracking functionality"""
    print("🔍 Memory Banker Token Usage Tracking Demo")
    print("=" * 50)

    # Create a sample token tracker
    tracker = TokenTracker(
        session_id=str(uuid.uuid4()),
        project_path="/example/project",
        model="gpt-4o-mini",
        command="demo",
    )

    # Simulate agent executions
    agents = [
        ("projectbrief", 1200, 800),
        ("productContext", 1500, 1200),
        ("systemPatterns", 1800, 1000),
        ("techContext", 1600, 900),
        ("activeContext", 1400, 750),
        ("progress", 1000, 600),
    ]

    print("\n📊 Simulating agent executions...")

    for agent_name, prompt_tokens, completion_tokens in agents:
        print(f"  🤖 Running {agent_name}...")

        # Start tracking
        usage = tracker.start_agent(agent_name)

        # Simulate some processing time
        import time

        time.sleep(0.1)

        # Simulate result with token usage
        class MockResult:
            def __init__(self, prompt_tokens, completion_tokens):
                self.usage = MockUsage(prompt_tokens, completion_tokens)

        class MockUsage:
            def __init__(self, prompt_tokens, completion_tokens):
                self.prompt_tokens = prompt_tokens
                self.completion_tokens = completion_tokens
                self.total_tokens = prompt_tokens + completion_tokens

        result = MockResult(prompt_tokens, completion_tokens)

        # Finish tracking
        tracker.finish_agent(usage, result)

    # Finish session and get report
    report = tracker.finish_session()

    # Display results
    print("\n" + "=" * 60)
    print("📊 TOKEN USAGE REPORT")
    print("=" * 60)

    print(f"Model: {report.model}")
    print(f"Command: {report.command}")
    print(f"Duration: {report.total_duration_seconds:.1f}s")
    print(f"Successful Agents: {report.successful_agents}/{len(report.agent_usage)}")

    print(f"\n📝 Total Prompt Tokens: {report.total_prompt_tokens:,}")
    print(f"💬 Total Completion Tokens: {report.total_completion_tokens:,}")
    print(f"🔢 Total Tokens: {report.total_tokens:,}")
    print(f"💰 Estimated Cost: ${report.total_cost_usd:.4f} USD")

    print("\n🤖 Per-Agent Breakdown:")
    for usage in report.agent_usage:
        status_emoji = "✅" if usage.success else "❌"
        duration = (
            f"{usage.duration_seconds:.1f}s" if usage.duration_seconds > 0 else "N/A"
        )
        print(
            f"  {status_emoji} {usage.agent_name:<16} | "
            f"Tokens: {usage.total_tokens:>6,} | "
            f"Duration: {duration:>6}"
        )

    print("=" * 60)

    # Show cost breakdown for different models
    print("\n💰 Cost Comparison Across Models:")
    models_to_test = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4",
        "claude-3-sonnet",
        "claude-3-haiku",
    ]

    for model in models_to_test:
        test_report = TokenUsageReport(
            session_id=report.session_id,
            project_path=report.project_path,
            model=model,
            command=report.command,
            start_time=report.start_time,
            end_time=report.end_time,
            agent_usage=report.agent_usage.copy(),
        )
        cost = test_report.calculate_cost()
        print(f"  {model:<20} | ${cost:.4f} USD")

    # Save demo report
    demo_dir = Path(__file__).parent / "demo_reports"
    report_file = tracker.save_report(demo_dir, "demo_token_usage.json")
    print(f"\n📄 Demo report saved to: {report_file}")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_token_tracking()
