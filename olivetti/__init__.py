"""
Olivetti - A personal, highly intelligent AI writing assistant for professional novelists.

Bigger, better, faster, stronger than Sudowrite My Voice.
"""

__version__ = "0.1.0"
__author__ = "Olivetti Team"

from .assistant import WritingAssistant
from .voice_profile import VoiceProfile

__all__ = ["WritingAssistant", "VoiceProfile"]
