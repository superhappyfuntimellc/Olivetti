# Olivetti Quick Start Guide

Get started with Olivetti in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/superhappyfuntimellc/Olivetti.git
cd Olivetti

# Install
pip install -e .
```

## Setup Your API Key

Choose your preferred AI provider:

### Option 1: OpenAI (GPT-4)
```bash
export OPENAI_API_KEY="your-key-here"
```

### Option 2: Anthropic (Claude)
```bash
export ANTHROPIC_API_KEY="your-key-here"
olivetti config --set api_provider=anthropic
olivetti config --set model=claude-3-5-sonnet-20241022
```

### Option 3: Ollama (Local, Free)
```bash
# Install Ollama from https://ollama.ai
# Pull a model: ollama pull llama2
olivetti config --set api_provider=ollama
olivetti config --set model=llama2
```

## Create Your Voice Profile

```bash
# Create a profile
olivetti profile create my-novel \
  --style "literary fiction, atmospheric prose" \
  --genre "mystery"

# Add a writing sample
cat << 'EOF' > sample.txt
The rain drummed against the windows of the old bookshop, each drop a tiny
percussion in the evening's symphony. Margaret traced her finger along the
spine of a leather-bound volume, feeling the decades embedded in its texture.
EOF

olivetti profile add-sample my-novel --file sample.txt

# Set as default
olivetti config --set default_voice_profile=my-novel
```

## Try It Out!

### Continue Writing
```bash
echo "The detective entered the dimly lit room." | olivetti continue
```

### Rewrite More Dramatically
```bash
echo "She opened the door." | olivetti rewrite --instruction "more suspenseful"
```

### Describe a Scene
```bash
olivetti describe "an abandoned Victorian mansion at twilight"
```

### Brainstorm Plot Ideas
```bash
olivetti brainstorm "unexpected ways to reveal the killer's identity" --count 5
```

### Generate Dialogue
```bash
olivetti dialogue \
  --characters "Detective Sara, Witness John" \
  --situation "questioning about the night of the murder"
```

## Working with Files

```bash
# Continue your chapter
olivetti continue --file chapter3.txt --length long > continuation.txt

# Analyze your writing
olivetti analyze --file my-draft.txt

# Rewrite a scene
olivetti rewrite --file scene.txt --instruction "tighten pacing" > scene-revised.txt
```

## Tips for Best Results

1. **Add Multiple Writing Samples**: The more samples you add to your voice profile, the better Olivetti understands your style.

2. **Be Specific**: When describing or brainstorming, provide clear context for better results.

3. **Experiment with Temperature**: Lower temperature (0.5-0.7) for more consistent output, higher (0.8-1.0) for more creative variations.
   ```bash
   olivetti config --set temperature=0.7
   ```

4. **Use Longer Contexts**: For continuing writing, provide at least a paragraph for better continuity.

5. **Profile Different Projects**: Create separate profiles for different genres or projects:
   ```bash
   olivetti profile create sci-fi-novel --genre "science fiction"
   olivetti profile create mystery-series --genre "mystery"
   ```

## Integration with Your Workflow

### Use in Vim/Neovim
```vim
" Continue writing from current paragraph
:r !olivetti continue --file %

" Rewrite selection (in visual mode)
:'<,'>!olivetti rewrite --instruction "more concise"
```

### Use with tmux
```bash
# Keep olivetti ready in a split pane
tmux split-window -h 'bash'
# Then pipe your writing to olivetti commands
```

### Batch Processing
```bash
# Process multiple chapters
for file in chapters/*.txt; do
  olivetti analyze --file "$file" > "analysis/$(basename $file .txt)-analysis.txt"
done
```

## Next Steps

- Read the full [README.md](README.md) for all features
- Check out [examples/example_usage.py](examples/example_usage.py) for Python API usage
- Explore different AI models to find what works best for your style
- Regularly update your voice profile with your best writing

## Troubleshooting

**Q: "AI engine not initialized" error?**  
A: Make sure your API key is set correctly:
```bash
# Check current config
olivetti config --list

# Set API key
export OPENAI_API_KEY="your-key"
# or
olivetti config --set api_key=your-key
```

**Q: Output doesn't match my style?**  
A: Add more writing samples to your voice profile:
```bash
olivetti profile add-sample my-profile --file my-best-work.txt
```

**Q: How do I switch between projects?**  
A: Use different profiles:
```bash
olivetti continue --profile project-a --file text.txt
olivetti continue --profile project-b --file text.txt
```

Happy writing! 📝✨
