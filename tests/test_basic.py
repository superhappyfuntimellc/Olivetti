"""Basic tests for Olivetti."""

import pytest
import tempfile
import json
from pathlib import Path

from olivetti.config import Config
from olivetti.voice_profile import VoiceProfile


class TestConfig:
    """Test configuration management."""
    
    def test_config_creation(self):
        """Test creating a config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            assert config.config_dir.exists()
            assert config.config_file.exists()
    
    def test_config_get_set(self):
        """Test getting and setting config values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Config(Path(tmpdir))
            
            # Test default value
            assert config.get("api_provider") == "openai"
            
            # Test setting value
            config.set("api_provider", "anthropic")
            assert config.get("api_provider") == "anthropic"
            
            # Test custom value
            config.set("custom_key", "custom_value")
            assert config.get("custom_key") == "custom_value"


class TestVoiceProfile:
    """Test voice profile system."""
    
    def test_profile_creation(self):
        """Test creating a voice profile."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profile = VoiceProfile("test-profile", Path(tmpdir))
            assert profile.name == "test-profile"
            assert profile.data["name"] == "test-profile"
    
    def test_profile_save_load(self):
        """Test saving and loading profiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create and save profile
            profile1 = VoiceProfile("test-profile", Path(tmpdir))
            profile1.set_style_notes("Test style notes")
            profile1.save()
            
            # Load profile
            profile2 = VoiceProfile("test-profile", Path(tmpdir))
            assert profile2.data["style_notes"] == "Test style notes"
    
    def test_add_writing_sample(self):
        """Test adding writing samples."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profile = VoiceProfile("test-profile", Path(tmpdir))
            
            sample_text = "This is a test writing sample."
            profile.add_writing_sample(sample_text, "Test sample")
            
            assert len(profile.data["writing_samples"]) == 1
            assert profile.data["writing_samples"][0]["text"] == sample_text
    
    def test_add_genre_preference(self):
        """Test adding genre preferences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profile = VoiceProfile("test-profile", Path(tmpdir))
            
            profile.add_genre_preference("fantasy")
            profile.add_genre_preference("sci-fi")
            
            assert "fantasy" in profile.data["genre_preferences"]
            assert "sci-fi" in profile.data["genre_preferences"]
            assert len(profile.data["genre_preferences"]) == 2
    
    def test_get_context_for_ai(self):
        """Test generating AI context."""
        with tempfile.TemporaryDirectory() as tmpdir:
            profile = VoiceProfile("test-profile", Path(tmpdir))
            
            profile.set_style_notes("Literary fiction")
            profile.add_genre_preference("mystery")
            
            context = profile.get_context_for_ai()
            assert "Literary fiction" in context
            assert "mystery" in context
    
    def test_list_profiles(self):
        """Test listing profiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple profiles
            VoiceProfile("profile1", Path(tmpdir)).save()
            VoiceProfile("profile2", Path(tmpdir)).save()
            VoiceProfile("profile3", Path(tmpdir)).save()
            
            profiles = VoiceProfile.list_profiles(Path(tmpdir))
            assert len(profiles) == 3
            assert "profile1" in profiles
            assert "profile2" in profiles
            assert "profile3" in profiles
    
    def test_delete_profile(self):
        """Test deleting profiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create and delete profile
            VoiceProfile("test-profile", Path(tmpdir)).save()
            
            assert VoiceProfile.delete_profile("test-profile", Path(tmpdir))
            profiles = VoiceProfile.list_profiles(Path(tmpdir))
            assert "test-profile" not in profiles
            
            # Try deleting non-existent profile
            assert not VoiceProfile.delete_profile("non-existent", Path(tmpdir))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
