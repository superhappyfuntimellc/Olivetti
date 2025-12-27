"""Voice profile system for capturing and maintaining writer's style."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime


class VoiceProfile:
    """Represents a writer's unique voice and style."""
    
    def __init__(self, name: str, config_dir: Optional[Path] = None):
        """Initialize voice profile.
        
        Args:
            name: Name of the voice profile
            config_dir: Configuration directory (defaults to ~/.olivetti)
        """
        self.name = name
        
        if config_dir is None:
            config_dir = Path.home() / ".olivetti"
        
        self.profile_dir = config_dir / "voice_profiles"
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        
        self.profile_file = self.profile_dir / f"{name}.json"
        
        # Load or initialize profile data
        self.data = self._load_profile()
    
    def _load_profile(self) -> Dict[str, Any]:
        """Load profile from file or create new."""
        if self.profile_file.exists():
            with open(self.profile_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "name": self.name,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "writing_samples": [],
                "style_notes": "",
                "genre_preferences": [],
                "vocabulary_preferences": [],
                "sentence_structure_notes": "",
                "pacing_preferences": "",
                "character_voice_notes": "",
            }
    
    def save(self) -> None:
        """Save profile to file."""
        self.data["updated_at"] = datetime.now().isoformat()
        with open(self.profile_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_writing_sample(self, text: str, description: str = "") -> None:
        """Add a writing sample to learn from.
        
        Args:
            text: The writing sample text
            description: Optional description of the sample
        """
        sample = {
            "text": text,
            "description": description,
            "added_at": datetime.now().isoformat(),
        }
        self.data["writing_samples"].append(sample)
        self.save()
    
    def set_style_notes(self, notes: str) -> None:
        """Set general style notes."""
        self.data["style_notes"] = notes
        self.save()
    
    def add_genre_preference(self, genre: str) -> None:
        """Add a genre preference."""
        if genre not in self.data["genre_preferences"]:
            self.data["genre_preferences"].append(genre)
            self.save()
    
    def get_context_for_ai(self) -> str:
        """Generate context string for AI prompts."""
        context_parts = []
        
        if self.data.get("style_notes"):
            context_parts.append(f"Writing Style: {self.data['style_notes']}")
        
        if self.data.get("genre_preferences"):
            genres = ", ".join(self.data["genre_preferences"])
            context_parts.append(f"Preferred Genres: {genres}")
        
        if self.data.get("sentence_structure_notes"):
            context_parts.append(f"Sentence Structure: {self.data['sentence_structure_notes']}")
        
        if self.data.get("pacing_preferences"):
            context_parts.append(f"Pacing: {self.data['pacing_preferences']}")
        
        # Include recent writing samples
        samples = self.data.get("writing_samples", [])
        if samples:
            context_parts.append("\nWriting Samples:")
            for i, sample in enumerate(samples[-3:], 1):  # Last 3 samples
                context_parts.append(f"\nSample {i}:")
                if sample.get("description"):
                    context_parts.append(f"  ({sample['description']})")
                context_parts.append(f"  {sample['text'][:500]}...")  # First 500 chars
        
        return "\n".join(context_parts)
    
    @classmethod
    def list_profiles(cls, config_dir: Optional[Path] = None) -> List[str]:
        """List all available voice profiles.
        
        Args:
            config_dir: Configuration directory
            
        Returns:
            List of profile names
        """
        if config_dir is None:
            config_dir = Path.home() / ".olivetti"
        
        profile_dir = config_dir / "voice_profiles"
        
        if not profile_dir.exists():
            return []
        
        profiles = []
        for file in profile_dir.glob("*.json"):
            profiles.append(file.stem)
        
        return sorted(profiles)
    
    @classmethod
    def delete_profile(cls, name: str, config_dir: Optional[Path] = None) -> bool:
        """Delete a voice profile.
        
        Args:
            name: Name of profile to delete
            config_dir: Configuration directory
            
        Returns:
            True if deleted, False if not found
        """
        if config_dir is None:
            config_dir = Path.home() / ".olivetti"
        
        profile_file = config_dir / "voice_profiles" / f"{name}.json"
        
        if profile_file.exists():
            profile_file.unlink()
            return True
        
        return False
