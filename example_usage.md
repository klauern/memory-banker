# Memory Banker Subset Agent Usage Examples

The Memory Banker now supports running only a subset of agents to speed up analysis and reduce API costs for testing.

## Basic Usage

### Run all agents (default behavior)

```bash
memory-banker init
```

### Run specific agents only

```bash
# Run only project brief and tech context agents
memory-banker init --agents projectbrief --agents techContext

# Run just the essential agents for quick analysis
memory-banker init --agents projectbrief --agents activeContext --agents progress

# Update only specific agents
memory-banker update --agents activeContext --agents progress
```

## Available Agents

The following agents are available:

1. **projectbrief** - Foundation document defining project scope
2. **productContext** - Why the project exists and problem context
3. **activeContext** - Current development state and next steps
4. **systemPatterns** - Architecture and design patterns
5. **techContext** - Technical setup and dependencies
6. **progress** - What works, what's left, project status
7. **aiGuidelines** - AI assistant best practices for the project

## Performance Benefits

### Integration Testing

Instead of running all 7 agents (which can take 15-35 minutes with API calls), tests now run subsets:

- **Quick validation**: `--agents projectbrief --agents techContext` (2-4 minutes)
- **Status check**: `--agents activeContext --agents progress` (2-4 minutes)
- **Full analysis**: No `--agents` flag (15-35 minutes, unchanged)

### Development Workflow

```bash
# Quick project understanding
memory-banker init --agents projectbrief --agents techContext

# Check current status
memory-banker update --agents activeContext --agents progress

# Full comprehensive analysis when needed
memory-banker refresh
```

This dramatically improves the development and testing experience while maintaining full functionality when needed.
