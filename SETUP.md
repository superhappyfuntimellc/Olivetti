# Olivetti Setup Guide

Welcome to Olivetti! This guide will help you set up the platform on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- An OpenAI API key (get one at https://platform.openai.com/api-keys)

## Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key for Web App

The web app needs a configuration file that is **NOT** in the repository (for security).

**Create the file manually:**

1. Create a new directory called `.streamlit` in the root of the repository:
   ```bash
   mkdir .streamlit
   ```

2. Create a file called `secrets.toml` inside `.streamlit`:
   ```bash
   # On Windows
   type nul > .streamlit\secrets.toml
   
   # On macOS/Linux
   touch .streamlit/secrets.toml
   ```

3. Open `.streamlit/secrets.toml` in your text editor and add:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-actual-key-here"
   ```

4. Replace `sk-proj-your-actual-key-here` with your real OpenAI API key

**Quick setup script (alternative):**

```bash
# Run this in the repository root
mkdir -p .streamlit
echo 'OPENAI_API_KEY = "sk-proj-your-key-here"' > .streamlit/secrets.toml
```

Then edit `.streamlit/secrets.toml` to add your actual key.

### Step 3: Configure API Key for CLI Tool (Optional)

If you want to use the command-line tool:

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   AI_PROVIDER=openai
   ```

3. Install the CLI package:
   ```bash
   pip install -e .
   ```

## Running Olivetti

### Web App

**Browser Mode:**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

**Desktop Mode (recommended):**
```bash
# Windows
launch_desktop.bat

# macOS/Linux
./launch_desktop.sh

# Or with Python
python desktop_launcher.py
```

For native desktop window (optional):
```bash
pip install pywebview>=4.0.0
```

### CLI Tool

After installing with `pip install -e .`:

```bash
# Create a voice profile
olivetti profile create novelist --style "literary fiction"

# Continue writing
echo "The story begins..." | olivetti continue --length long

# Other commands
olivetti rewrite --file draft.txt --instruction "increase tension"
olivetti dialogue --characters "Alice, Bob" --situation "confronting betrayal"
olivetti brainstorm --topic "plot twist ideas"
olivetti analyze --file manuscript.txt
```

## Troubleshooting

### "OPENAI_API_KEY is not set" error

This means the configuration file wasn't found. Make sure:

1. The file is named exactly `.streamlit/secrets.toml` (note the dot prefix)
2. It's in the root of the repository (same directory as `app.py`)
3. It contains the line: `OPENAI_API_KEY = "your-key"`
4. Your API key is correct and starts with `sk-`

### Can't find `.streamlit` folder

Hidden folders (starting with a dot) may not be visible by default:

- **Windows**: In File Explorer, go to View → Show → Hidden items
- **macOS**: In Finder, press `Cmd + Shift + .` to show hidden files
- **Linux**: Use `ls -la` to see hidden folders

### File structure should look like this:

```
Olivetti/
├── .streamlit/              ← You create this folder
│   └── secrets.toml        ← You create this file (your API key)
├── streamlit/              ← Already exists (template only)
│   └── .secrets.toml.example
├── app.py                  ← Main Streamlit application
├── README.md
└── ...
```

## Features Overview

### Web App Features
- **Project Bay System**: 4 bays (NEW, ROUGH, EDIT, FINAL)
- **Writing Desk**: 9 AI-powered writing actions
- **Story Bible**: 5 sections for world-building
- **Voice Bible**: 6 control systems for style customization
- **Auto-save**: Automatic backup with rotation
- **Export**: Multiple formats (Markdown, Manuscript, HTML, DOCX, JSON)

### CLI Features
- **Voice Profiles**: Train custom writing styles
- **Multi-Provider**: OpenAI, Anthropic, or Ollama
- **6 Commands**: continue, rewrite, describe, brainstorm, dialogue, analyze
- **Python API**: Programmatic access

## Next Steps

1. ✅ Set up your API key
2. ✅ Run `streamlit run app.py`
3. 📝 Start writing!
4. 📖 Check out the full README.md for detailed documentation

## Getting Help

- See README.md for complete documentation
- See QUICKSTART.md for CLI tool examples
- See CONTRIBUTING.md if you want to contribute
- Open an issue on GitHub for bugs or questions

---

**Security Note**: Never commit your `.streamlit/secrets.toml` or `.env` files. They are already in `.gitignore` to protect your API keys.
