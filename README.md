# Olivetti

**Bigger, Better, Faster, Stronger** - Your personal, highly intelligent AI writing assistant for professional novelists.

Olivetti is an advanced AI-powered writing assistant that learns and adapts to your unique voice and style. Unlike generic writing tools, Olivetti is designed specifically for novelists who want intelligent assistance that matches their personal writing style.

## Features

🎭 **Voice Profile System** - Train Olivetti with your writing samples to match your unique style  
✍️ **Smart Writing Commands** - Continue, rewrite, describe, brainstorm, and more  
🔄 **Multiple AI Providers** - Support for OpenAI, Anthropic Claude, and local Ollama models  
⚡ **Fast & Efficient** - Command-line interface for quick integration into your workflow  
🎨 **Style-Aware** - Maintains consistency with your voice, genre, and preferences  

## Installation

```bash
# Clone the repository
git clone https://github.com/superhappyfuntimellc/Olivetti.git
cd Olivetti

# Install dependencies
pip install -r requirements.txt

# Install Olivetti
pip install -e .
```

## Quick Start

### 1. Configure Your API Key

```bash
# For OpenAI (default)
export OPENAI_API_KEY="your-api-key-here"

# Or for Anthropic Claude
export ANTHROPIC_API_KEY="your-api-key-here"
olivetti config --set api_provider=anthropic
olivetti config --set model=claude-3-5-sonnet-20241022
```

### 2. Create Your Voice Profile

```bash
# Create a new voice profile
olivetti profile create my-voice \
  --style "literary fiction, introspective, lyrical prose" \
  --genre "contemporary fiction" \
  --genre "magical realism"

# Add writing samples to train your voice
olivetti profile add-sample my-voice --file my-novel-excerpt.txt \
  --description "Chapter 3 from my latest novel"

# Set as default
olivetti config --set default_voice_profile=my-voice
```

### 3. Start Writing!

```bash
# Continue writing from where you left off
echo "The old house stood at the edge of the forest, silent and watching." | \
  olivetti continue --length medium

# Rewrite a passage to be more dramatic
echo "She walked into the room." | \
  olivetti rewrite --instruction "more dramatic and tense"

# Describe a character or setting
olivetti describe "a mysterious stranger in a Victorian-era tavern" --detail extensive

# Brainstorm plot ideas
olivetti brainstorm "unexpected plot twists for a heist novel" --count 10

# Generate dialogue
olivetti dialogue \
  --characters "Detective Sarah, Suspect Mike" \
  --situation "Sarah confronts Mike about the missing evidence" \
  --length medium

# Analyze your writing
olivetti analyze --file chapter-draft.txt
```

## Command Reference

### Writing Commands

- `olivetti continue` - Continue writing from provided text
- `olivetti rewrite` - Rewrite text with optional instructions
- `olivetti describe` - Generate vivid descriptions
- `olivetti brainstorm` - Generate creative ideas
- `olivetti dialogue` - Generate character dialogue
- `olivetti analyze` - Analyze writing style and quality

### Voice Profile Commands

- `olivetti profile create <name>` - Create a new voice profile
- `olivetti profile list` - List all voice profiles
- `olivetti profile delete <name>` - Delete a voice profile
- `olivetti profile add-sample <name>` - Add writing sample to profile

### Configuration Commands

- `olivetti config --list` - Show current configuration
- `olivetti config --set key=value` - Set a configuration value
- `olivetti config --get key` - Get a configuration value

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `api_provider` | `openai` | AI provider (openai, anthropic, ollama) |
| `model` | `gpt-4` | Model to use |
| `temperature` | `0.8` | Creativity level (0.0-1.0) |
| `max_tokens` | `2000` | Maximum response length |
| `default_voice_profile` | `None` | Default voice profile name |

## Python API

You can also use Olivetti programmatically:

```python
from olivetti import WritingAssistant, VoiceProfile

# Create and configure a voice profile
profile = VoiceProfile("my-voice")
profile.set_style_notes("literary fiction, introspective")
profile.add_writing_sample("Your writing sample here...", "Novel excerpt")
profile.save()

# Use the assistant
assistant = WritingAssistant(voice_profile="my-voice")

# Continue writing
continuation = assistant.continue_writing(
    "The old house stood at the edge of the forest...",
    length="medium"
)

# Rewrite text
rewritten = assistant.rewrite(
    "She walked into the room.",
    instruction="more dramatic"
)

# Describe something
description = assistant.describe(
    "a mysterious stranger",
    detail_level="detailed"
)

# Brainstorm ideas
ideas = assistant.brainstorm("plot twists", count=10)

# Generate dialogue
dialogue = assistant.dialogue(
    characters=["Alice", "Bob"],
    situation="confronting a secret",
    length="medium"
)
```

## Why Olivetti?

Named after the iconic Olivetti typewriters that powered countless novelists, this tool brings that same reliability and craftsmanship to the AI age. Just as Olivetti typewriters were known for their quality and design, Olivetti the AI assistant is designed to be:

- **Personal** - Learns YOUR voice, not generic writing
- **Intelligent** - Understands context, genre, and style
- **Professional** - Built for serious novelists and authors
- **Reliable** - Consistent quality with every generation
- **Flexible** - Works with multiple AI providers and models

## Requirements

- Python 3.8+
- OpenAI API key, Anthropic API key, or local Ollama installation

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ for novelists who want AI assistance that truly understands their craft.
