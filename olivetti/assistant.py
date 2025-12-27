"""Core writing assistant with AI-powered features."""

from typing import Optional, List
from pathlib import Path

from .config import Config
from .voice_profile import VoiceProfile
from .ai_engine import create_engine, AIEngine


class WritingAssistant:
    """AI-powered writing assistant for novelists."""
    
    def __init__(self, config_dir: Optional[Path] = None, voice_profile: Optional[str] = None):
        """Initialize writing assistant.
        
        Args:
            config_dir: Configuration directory (defaults to ~/.olivetti)
            voice_profile: Name of voice profile to use
        """
        self.config = Config(config_dir)
        
        # Load voice profile
        if voice_profile:
            self.voice_profile = VoiceProfile(voice_profile, config_dir)
        elif self.config.get("default_voice_profile"):
            self.voice_profile = VoiceProfile(
                self.config.get("default_voice_profile"), 
                config_dir
            )
        else:
            self.voice_profile = None
        
        # Initialize AI engine
        self.engine: Optional[AIEngine] = None
        self._init_engine()
    
    def _init_engine(self) -> None:
        """Initialize AI engine based on configuration."""
        provider = self.config.get("api_provider", "openai")
        api_key = self.config.get_api_key()
        model = self.config.get("model")
        
        if provider in ["openai", "anthropic"] and not api_key:
            # Don't raise error yet, will raise when trying to generate
            return
        
        try:
            self.engine = create_engine(provider, api_key, model)
        except Exception as e:
            print(f"Warning: Failed to initialize AI engine: {e}")
    
    def _build_prompt(self, instruction: str, context: str = "") -> str:
        """Build prompt with voice profile context.
        
        Args:
            instruction: The main instruction/request
            context: Additional context to include
            
        Returns:
            Complete prompt string
        """
        parts = []
        
        # Add voice profile context if available
        if self.voice_profile:
            voice_context = self.voice_profile.get_context_for_ai()
            if voice_context:
                parts.append("=== Writer's Voice Profile ===")
                parts.append(voice_context)
                parts.append("\n=== Task ===")
        
        # Add context if provided
        if context:
            parts.append(f"Context:\n{context}\n")
        
        # Add instruction
        parts.append(instruction)
        
        return "\n".join(parts)
    
    def continue_writing(self, text: str, length: str = "medium") -> str:
        """Continue writing from given text.
        
        Args:
            text: The text to continue from
            length: Length of continuation (short, medium, long)
            
        Returns:
            Generated continuation
        """
        if not self.engine:
            raise RuntimeError("AI engine not initialized. Please configure API key.")
        
        length_tokens = {
            "short": 200,
            "medium": 500,
            "long": 1000,
        }
        
        max_tokens = length_tokens.get(length, 500)
        
        instruction = f"""Continue this narrative naturally, maintaining the same voice, style, and tone. 
Write approximately {length} length continuation.

Text to continue:
{text}

Continue:"""
        
        prompt = self._build_prompt(instruction)
        
        temperature = self.config.get("temperature", 0.8)
        return self.engine.generate(prompt, max_tokens, temperature)
    
    def rewrite(self, text: str, instruction: str = "") -> str:
        """Rewrite text with optional instruction.
        
        Args:
            text: Text to rewrite
            instruction: How to rewrite (e.g., "more dramatic", "simpler")
            
        Returns:
            Rewritten text
        """
        if not self.engine:
            raise RuntimeError("AI engine not initialized. Please configure API key.")
        
        base_instruction = "Rewrite the following text"
        if instruction:
            base_instruction += f" to be {instruction}"
        base_instruction += ", maintaining the writer's voice and style."
        
        full_instruction = f"""{base_instruction}

Original text:
{text}

Rewritten version:"""
        
        prompt = self._build_prompt(full_instruction)
        
        temperature = self.config.get("temperature", 0.8)
        max_tokens = self.config.get("max_tokens", 2000)
        return self.engine.generate(prompt, max_tokens, temperature)
    
    def describe(self, subject: str, detail_level: str = "detailed") -> str:
        """Generate description of a subject.
        
        Args:
            subject: What to describe (character, setting, object, etc.)
            detail_level: Level of detail (brief, detailed, extensive)
            
        Returns:
            Generated description
        """
        if not self.engine:
            raise RuntimeError("AI engine not initialized. Please configure API key.")
        
        instruction = f"""Write a {detail_level} description of: {subject}

Make it vivid, engaging, and suitable for a novel. Match the writer's style and voice.

Description:"""
        
        prompt = self._build_prompt(instruction)
        
        temperature = self.config.get("temperature", 0.8)
        max_tokens = self.config.get("max_tokens", 2000)
        return self.engine.generate(prompt, max_tokens, temperature)
    
    def brainstorm(self, topic: str, count: int = 5) -> str:
        """Generate ideas about a topic.
        
        Args:
            topic: Topic to brainstorm about
            count: Number of ideas to generate
            
        Returns:
            Generated ideas
        """
        if not self.engine:
            raise RuntimeError("AI engine not initialized. Please configure API key.")
        
        instruction = f"""Brainstorm {count} creative ideas for: {topic}

Generate diverse, interesting ideas that could work well in the writer's style and genres.

Ideas:"""
        
        prompt = self._build_prompt(instruction)
        
        temperature = self.config.get("temperature", 0.9)  # Higher for creativity
        max_tokens = self.config.get("max_tokens", 2000)
        return self.engine.generate(prompt, max_tokens, temperature)
    
    def dialogue(self, characters: List[str], situation: str, length: str = "medium") -> str:
        """Generate dialogue between characters.
        
        Args:
            characters: List of character names
            situation: The situation/context for dialogue
            length: Length of dialogue (short, medium, long)
            
        Returns:
            Generated dialogue
        """
        if not self.engine:
            raise RuntimeError("AI engine not initialized. Please configure API key.")
        
        length_tokens = {
            "short": 300,
            "medium": 600,
            "long": 1200,
        }
        
        max_tokens = length_tokens.get(length, 600)
        
        char_list = ", ".join(characters)
        
        instruction = f"""Write a {length} dialogue scene between: {char_list}

Situation: {situation}

Make the dialogue natural, character-driven, and match the writer's style. Include necessary action beats and description.

Dialogue:"""
        
        prompt = self._build_prompt(instruction)
        
        temperature = self.config.get("temperature", 0.85)
        return self.engine.generate(prompt, max_tokens, temperature)
    
    def analyze(self, text: str) -> str:
        """Analyze text for style, pacing, and other elements.
        
        Args:
            text: Text to analyze
            
        Returns:
            Analysis results
        """
        if not self.engine:
            raise RuntimeError("AI engine not initialized. Please configure API key.")
        
        instruction = f"""Analyze the following text for:
- Writing style and voice
- Pacing and rhythm
- Strengths and areas for improvement
- Consistency with the writer's established voice (if applicable)

Text to analyze:
{text}

Analysis:"""
        
        prompt = self._build_prompt(instruction)
        
        temperature = 0.5  # Lower for analytical tasks
        max_tokens = self.config.get("max_tokens", 2000)
        return self.engine.generate(prompt, max_tokens, temperature)
