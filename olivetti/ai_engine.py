"""AI engine for text generation with support for multiple providers."""

import os
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod


class AIEngine(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate text from prompt."""
        pass


class OpenAIEngine(AIEngine):
    """OpenAI API engine."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize OpenAI engine.
        
        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-4)
        """
        self.api_key = api_key
        self.model = model
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError(
                "openai package not installed. Install with: pip install openai"
            )
    
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.8) -> str:
        """Generate text using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")


class AnthropicEngine(AIEngine):
    """Anthropic Claude API engine."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize Anthropic engine.
        
        Args:
            api_key: Anthropic API key
            model: Model name
        """
        self.api_key = api_key
        self.model = model
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Install with: pip install anthropic"
            )
    
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.8) -> str:
        """Generate text using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")


class OllamaEngine(AIEngine):
    """Ollama local model engine."""
    
    def __init__(self, model: str = "llama2", host: str = "http://localhost:11434"):
        """Initialize Ollama engine.
        
        Args:
            model: Model name
            host: Ollama server URL
        """
        self.model = model
        self.host = host
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError(
                "requests package not installed. Install with: pip install requests"
            )
    
    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.8) -> str:
        """Generate text using Ollama API."""
        try:
            response = self.requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    }
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {str(e)}")


def create_engine(provider: str, api_key: Optional[str] = None, model: Optional[str] = None) -> AIEngine:
    """Factory function to create AI engine.
    
    Args:
        provider: Provider name (openai, anthropic, ollama)
        api_key: API key (required for openai and anthropic)
        model: Model name (optional)
        
    Returns:
        AIEngine instance
    """
    if provider == "openai":
        if not api_key:
            raise ValueError("API key required for OpenAI")
        return OpenAIEngine(api_key, model or "gpt-4")
    
    elif provider == "anthropic":
        if not api_key:
            raise ValueError("API key required for Anthropic")
        return AnthropicEngine(api_key, model or "claude-3-5-sonnet-20241022")
    
    elif provider == "ollama":
        return OllamaEngine(model or "llama2")
    
    else:
        raise ValueError(f"Unknown provider: {provider}. Supported: openai, anthropic, ollama")
