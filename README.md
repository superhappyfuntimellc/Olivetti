# ✍️ Olivetti Creative Editing Partner

A fully functional AI-powered creative writing application built with Streamlit. Olivetti combines traditional writing craft with modern AI assistance to help authors develop, draft, and polish their creative work.

## Features

### 🗂️ Project Bay System (4 Bays)
- **NEW** - Story Bible workspace, pre-project ideation
- **ROUGH** - First draft bay, heavy AI assistance
- **EDIT** - Revision bay, polish and refine
- **FINAL** - Publication ready

Each bay remembers its last active project, auto-saves on bay switch, and supports project promotion.

### ✍️ Writing Desk (9 Actions)
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

### 🎯 Lane Detection (Automatic)
System automatically analyzes your writing and detects:
- **Narration** — Default descriptive/narrative prose
- **Dialogue** — Quoted speech, conversational patterns
- **Interiority** — Internal thoughts, character psychology
- **Action** — Physical movement, kinetic sequences

### 📖 Story Bible (5 Sections)
- Synopsis — Core conflict, characters, stakes
- Genre/Style Notes — Tone, voice, stylistic markers
- World — Setting, rules, atmosphere, time period
- Characters — Names, roles, relationships, motivations
- Outline — Acts, beats, key scenes, turning points

Features: Manual editing, AI generation, document import (.txt, .md, .docx), merge modes, Canon Guardian toggle, Markdown export

### 🎨 Voice Bible (6 Control Systems)

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

### 📊 Analysis Tools (Alpha)
- Style Sample Analysis
- Voice Conformity scoring (0-100)
- Canon Conformity checking

### 💾 Auto-Save System
- Saves after EVERY action
- Backup rotation (.bak, .bak1, .bak2, .bak3)
- Atomic writes for safety
- State survives browser refresh

### 📤 Export Formats
- Markdown with metadata
- Manuscript Standard format
- HTML (eBook)
- DOCX (optional)
- Project JSON

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/superhappyfuntimellc/Olivetti.git
cd Olivetti
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure OpenAI API key:
```bash
# Create secrets file
mkdir -p .streamlit
cp streamlit/.secrets.toml.example .streamlit/secrets.toml

# Edit .streamlit/secrets.toml and add your API key
# OPENAI_API_KEY = "sk-proj-your-key-here"
```

4. Run the application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

### Creating a Project
Type in the command input:
```
/create: My Novel Title
```

### Writing
1. Click on a bay (NEW, ROUGH, EDIT, FINAL) to activate it
2. Use your project in that bay or create a new one
3. Type or paste your draft in the editor
4. Use the Writing Desk buttons to enhance your text
5. All changes auto-save automatically

### Training the AI
1. Open **Voice Bible** in the sidebar
2. Enable **Style Engine** or **Trained Voice**
3. Add training samples for your preferred writing style
4. The system will retrieve similar examples during generation

### Voice Lock (Hard Rules)
Use Voice Lock for strict constraints:
```
NEVER use adverbs ending in -ly
ALWAYS use active voice
NEVER use semicolons
```

### Promoting Projects
Move a project to the next bay:
```
/promote
```

### Searching
Search across Story Bible and draft:
```
/find: character name
```

## Architecture

### Hash-Based Vectors
Olivetti uses hash-based bag-of-words vectors (no external embedding API required):
- 512-dimensional sparse vectors
- MD5 hashing for word-to-index mapping
- Cosine similarity for retrieval
- Trainable Style Banks and Voice Vault

### Unified AI Brief System
All Voice Bible controls feed into a single `build_partner_brief()` function that constructs the complete system prompt for OpenAI, ensuring consistency across all actions.

### Auto-Save
State persists in `autosave/olivetti_state.json` with automatic backup rotation. All projects, bays, Voice Vault, and Style Banks are preserved.

## Design Philosophy

**Olivetti Aesthetic:**
- Vintage typewriter meets modern LCD
- Color palette: Cream (#F5F5DC), Bronze (#CD7F32), Charcoal (#36454F)
- Paper-texture editing area
- Monospace headers (IBM Plex Mono)
- Serif body text (Libre Baskerville)

**Training Makes Perfect:**
The more samples you add to Style Banks and Voice Vault, the better the system adapts to your unique writing style.

## File Structure
```
olivetti/
├── app.py                      # Main application (all features)
├── requirements.txt            # Dependencies
├── streamlit/
│   └── .secrets.toml.example   # API key template
├── autosave/                   # Auto-created for saves
│   └── .gitkeep
└── README.md                   # This file
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
