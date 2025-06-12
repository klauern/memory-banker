import shutil
from pathlib import Path
from typing import Any


class MemoryBank:
    """Manages the memory bank directory and files"""

    MEMORY_BANK_FILES = [
        "projectbrief.md",
        "productContext.md",
        "activeContext.md",
        "systemPatterns.md",
        "techContext.md",
        "progress.md",
    ]

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.memory_bank_path = project_path / "memory-bank"

    def exists(self) -> bool:
        """Check if memory bank directory exists"""
        return self.memory_bank_path.exists()

    def create_directory(self) -> Path:
        """Create the memory bank directory"""
        self.memory_bank_path.mkdir(exist_ok=True)
        return self.memory_bank_path

    def remove(self):
        """Remove the entire memory bank directory"""
        if self.memory_bank_path.exists():
            shutil.rmtree(self.memory_bank_path)

    async def create_files(self, analysis: dict[str, Any]):
        """Create all memory bank files based on agent analysis"""
        file_mapping = {
            "projectbrief": "projectbrief.md",
            "productContext": "productContext.md",
            "activeContext": "activeContext.md",
            "systemPatterns": "systemPatterns.md",
            "techContext": "techContext.md",
            "progress": "progress.md",
        }

        for analysis_key, filename in file_mapping.items():
            if analysis_key in analysis:
                file_path = self.memory_bank_path / filename
                content = analysis[analysis_key]
                file_path.write_text(content, encoding="utf-8")

    async def update_files(self, analysis: dict[str, Any]):
        """Update existing memory bank files"""
        # For now, just recreate all files
        # In the future, we could be smarter about preserving manual edits
        await self.create_files(analysis)
