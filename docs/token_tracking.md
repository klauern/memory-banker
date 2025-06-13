# Token Usage Tracking

Memory Banker now includes comprehensive token usage tracking and cost calculation features to help you monitor and optimize your LLM usage costs.

## Features

### 🔍 Real-time Token Tracking
- Tracks token usage for each individual agent execution
- Captures prompt tokens, completion tokens, and total tokens
- Records execution timing and success/failure status
- Automatically saves detailed reports after each run

### 💰 Cost Calculation
- Built-in pricing for popular models (GPT-4o, GPT-4o-mini, Claude-3, etc.)
- Automatic cost calculation based on token usage
- Support for custom pricing configurations
- Cost comparison across different models

### 📊 Detailed Reporting
- Per-agent token usage breakdown
- Session-level aggregation and statistics
- Historical report storage and retrieval
- Rich CLI output with formatted reports

## Usage

### Automatic Tracking

Token tracking is automatically enabled for all Memory Banker operations. After running any command (`init`, `update`, `refresh`), you'll see a detailed token usage report:

```bash
memory-banker init

# ... project analysis output ...

============================================================
📊 TOKEN USAGE REPORT  
============================================================
Model: gpt-4o-mini
Total Duration: 45.2s
Successful Agents: 6/6

📝 Total Prompt Tokens: 12,450
💬 Total Completion Tokens: 8,320
🔢 Total Tokens: 20,770
💰 Estimated Cost: $0.0531 USD

🤖 Per-Agent Breakdown:
  ✅ projectbrief     | Tokens:  3,245 | Duration:   7.2s
  ✅ productContext   | Tokens:  3,890 | Duration:   8.1s  
  ✅ systemPatterns   | Tokens:  4,120 | Duration:   9.3s
  ✅ techContext      | Tokens:  3,780 | Duration:   8.8s
  ✅ activeContext    | Tokens:  3,110 | Duration:   6.9s
  ✅ progress         | Tokens:  2,625 | Duration:   5.9s
============================================================
```

### Viewing Historical Reports

Use the `tokens` command to view saved token usage reports:

```bash
# View the most recent report
memory-banker tokens

# List all available reports
memory-banker tokens --list-all

# View a specific report file
memory-banker tokens --report-file memory-bank/token-reports/token_usage_20241206_143022.json
```

### Report Storage

Token usage reports are automatically saved to:
```
<project-path>/memory-bank/token-reports/token_usage_<timestamp>.json
```

Each report includes:
- Session metadata (timestamp, model, command)
- Per-agent execution details
- Token usage statistics
- Cost calculations
- Success/failure status for each agent

## Cost Calculation

### Supported Models

Memory Banker includes built-in pricing for popular models:

| Model | Prompt (per 1K tokens) | Completion (per 1K tokens) |
|-------|------------------------|----------------------------|
| gpt-4o | $0.0025 | $0.01 |
| gpt-4o-mini | $0.00015 | $0.0006 |
| gpt-4 | $0.03 | $0.06 |
| gpt-3.5-turbo | $0.0015 | $0.002 |
| claude-3-haiku | $0.00025 | $0.00125 |
| claude-3-sonnet | $0.003 | $0.015 |
| claude-3-opus | $0.015 | $0.075 |

### Custom Pricing

You can provide custom pricing configurations programmatically:

```python
from memory_banker.token_tracking import TokenUsageReport

custom_pricing = {
    "my-custom-model": {
        "prompt_per_1k": 0.001,
        "completion_per_1k": 0.002
    }
}

report = TokenUsageReport.load_from_file("report.json")
cost = report.calculate_cost(custom_pricing)
```

## Report Format

Token usage reports are saved as JSON files with the following structure:

```json
{
  "session_id": "uuid-string",
  "project_path": "/path/to/project",
  "model": "gpt-4o-mini",
  "command": "init",
  "start_time": "2024-12-06T14:30:22",
  "end_time": "2024-12-06T14:31:07",
  "total_duration_seconds": 45.2,
  "total_prompt_tokens": 12450,
  "total_completion_tokens": 8320,
  "total_tokens": 20770,
  "total_cost_usd": 0.0531,
  "successful_agents": 6,
  "failed_agents": 0,
  "agent_usage": [
    {
      "agent_name": "projectbrief",
      "prompt_tokens": 1820,
      "completion_tokens": 1425,
      "total_tokens": 3245,
      "model": "gpt-4o-mini",
      "start_time": "2024-12-06T14:30:22",
      "end_time": "2024-12-06T14:30:29",
      "duration_seconds": 7.2,
      "success": true,
      "error": null
    }
    // ... more agents
  ]
}
```

## Integration with CI/CD

Token reports can be integrated into CI/CD pipelines for cost monitoring:

```bash
#!/bin/bash
# Generate memory bank and capture cost
memory-banker init > output.log 2>&1

# Extract cost from the latest report
COST=$(memory-banker tokens --report-file $(ls -t memory-bank/token-reports/*.json | head -1) | grep "Estimated Cost" | grep -o '\$[0-9.]*')

echo "Memory bank generation cost: $COST"

# Set cost threshold (e.g., $1.00)
if [ $(echo "$COST > 1.00" | bc) -eq 1 ]; then
  echo "⚠️ Cost exceeds threshold!"
  exit 1
fi
```

## Performance Optimization

Use token reports to optimize your usage:

1. **Identify Expensive Agents**: Review per-agent costs to find optimization opportunities
2. **Model Selection**: Compare costs across different models for your specific use case
3. **Timeout Optimization**: Balance timeout settings with cost considerations
4. **Parallel vs Sequential**: Understand the cost impact of different execution strategies

## Troubleshooting

### Missing Token Data

If token usage shows as 0, this may be due to:
- Model provider not returning usage data
- Custom model configurations
- Network timeouts or errors

### Cost Calculation Issues

- Ensure your model name matches supported models
- Check for model name variations (e.g., "gpt-4o" vs "gpt-4o-2024-05-13")
- Provide custom pricing for unsupported models

### Report Access Issues

- Check file permissions on the `memory-bank/token-reports/` directory
- Ensure sufficient disk space for report storage
- Verify the project path is correct when using `--project-path`