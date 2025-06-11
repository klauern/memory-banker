import os
from pathlib import Path
from typing import Optional

import click
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

from .agents import MemoryBankAgents
from .memory_bank import MemoryBank


class MemoryBankerCLI:
    def __init__(self, project_path: Path, model: str, api_key: Optional[str] = None, timeout: int = 300):
        self.project_path = project_path
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError("API key must be provided via --api-key or OPENAI_API_KEY environment variable")
        
        self.llm_model = LitellmModel(model=self.model, api_key=self.api_key)
        self.memory_bank = MemoryBank(self.project_path)
        self.agents = MemoryBankAgents(self.llm_model, timeout=self.timeout)
        
    async def init(self):
        """Initialize a new memory bank"""
        click.echo(f"🚀 Initializing memory bank for project at: {self.project_path}")
        
        # Create memory-bank directory
        memory_bank_path = self.memory_bank.create_directory()
        click.echo(f"📁 Created memory bank directory: {memory_bank_path}")
        
        # Analyze the project
        click.echo("🔍 Analyzing project structure...")
        click.echo(f"⏱️  Using {self.timeout}s timeout per agent...")
        analysis = await self.agents.analyze_project(self.project_path)
        
        # Generate memory bank files
        click.echo("📝 Generating memory bank files...")
        await self.memory_bank.create_files(analysis)
        
        click.echo("✅ Memory bank initialized successfully!")
        click.echo(f"📄 Files created in: {memory_bank_path}")
        
    async def update(self):
        """Update existing memory bank files"""
        click.echo(f"🔄 Updating memory bank for project at: {self.project_path}")
        
        if not self.memory_bank.exists():
            click.echo("❌ No existing memory bank found. Use 'init' command first.")
            return
        
        # Re-analyze project and update files
        click.echo("🔍 Re-analyzing project...")
        analysis = await self.agents.analyze_project(self.project_path)
        
        click.echo("📝 Updating memory bank files...")
        await self.memory_bank.update_files(analysis)
        
        click.echo("✅ Memory bank updated successfully!")
        
    async def refresh(self):
        """Completely refresh the memory bank"""
        click.echo(f"🔄 Refreshing memory bank for project at: {self.project_path}")
        
        if self.memory_bank.exists():
            click.echo("🗑️  Removing existing memory bank...")
            self.memory_bank.remove()
        
        # Reinitialize
        await self.init()