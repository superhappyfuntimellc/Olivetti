"""Configuration management for Olivetti."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """Manage configuration for Olivetti writing assistant."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration.
        
        Args:
            config_dir: Directory to store configuration files. 
                       Defaults to ~/.olivetti
        """
        if config_dir is None:
            config_dir = Path.home() / ".olivetti"
        
        self.config_dir = config_dir
        self.config_file = self.config_dir / "config.json"
        self.voice_profiles_dir = self.config_dir / "voice_profiles"
        
        # Create directories if they don't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.voice_profiles_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create config
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                "api_provider": "openai",  # openai, anthropic, ollama, etc.
                "model": "gpt-4",
                "temperature": 0.8,
                "max_tokens": 2000,
                "default_voice_profile": None,
            }
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
        self._save_config(self._config)
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from environment or config."""
        provider = self.get("api_provider", "openai")
        
        # Try environment variables first
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "together": "TOGETHER_API_KEY",
        }
        
        env_var = env_vars.get(provider, f"{provider.upper()}_API_KEY")
        api_key = os.environ.get(env_var)
        
        if api_key:
            return api_key
        
        # Fall back to config file
        return self._config.get("api_key")
    
    def set_api_key(self, api_key: str) -> None:
        """Set API key in config."""
        self.set("api_key", api_key)
