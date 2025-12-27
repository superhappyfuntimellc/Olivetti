# ✍️ Olivetti - AI-Powered Writing Assistant

A comprehensive AI-powered creative writing platform combining a powerful web interface with a flexible command-line tool. Olivetti helps authors develop, draft, and polish their creative work using AI assistance that learns your unique writing style.

## 🎯 Two Ways to Write

### 1. 🖥️ Web App (Streamlit) - Full Creative Suite
A feature-rich web application with visual project management, Story Bible, and advanced Voice controls.

### 2. ⌨️ CLI Tool - Fast & Scriptable
A command-line interface for quick writing tasks, automation, and integration into your workflow.

---

## 📦 Installation

```bash
git clone https://github.com/superhappyfuntimellc/Olivetti.git
cd Olivetti
pip install -r requirements.txt
```

For CLI usage, also install the package:
```bash
pip install -e .
```

### API Key Configuration

**For Web App:**
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-proj-your-key-here"
OPENAI_MODEL = "gpt-4"  # optional
```

**For CLI Tool:**
Create `.env` file or set environment variable:
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
export AI_PROVIDER="openai"  # or "anthropic" or "ollama"
```

---

## 🖥️ Web App Features

### Project Bay System (4 Bays)
- **NEW** - Story Bible workspace, pre-project ideation
- **ROUGH** - First draft bay, heavy AI assistance
- **EDIT** - Revision bay, polish and refine
- **FINAL** - Publication ready

Each bay remembers its last active project, auto-saves on bay switch, and supports project promotion via `/promote`.

### Writing Desk (9 Actions)
**Content Generation:**
- **Write** — Continue draft with 1-3 new paragraphs
- **Expand** — Add depth/detail without changing meaning
- **Describe** — Add vivid sensory description

**Editing Actions:**
- **Rewrite** — Improve quality while preserving meaning
- **Rephrase** — Replace final sentence with stronger alternative
- **Spell/Grammar** — Copyedit spelling/grammar/punctuation

**Tool Outputs:**
- **Synonym** — 12 strong alternatives for last word
- **Sentence** — 8 rewrites of final sentence

### Lane Detection (Automatic)
System automatically analyzes your writing and detects:
- **Narration** — Default descriptive/narrative prose
- **Dialogue** — Quoted speech, conversational patterns
- **Interiority** — Internal thoughts, character psychology
- **Action** — Physical movement, kinetic sequences

### Story Bible (5 Sections)
- Synopsis — Core conflict, characters, stakes
- Genre/Style Notes — Tone, voice, stylistic markers
- World — Setting, rules, atmosphere, time period
- Characters — Names, roles, relationships, motivations
- Outline — Acts, beats, key scenes, turning points

Features: Manual editing, AI generation, document import (.txt, .md, .docx), merge modes, Canon Guardian toggle, Markdown export

### Voice Bible (6 Control Systems)

#### AI Intensity (Master Control)
Range: 0.0 (LOW) to 1.0 (MAX) - Controls creativity and risk-taking

#### Style Engine (Trainable)
7 Styles: Neutral / Narrative / Descriptive / Emotional / Lyrical / Sparse / Ornate
- Store up to 250 training samples per lane
- Semantic retrieval of best exemplars during generation

#### Genre Intelligence
9 Genres: Literary / Thriller / Noir / Horror / Romance / Fantasy / Sci-Fi / Historical / Contemporary
- Genre-specific mood directives
- Adjusts pacing and tension patterns

#### Trained Voice (Voice Vault)
- Custom voices with up to 60 samples per lane
- Hash-based semantic vectors (512 dimensions)
- Cosine similarity retrieval

#### Match My Style (One-Shot)
- Paste sample text for instant style transfer
- No training required

#### Voice Lock (Hard Constraints)
- MANDATORY enforcement, highest priority
- Example: "NEVER use adverbs ending in -ly"

#### Technical Controls
- POV: First / Close Third / Omniscient
- Tense: Past / Present

### Analysis Tools (Alpha)
- Style Sample Analysis
- Voice Conformity scoring (0-100)
- Canon Conformity checking

### Auto-Save System
- Saves after EVERY action
- Backup rotation (.bak, .bak1, .bak2, .bak3)
- Atomic writes for safety
- State survives browser refresh

### Export Formats
- Markdown with metadata
- Manuscript Standard format
- HTML (eBook)
- DOCX (optional)
- Project JSON

### Desktop Mode
- Run as a standalone desktop application
- Native window experience (with pywebview)
- No browser needed
- Cross-platform: Windows, macOS, Linux

## Running the Web App

**Desktop Mode (Recommended):**
```bash
# Windows
launch_desktop.bat

# macOS/Linux
./launch_desktop.sh

# Or directly with Python
python desktop_launcher.py
```

For native desktop window, install optional dependency:
```bash
pip install pywebview>=4.0.0
```

**Browser Mode:**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Web App Commands
- `/create: [Title]` — Create new project in current bay
- `/promote` — Move project to next bay
- `/find: [term]` — Search across Story Bible and draft

---

## ⌨️ CLI Tool Features

### Voice Profile System
- JSON-persisted writer profiles with style samples
- Genre preferences and contextual metadata
- Multi-provider support (OpenAI, Anthropic, Ollama)

### Writing Commands
Six specialized commands:
- **continue** — Continue writing from where you left off
- **rewrite** — Improve existing text while preserving meaning
- **describe** — Add vivid sensory description
- **brainstorm** — Generate creative ideas
- **dialogue** — Create character dialogue
- **analyze** — Analyze writing style and quality

### Multi-Provider Engine
Abstract interface supporting:
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude)
- **Ollama** (local models)

## Using the CLI Tool

### Create and Train a Voice Profile

```bash
# Create a profile
olivetti profile create novelist --style "literary fiction, lyrical prose"

# Add writing samples
olivetti profile add-sample novelist --file published-work.txt
olivetti profile add-sample novelist --text "Sample prose here..."

# List profiles
olivetti profile list

# View profile details
olivetti profile show novelist
```

### Writing Operations

```bash
# Continue writing (from stdin)
echo "The letter arrived on Tuesday." | olivetti continue --length long

# Continue from file
olivetti continue --file draft.txt --length medium

# Rewrite with instructions
olivetti rewrite --file chapter1.txt --instruction "increase tension"

# Add description
olivetti describe --file scene.txt --focus "setting and atmosphere"

# Generate dialogue
olivetti dialogue --characters "Alice, Bob" --situation "confronting betrayal"

# Brainstorm ideas
olivetti brainstorm --topic "plot twist ideas" --count 10

# Analyze writing
olivetti analyze --file manuscript.txt
```

### Provider Configuration

```bash
# Use OpenAI (default)
export AI_PROVIDER=openai
export OPENAI_API_KEY="sk-..."

# Use Anthropic
export AI_PROVIDER=anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Use Ollama (local)
export AI_PROVIDER=ollama
export OLLAMA_MODEL="llama2"
```

### Python API

```python
from olivetti import WritingAssistant, VoiceProfile

# Create and train a profile
profile = VoiceProfile("my-voice")
profile.add_writing_sample(text, description="Award-winning chapter")
profile.save()

# Use the assistant
assistant = WritingAssistant(voice_profile="my-voice")
continuation = assistant.continue_writing(text, length="medium")
```

---

## 🏗️ Architecture

### Hash-Based Vectors (Web App)
- 512-dimensional sparse vectors using MD5 hashing
- No external embedding API required
- Cosine similarity for style sample retrieval
- Trainable Style Banks and Voice Vault

### Voice Profile System (CLI)
- JSON-persisted profiles with metadata
- Sample-based style learning
- Provider-agnostic architecture
- Factory pattern for AI providers

### Unified AI Brief System (Web App)
All Voice Bible controls feed into a single `build_partner_brief()` function that constructs complete system prompts for OpenAI.

---

## 📁 Project Structure

```
olivetti/
├── app.py                          # Streamlit web application
├── desktop_launcher.py             # Desktop mode launcher
├── launch_desktop.bat              # Windows launcher
├── launch_desktop.sh               # Unix/Linux/macOS launcher
├── olivetti/                       # Python package (CLI tool)
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── voice_profile.py            # Voice profile system
│   ├── ai_engine.py                # Multi-provider AI engine
│   ├── assistant.py                # Writing assistant core
│   └── cli.py                      # Command-line interface
├── examples/
│   └── example_usage.py            # Python API examples
├── tests/
│   ├── __init__.py
│   └── test_basic.py               # Unit tests
├── autosave/                       # Auto-save directory (web app)
├── streamlit/
│   └── .secrets.toml.example       # API key template (web app)
├── requirements.txt                # Dependencies
├── setup.py                        # Package setup
├── README.md                       # This file
├── QUICKSTART.md                   # Quick start guide
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # MIT License
└── .env.example                    # Environment variables template
```

---

## 🎨 Design Philosophy

**Olivetti Aesthetic (Web App):**
- Vintage typewriter meets modern LCD
- Color palette: Cream (#F5F5DC), Bronze (#CD7F32), Charcoal (#36454F)
- Paper-texture editing area
- Monospace headers (IBM Plex Mono)
- Serif body text (Libre Baskerville)

**Training Makes Perfect:**
The more samples you add to Style Banks, Voice Vault (web app), or Voice Profiles (CLI), the better the system adapts to your unique writing style.

---

## 🧪 Testing

Run tests for the CLI package:
```bash
pytest tests/
```

---

## 📚 Documentation

- **README.md** - This file (overview and features)
- **QUICKSTART.md** - Quick start guide for CLI tool
- **CONTRIBUTING.md** - Contribution guidelines

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🆘 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example code in `examples/`

---

## 🔮 Roadmap

- [ ] Additional AI providers (Google, Cohere)
- [ ] Collaborative editing features
- [ ] Advanced analytics and insights
- [ ] Mobile app companion
- [ ] Plugin system for extensions

---

Made with ❤️ for writers, by writers.
