"""
Olivetti Creative Editing Partner
A fully functional AI-powered creative writing application in Streamlit.
"""

import streamlit as st
import json
import os
import hashlib
import math
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from openai import OpenAI
from pathlib import Path
import tempfile
import shutil

# ============================================================================
# CONSTANTS
# ============================================================================

BAYS = ["NEW", "ROUGH", "EDIT", "FINAL"]
STORY_BIBLE_SECTIONS = ["Synopsis", "Genre/Style Notes", "World", "Characters", "Outline"]
STYLES = ["Neutral", "Narrative", "Descriptive", "Emotional", "Lyrical", "Sparse", "Ornate"]
GENRES = ["Literary", "Thriller", "Noir", "Horror", "Romance", "Fantasy", "Sci-Fi", "Historical", "Contemporary"]
POVS = ["First", "Close Third", "Omniscient"]
TENSES = ["Past", "Present"]
LANES = ["Narration", "Dialogue", "Interiority", "Action"]
VOICES = ["None", "Voice A", "Voice B"]

AUTOSAVE_PATH = "autosave/olivetti_state.json"
BACKUP_COUNT = 3

# Color palette
CREAM = "#F5F5DC"
BRONZE = "#CD7F32"
CHARCOAL = "#36454F"

# ============================================================================
# VECTOR STORAGE - Hash-based implementation (no external APIs)
# ============================================================================

def text_to_hash_vector(text: str, dimensions: int = 512) -> List[float]:
    """
    Convert text to bag-of-words hash vector using MD5 hashing.
    
    Args:
        text: Input text to vectorize
        dimensions: Vector dimensionality (default 512)
    
    Returns:
        Sparse vector representation
    """
    # Tokenize text
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Create sparse vector
    vector = [0.0] * dimensions
    
    # Hash each word and accumulate into vector
    for word in words:
        word_hash = hashlib.md5(word.encode()).hexdigest()
        # Use first few hex digits to determine index
        index = int(word_hash[:8], 16) % dimensions
        vector[index] += 1.0
    
    # Normalize vector
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude > 0:
        vector = [x / magnitude for x in vector]
    
    return vector


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
    
    Returns:
        Similarity score between 0 and 1
    """
    if len(vec1) != len(vec2):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    return max(0.0, min(1.0, dot_product))


def retrieve_similar_samples(query_text: str, sample_bank: List[Dict], top_k: int = 3) -> List[Dict]:
    """
    Find most similar samples using cosine similarity.
    
    Args:
        query_text: Query text to match
        sample_bank: List of samples with 'text' and 'vector' keys
        top_k: Number of top samples to return
    
    Returns:
        List of most similar samples
    """
    if not sample_bank:
        return []
    
    query_vector = text_to_hash_vector(query_text)
    
    # Compute similarities
    similarities = []
    for sample in sample_bank:
        if 'vector' in sample:
            sim = cosine_similarity(query_vector, sample['vector'])
            similarities.append((sim, sample))
    
    # Sort by similarity and return top_k
    similarities.sort(reverse=True, key=lambda x: x[0])
    return [sample for _, sample in similarities[:top_k]]


# ============================================================================
# LANE DETECTION
# ============================================================================

def detect_lane(text: str) -> str:
    """
    Detect writing lane from text content.
    
    Args:
        text: Text to analyze (typically final paragraph)
    
    Returns:
        Lane name: "Dialogue", "Interiority", "Action", or "Narration"
    """
    if not text:
        return "Narration"
    
    # Get last paragraph
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if not paragraphs:
        return "Narration"
    
    last_para = paragraphs[-1]
    
    # Dialogue detection - quoted speech
    if '"' in last_para or '"' in last_para or '"' in last_para:
        quote_count = last_para.count('"') + last_para.count('"') + last_para.count('"')
        if quote_count >= 2:
            return "Dialogue"
    
    # Interiority detection - thought patterns
    interiority_markers = [
        'thought', 'wondered', 'realized', 'felt', 'knew', 'remembered',
        'understood', 'believed', 'hoped', 'feared', 'wished',
        'could see', 'could hear', 'could feel'
    ]
    lower_para = last_para.lower()
    if any(marker in lower_para for marker in interiority_markers):
        return "Interiority"
    
    # Action detection - kinetic verbs
    action_markers = [
        'ran', 'jumped', 'grabbed', 'threw', 'kicked', 'punched', 'struck',
        'dashed', 'sprinted', 'lunged', 'dove', 'rolled', 'ducked', 'swung',
        'fired', 'shot', 'slammed', 'crashed', 'leaped'
    ]
    if any(marker in lower_para for marker in action_markers):
        # Count action verbs
        action_count = sum(1 for marker in action_markers if marker in lower_para)
        if action_count >= 2:
            return "Action"
    
    # Default to narration
    return "Narration"


# ============================================================================
# OPENAI INTEGRATION
# ============================================================================

def call_openai(system_prompt: str, user_prompt: str, temperature: float) -> Optional[str]:
    """
    Make OpenAI API call with proper error handling.
    
    Args:
        system_prompt: System instruction
        user_prompt: User message
        temperature: Temperature setting (0.0-1.0)
    
    Returns:
        Generated text or None on error
    """
    try:
        # Get API key from secrets
        if 'OPENAI_API_KEY' not in st.secrets:
            st.error("OpenAI API key not found. Please add it to .streamlit/secrets.toml")
            return None
        
        client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=2000,
            timeout=60
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"OpenAI API error: {str(e)}")
        return None


# ============================================================================
# UNIFIED AI BRIEF SYSTEM
# ============================================================================

def build_partner_brief(action: str, lane: str, project: Dict, voice_bible: Dict) -> Tuple[str, str, float]:
    """
    Assemble complete AI brief from all Voice Bible controls.
    
    Args:
        action: Writing action being performed
        lane: Detected writing lane
        project: Current project data
        voice_bible: Voice Bible settings
    
    Returns:
        (system_prompt, user_prompt, temperature)
    """
    # Extract Voice Bible settings
    ai_intensity = voice_bible.get('ai_intensity', 0.5)
    style_engine = voice_bible.get('style_engine', {})
    genre_intelligence = voice_bible.get('genre_intelligence', {})
    trained_voice = voice_bible.get('trained_voice', {})
    match_my_style = voice_bible.get('match_my_style', '')
    voice_lock = voice_bible.get('voice_lock', '')
    technical = voice_bible.get('technical', {})
    
    # Calculate temperature from AI intensity
    temperature = 0.15 + ai_intensity * 0.95
    
    # Build system prompt
    system_parts = []
    
    # Core identity
    system_parts.append("You are the Olivetti Creative Editing Partner, an expert writing assistant.")
    
    # Voice Lock (HIGHEST PRIORITY)
    if voice_lock and voice_lock.strip():
        system_parts.append(f"\n**MANDATORY RULES (HIGHEST PRIORITY):**\n{voice_lock}")
    
    # Technical controls
    pov = technical.get('pov', 'Close Third')
    tense = technical.get('tense', 'Past')
    system_parts.append(f"\nWrite in {pov} POV, {tense} tense.")
    
    # Genre directives
    if genre_intelligence.get('enabled') and genre_intelligence.get('genre') != 'Literary':
        genre = genre_intelligence.get('genre')
        intensity = genre_intelligence.get('intensity', 0.5)
        
        genre_directives = {
            'Thriller': f"Maintain tension and pacing. Build suspense. Keep readers on edge. (Intensity: {intensity:.1f})",
            'Noir': f"Use dark, cynical tone. Emphasize moral ambiguity. Employ atmospheric description. (Intensity: {intensity:.1f})",
            'Horror': f"Create dread and unease. Use visceral imagery. Build atmospheric terror. (Intensity: {intensity:.1f})",
            'Romance': f"Emphasize emotional connection. Build romantic tension. Focus on character feelings. (Intensity: {intensity:.1f})",
            'Fantasy': f"Rich world-building. Vivid magical elements. Maintain internal consistency. (Intensity: {intensity:.1f})",
            'Sci-Fi': f"Technical plausibility. Explore implications. Balance explanation with story. (Intensity: {intensity:.1f})",
            'Historical': f"Period-appropriate language. Historical accuracy. Immersive setting details. (Intensity: {intensity:.1f})",
            'Contemporary': f"Modern voice. Current references. Authentic contemporary feel. (Intensity: {intensity:.1f})"
        }
        
        if genre in genre_directives:
            system_parts.append(f"\nGENRE: {genre_directives[genre]}")
    
    # Style Engine
    if style_engine.get('enabled') and style_engine.get('style') != 'Neutral':
        style = style_engine.get('style')
        intensity = style_engine.get('intensity', 0.5)
        
        style_directives = {
            'Narrative': f"Clear storytelling. Forward momentum. Balanced pacing. (Intensity: {intensity:.1f})",
            'Descriptive': f"Rich sensory detail. Vivid imagery. Immersive atmosphere. (Intensity: {intensity:.1f})",
            'Emotional': f"Deep feeling. Emotional resonance. Character interiority. (Intensity: {intensity:.1f})",
            'Lyrical': f"Poetic language. Rhythmic prose. Beautiful phrasing. (Intensity: {intensity:.1f})",
            'Sparse': f"Economy of language. Minimal description. Direct prose. (Intensity: {intensity:.1f})",
            'Ornate': f"Elaborate language. Complex sentences. Rich vocabulary. (Intensity: {intensity:.1f})"
        }
        
        if style in style_directives:
            system_parts.append(f"\nSTYLE: {style_directives[style]}")
        
        # Retrieve style samples for this lane
        style_banks = voice_bible.get('style_banks', {})
        lane_samples = style_banks.get(lane, [])
        if lane_samples:
            current_text = project.get('draft', '')
            if current_text:
                similar = retrieve_similar_samples(current_text[-500:], lane_samples, top_k=2)
                if similar:
                    system_parts.append("\nSTYLE EXAMPLES:")
                    for i, sample in enumerate(similar, 1):
                        system_parts.append(f"{i}. {sample['text'][:200]}")
    
    # Trained Voice (Voice Vault)
    if trained_voice.get('enabled') and trained_voice.get('voice') != 'None':
        voice_name = trained_voice.get('voice')
        voice_vault = voice_bible.get('voice_vault', {})
        voice_samples = voice_vault.get(voice_name, {}).get(lane, [])
        
        if voice_samples:
            current_text = project.get('draft', '')
            if current_text:
                similar = retrieve_similar_samples(current_text[-500:], voice_samples, top_k=2)
                if similar:
                    system_parts.append(f"\nVOICE SAMPLES ({voice_name}):")
                    for i, sample in enumerate(similar, 1):
                        system_parts.append(f"{i}. {sample['text'][:200]}")
    
    # Match My Style (one-shot)
    if match_my_style and match_my_style.strip():
        system_parts.append(f"\nMATCH THIS STYLE:\n{match_my_style[:300]}")
    
    # Lane context
    lane_context = {
        'Narration': "Continue the narrative flow naturally.",
        'Dialogue': "Write authentic dialogue with natural speech patterns.",
        'Interiority': "Explore character thoughts and emotions deeply.",
        'Action': "Write kinetic, physical action with clear movement."
    }
    system_parts.append(f"\nCONTEXT: {lane_context.get(lane, '')}")
    
    # Story Bible context
    story_bible = project.get('story_bible', {})
    if any(story_bible.get(section) for section in STORY_BIBLE_SECTIONS):
        system_parts.append("\nSTORY CONTEXT:")
        for section in STORY_BIBLE_SECTIONS:
            content = story_bible.get(section, '').strip()
            if content:
                system_parts.append(f"- {section}: {content[:150]}")
    
    system_prompt = '\n'.join(system_parts)
    
    # Build user prompt based on action
    draft = project.get('draft', '')
    
    action_prompts = {
        'Write': f"Continue this draft with 1-3 new paragraphs:\n\n{draft[-1000:]}",
        'Expand': f"Add depth and detail to this text without changing its meaning:\n\n{draft[-500:]}",
        'Describe': f"Add vivid sensory description while preserving pace:\n\n{draft[-500:]}",
        'Rewrite': f"Improve the quality while preserving meaning:\n\n{draft[-500:]}",
        'Rephrase': f"Replace the final sentence with a stronger alternative. Here's the text:\n\n{draft[-500:]}",
        'Spell/Grammar': f"Fix spelling, grammar, and punctuation errors:\n\n{draft[-500:]}",
        'Synonym': f"Provide 12 strong synonym alternatives for the last word, grouped by nuance. Text:\n\n{draft[-200:]}",
        'Sentence': f"Provide 8 rewrites of the final sentence with varied rhythm and diction. Text:\n\n{draft[-200:]}"
    }
    
    user_prompt = action_prompts.get(action, draft[-1000:])
    
    return system_prompt, user_prompt, temperature


# ============================================================================
# AUTO-SAVE SYSTEM
# ============================================================================

def save_state(state: Dict):
    """
    Save application state with atomic writes and backup rotation.
    
    Args:
        state: Application state dictionary
    """
    try:
        # Ensure autosave directory exists
        os.makedirs('autosave', exist_ok=True)
        
        # Rotate backups
        if os.path.exists(AUTOSAVE_PATH):
            for i in range(BACKUP_COUNT - 1, 0, -1):
                old_backup = f"{AUTOSAVE_PATH}.bak{i}" if i > 1 else f"{AUTOSAVE_PATH}.bak"
                new_backup = f"{AUTOSAVE_PATH}.bak{i + 1}"
                if os.path.exists(old_backup):
                    if os.path.exists(new_backup):
                        os.remove(new_backup)
                    shutil.copy2(old_backup, new_backup)
            
            # Create .bak from current
            shutil.copy2(AUTOSAVE_PATH, f"{AUTOSAVE_PATH}.bak")
        
        # Atomic write: write to temp file, then rename
        with tempfile.NamedTemporaryFile(mode='w', dir='autosave', delete=False) as tmp:
            json.dump(state, tmp, indent=2)
            tmp_path = tmp.name
        
        shutil.move(tmp_path, AUTOSAVE_PATH)
        
    except Exception as e:
        st.error(f"Failed to save state: {str(e)}")


def load_state() -> Dict:
    """
    Load application state from autosave.
    
    Returns:
        Application state dictionary or empty state if not found
    """
    try:
        if os.path.exists(AUTOSAVE_PATH):
            with open(AUTOSAVE_PATH, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Failed to load state: {str(e)}")
        # Try backups
        for i in range(1, BACKUP_COUNT + 1):
            backup_path = f"{AUTOSAVE_PATH}.bak{i}" if i > 1 else f"{AUTOSAVE_PATH}.bak"
            try:
                if os.path.exists(backup_path):
                    with open(backup_path, 'r') as f:
                        st.info(f"Loaded from backup {i}")
                        return json.load(f)
            except:
                continue
    
    # Return empty state
    return {
        'projects': {},
        'bay_state': {bay: None for bay in BAYS},
        'voice_bible': initialize_voice_bible(),
        'current_bay': 'NEW',
        'current_project_id': None
    }


def initialize_voice_bible() -> Dict:
    """Initialize Voice Bible with default settings."""
    return {
        'ai_intensity': 0.5,
        'style_engine': {'enabled': False, 'style': 'Neutral', 'intensity': 0.5},
        'genre_intelligence': {'enabled': False, 'genre': 'Literary', 'intensity': 0.5},
        'trained_voice': {'enabled': False, 'voice': 'None', 'intensity': 0.5},
        'match_my_style': '',
        'voice_lock': '',
        'technical': {'pov': 'Close Third', 'tense': 'Past'},
        'style_banks': {lane: [] for lane in LANES},
        'voice_vault': {}
    }


# ============================================================================
# PROJECT MANAGEMENT
# ============================================================================

def create_project(title: str, bay: str = 'NEW') -> Dict:
    """Create a new project."""
    project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(title) % 10000}"
    return {
        'id': project_id,
        'title': title,
        'draft': '',
        'bay': bay,
        'created': datetime.now().isoformat(),
        'modified': datetime.now().isoformat(),
        'story_bible': {section: '' for section in STORY_BIBLE_SECTIONS},
        'tool_output': ''
    }


def promote_project(project: Dict, current_bay: str) -> str:
    """Promote project to next bay."""
    bay_order = ['NEW', 'ROUGH', 'EDIT', 'FINAL']
    if current_bay in bay_order:
        current_idx = bay_order.index(current_bay)
        if current_idx < len(bay_order) - 1:
            return bay_order[current_idx + 1]
    return current_bay


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_as_markdown(project: Dict) -> str:
    """Export project as Markdown with metadata."""
    lines = []
    lines.append("---")
    lines.append(f"title: {project['title']}")
    lines.append(f"created: {project['created']}")
    lines.append(f"modified: {project['modified']}")
    lines.append(f"bay: {project['bay']}")
    lines.append(f"word_count: {len(project['draft'].split())}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {project['title']}")
    lines.append("")
    lines.append(project['draft'])
    return '\n'.join(lines)


def export_as_manuscript(project: Dict) -> str:
    """Export project in manuscript standard format."""
    lines = []
    word_count = len(project['draft'].split())
    
    # Title page
    lines.append(f"{word_count} words")
    lines.append("")
    lines.append("")
    lines.append("")
    lines.append(project['title'])
    lines.append("")
    lines.append("")
    lines.append("")
    
    # Content with proper indentation
    paragraphs = project['draft'].split('\n\n')
    for para in paragraphs:
        if para.strip():
            lines.append(f"    {para.strip()}")
            lines.append("")
    
    return '\n'.join(lines)


def export_as_html(project: Dict) -> str:
    """Export project as HTML (eBook format)."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project['title']}</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.6;
            max-width: 40em;
            margin: 2em auto;
            padding: 0 1em;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 2em;
        }}
        p {{
            text-indent: 2em;
            margin: 0;
            margin-bottom: 1em;
        }}
    </style>
</head>
<body>
    <h1>{project['title']}</h1>
"""
    
    paragraphs = project['draft'].split('\n\n')
    for para in paragraphs:
        if para.strip():
            html += f"    <p>{para.strip()}</p>\n"
    
    html += """</body>
</html>"""
    
    return html


# ============================================================================
# STREAMLIT UI
# ============================================================================

def apply_custom_css():
    """Apply Olivetti aesthetic."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
        
        .stApp {{
            background-color: {CREAM};
        }}
        
        h1, h2, h3 {{
            font-family: 'IBM Plex Mono', monospace;
            color: {CHARCOAL};
        }}
        
        .stTextArea textarea {{
            font-family: 'Libre Baskerville', serif;
            background-color: #FFFFFF;
            border: 2px solid {BRONZE};
        }}
        
        .stButton button {{
            font-family: 'IBM Plex Mono', monospace;
            background-color: {BRONZE};
            color: white;
            border: none;
            border-radius: 4px;
        }}
        
        .stButton button:hover {{
            background-color: {CHARCOAL};
        }}
        
        .bay-button {{
            font-family: 'IBM Plex Mono', monospace;
            padding: 0.5em 1em;
            margin: 0.2em;
            background-color: {BRONZE};
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        
        .bay-button.active {{
            background-color: {CHARCOAL};
        }}
        
        .status-display {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.9em;
            color: {CHARCOAL};
            padding: 0.5em;
            background-color: #E8E8D0;
            border-radius: 4px;
            margin: 1em 0;
        }}
        </style>
    """, unsafe_allow_html=True)


def render_status_display(state: Dict):
    """Render Voice Bible status display."""
    vb = state['voice_bible']
    
    status_parts = []
    
    # AI Intensity
    intensity_level = "LOW" if vb['ai_intensity'] < 0.33 else "MED" if vb['ai_intensity'] < 0.67 else "HIGH"
    status_parts.append(f"AI:{intensity_level}")
    
    # Style
    if vb['style_engine']['enabled']:
        status_parts.append(f"Style:{vb['style_engine']['style']}")
    
    # Genre
    if vb['genre_intelligence']['enabled']:
        status_parts.append(f"Genre:{vb['genre_intelligence']['genre']}")
    
    # Voice
    if vb['trained_voice']['enabled'] and vb['trained_voice']['voice'] != 'None':
        status_parts.append(f"Voice:{vb['trained_voice']['voice']}")
    
    # Technical
    status_parts.append(f"Tech:{vb['technical']['pov']}/{vb['technical']['tense']}")
    
    status_text = " • ".join(status_parts)
    st.markdown(f'<div class="status-display">{status_text}</div>', unsafe_allow_html=True)


def render_bay_buttons(state: Dict):
    """Render bay selection buttons."""
    cols = st.columns(4)
    for i, bay in enumerate(BAYS):
        with cols[i]:
            label = f"{bay}"
            project_id = state['bay_state'].get(bay)
            if project_id and project_id in state['projects']:
                project = state['projects'][project_id]
                label += f"\n{project['title'][:20]}"
            
            if st.button(label, key=f"bay_{bay}", use_container_width=True):
                # Auto-save current project
                if state['current_project_id']:
                    save_state(state)
                
                # Switch bay
                state['current_bay'] = bay
                state['current_project_id'] = state['bay_state'].get(bay)
                save_state(state)


def render_action_bar(state: Dict, project: Dict):
    """Render bottom action bar with 9 buttons."""
    st.markdown("### Writing Desk")
    
    col1, col2, col3 = st.columns(3)
    
    # Content Generation
    with col1:
        st.markdown("**Content Generation**")
        if st.button("✍️ Write", use_container_width=True, help="Continue draft with 1-3 new paragraphs"):
            execute_action(state, project, 'Write')
        if st.button("📈 Expand", use_container_width=True, help="Add depth/detail"):
            execute_action(state, project, 'Expand')
        if st.button("🎨 Describe", use_container_width=True, help="Add vivid sensory description"):
            execute_action(state, project, 'Describe')
    
    # Editing Actions
    with col2:
        st.markdown("**Editing Actions**")
        if st.button("🔄 Rewrite", use_container_width=True, help="Improve quality"):
            execute_action(state, project, 'Rewrite')
        if st.button("💬 Rephrase", use_container_width=True, help="Replace final sentence"):
            execute_action(state, project, 'Rephrase')
        if st.button("✓ Spell/Grammar", use_container_width=True, help="Copyedit"):
            execute_action(state, project, 'Spell/Grammar')
    
    # Tool Outputs
    with col3:
        st.markdown("**Tool Outputs**")
        if st.button("📚 Synonym", use_container_width=True, help="12 alternatives for last word"):
            execute_action(state, project, 'Synonym')
        if st.button("📝 Sentence", use_container_width=True, help="8 rewrites of final sentence"):
            execute_action(state, project, 'Sentence')


def execute_action(state: Dict, project: Dict, action: str):
    """Execute a writing action."""
    if not project['draft'] and action not in ['Write']:
        st.warning("Draft is empty. Use Write to start.")
        return
    
    # Detect lane
    lane = detect_lane(project['draft'])
    
    # Build AI brief
    system_prompt, user_prompt, temperature = build_partner_brief(
        action, lane, project, state['voice_bible']
    )
    
    # Call OpenAI
    with st.spinner(f"Executing {action}..."):
        result = call_openai(system_prompt, user_prompt, temperature)
    
    if result:
        # Tool outputs go to separate panel
        if action in ['Synonym', 'Sentence']:
            project['tool_output'] = result
        else:
            # Content actions modify draft
            if action == 'Write':
                project['draft'] += '\n\n' + result
            elif action == 'Rephrase':
                # Replace last sentence
                sentences = re.split(r'[.!?]+', project['draft'])
                if len(sentences) > 1:
                    project['draft'] = '.'.join(sentences[:-1]) + '.' + result
                else:
                    project['draft'] = result
            else:
                # Replace last portion
                project['draft'] = project['draft'][:-500] + '\n\n' + result if len(project['draft']) > 500 else result
        
        project['modified'] = datetime.now().isoformat()
        save_state(state)
        st.success(f"{action} completed!")
        st.rerun()


def render_story_bible(state: Dict, project: Dict):
    """Render Story Bible interface."""
    st.markdown("### Story Bible")
    
    for section in STORY_BIBLE_SECTIONS:
        with st.expander(section):
            content = st.text_area(
                f"{section} content",
                value=project['story_bible'].get(section, ''),
                height=150,
                key=f"sb_{section}",
                label_visibility="collapsed"
            )
            project['story_bible'][section] = content
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Generate {section}", key=f"gen_{section}"):
                    # Generate content for this section
                    system_prompt = f"You are an expert writing coach. Generate {section} content for a story."
                    user_prompt = f"Based on this context:\n{project['draft'][:500]}\n\nGenerate {section}:"
                    
                    with st.spinner(f"Generating {section}..."):
                        result = call_openai(system_prompt, user_prompt, 0.7)
                    
                    if result:
                        project['story_bible'][section] = result
                        save_state(state)
                        st.rerun()
            
            with col2:
                if st.button(f"Clear {section}", key=f"clear_{section}"):
                    project['story_bible'][section] = ''
                    save_state(state)
                    st.rerun()


def render_voice_bible(state: Dict):
    """Render Voice Bible controls."""
    st.markdown("### Voice Bible")
    
    vb = state['voice_bible']
    
    # AI Intensity
    with st.expander("AI Intensity", expanded=False):
        vb['ai_intensity'] = st.slider(
            "Creativity Level",
            0.0, 1.0, vb['ai_intensity'],
            help="Controls creative risk-taking"
        )
    
    # Style Engine
    with st.expander("Style Engine", expanded=False):
        vb['style_engine']['enabled'] = st.checkbox(
            "Enable Style Engine",
            value=vb['style_engine']['enabled']
        )
        vb['style_engine']['style'] = st.selectbox(
            "Style",
            STYLES,
            index=STYLES.index(vb['style_engine']['style'])
        )
        vb['style_engine']['intensity'] = st.slider(
            "Style Intensity",
            0.0, 1.0, vb['style_engine']['intensity']
        )
        
        # Style Banks
        st.markdown("**Style Banks**")
        lane = st.selectbox("Lane for samples", LANES, key="style_lane")
        sample_text = st.text_area("Add training sample", height=100, key="style_sample")
        if st.button("Add to Style Bank"):
            if sample_text:
                vector = text_to_hash_vector(sample_text)
                vb['style_banks'][lane].append({
                    'text': sample_text,
                    'vector': vector
                })
                # Limit to 250 samples
                if len(vb['style_banks'][lane]) > 250:
                    vb['style_banks'][lane] = vb['style_banks'][lane][-250:]
                save_state(state)
                st.success(f"Added to {lane} Style Bank")
        
        st.text(f"Samples in {lane}: {len(vb['style_banks'].get(lane, []))}")
    
    # Genre Intelligence
    with st.expander("Genre Intelligence", expanded=False):
        vb['genre_intelligence']['enabled'] = st.checkbox(
            "Enable Genre Intelligence",
            value=vb['genre_intelligence']['enabled']
        )
        vb['genre_intelligence']['genre'] = st.selectbox(
            "Genre",
            GENRES,
            index=GENRES.index(vb['genre_intelligence']['genre'])
        )
        vb['genre_intelligence']['intensity'] = st.slider(
            "Genre Intensity",
            0.0, 1.0, vb['genre_intelligence']['intensity']
        )
    
    # Trained Voice (Voice Vault)
    with st.expander("Trained Voice (Voice Vault)", expanded=False):
        vb['trained_voice']['enabled'] = st.checkbox(
            "Enable Trained Voice",
            value=vb['trained_voice']['enabled']
        )
        
        # Initialize voice_vault if not exists
        if 'voice_vault' not in vb:
            vb['voice_vault'] = {}
        
        # Create new voice
        new_voice = st.text_input("Create new voice", key="new_voice")
        if st.button("Create Voice") and new_voice:
            vb['voice_vault'][new_voice] = {lane: [] for lane in LANES}
            save_state(state)
            st.success(f"Created voice: {new_voice}")
        
        # Select voice
        available_voices = ['None', 'Voice A', 'Voice B'] + list(vb['voice_vault'].keys())
        current_voice = vb['trained_voice'].get('voice', 'None')
        if current_voice not in available_voices:
            current_voice = 'None'
        
        vb['trained_voice']['voice'] = st.selectbox(
            "Voice",
            available_voices,
            index=available_voices.index(current_voice)
        )
        
        # Add samples to voice
        if vb['trained_voice']['voice'] != 'None':
            voice_name = vb['trained_voice']['voice']
            if voice_name not in vb['voice_vault']:
                vb['voice_vault'][voice_name] = {lane: [] for lane in LANES}
            
            lane = st.selectbox("Lane for voice samples", LANES, key="voice_lane")
            sample_text = st.text_area("Add voice sample", height=100, key="voice_sample")
            if st.button("Add to Voice Vault"):
                if sample_text:
                    vector = text_to_hash_vector(sample_text)
                    vb['voice_vault'][voice_name][lane].append({
                        'text': sample_text,
                        'vector': vector
                    })
                    # Limit to 60 samples per lane
                    if len(vb['voice_vault'][voice_name][lane]) > 60:
                        vb['voice_vault'][voice_name][lane] = vb['voice_vault'][voice_name][lane][-60:]
                    save_state(state)
                    st.success(f"Added to {voice_name} Voice Vault")
            
            st.text(f"Samples in {lane}: {len(vb['voice_vault'][voice_name].get(lane, []))}")
    
    # Match My Style
    with st.expander("Match My Style", expanded=False):
        vb['match_my_style'] = st.text_area(
            "Paste sample text",
            value=vb['match_my_style'],
            height=150,
            help="One-shot style transfer"
        )
    
    # Voice Lock
    with st.expander("Voice Lock (Hard Constraints)", expanded=False):
        vb['voice_lock'] = st.text_area(
            "Mandatory rules",
            value=vb['voice_lock'],
            height=150,
            help="MANDATORY enforcement, highest priority"
        )
    
    # Technical Controls
    with st.expander("Technical Controls", expanded=False):
        vb['technical']['pov'] = st.selectbox(
            "POV",
            POVS,
            index=POVS.index(vb['technical']['pov'])
        )
        vb['technical']['tense'] = st.selectbox(
            "Tense",
            TENSES,
            index=TENSES.index(vb['technical']['tense'])
        )
    
    # Save changes
    if st.button("Save Voice Bible Settings"):
        save_state(state)
        st.success("Voice Bible settings saved!")


def process_command(state: Dict, command: str):
    """Process special commands."""
    if command.startswith('/create:'):
        # Create new project
        title = command[8:].strip()
        if title:
            project = create_project(title, state['current_bay'])
            state['projects'][project['id']] = project
            state['bay_state'][state['current_bay']] = project['id']
            state['current_project_id'] = project['id']
            save_state(state)
            st.success(f"Created project: {title}")
            st.rerun()
    
    elif command.startswith('/promote'):
        # Promote current project
        if state['current_project_id']:
            project = state['projects'][state['current_project_id']]
            old_bay = state['current_bay']
            new_bay = promote_project(project, old_bay)
            
            if new_bay != old_bay:
                # Remove from old bay
                state['bay_state'][old_bay] = None
                
                # Add to new bay
                project['bay'] = new_bay
                state['bay_state'][new_bay] = project['id']
                state['current_bay'] = new_bay
                
                save_state(state)
                st.success(f"Promoted to {new_bay}")
                st.rerun()
            else:
                st.warning("Already at final bay")
    
    elif command.startswith('/find:'):
        # Search across Story Bible and draft
        search_term = command[6:].strip().lower()
        if search_term and state['current_project_id']:
            project = state['projects'][state['current_project_id']]
            results = []
            
            # Search draft
            if search_term in project['draft'].lower():
                results.append(f"Found in draft")
            
            # Search Story Bible
            for section in STORY_BIBLE_SECTIONS:
                content = project['story_bible'].get(section, '')
                if search_term in content.lower():
                    results.append(f"Found in {section}")
            
            if results:
                st.info("Search results:\n" + "\n".join(results))
            else:
                st.warning("No results found")


def main():
    """Main application."""
    st.set_page_config(
        page_title="Olivetti Creative Editing Partner",
        page_icon="✍️",
        layout="wide"
    )
    
    apply_custom_css()
    
    # Load state
    if 'state' not in st.session_state:
        st.session_state.state = load_state()
    
    state = st.session_state.state
    
    # Header
    st.title("✍️ Olivetti Creative Editing Partner")
    
    # Bay buttons
    render_bay_buttons(state)
    
    # Status display
    render_status_display(state)
    
    # Command input
    command = st.text_input("Command (e.g., /create: My Story, /promote, /find: keyword)", key="command_input")
    if command:
        process_command(state, command)
    
    # Main layout
    col_main, col_sidebar = st.columns([2, 1])
    
    with col_main:
        # Get current project
        project = None
        if state['current_project_id'] and state['current_project_id'] in state['projects']:
            project = state['projects'][state['current_project_id']]
        
        if project:
            st.markdown(f"### {project['title']}")
            st.markdown(f"*Bay: {project['bay']} | Words: {len(project['draft'].split())} | Lane: {detect_lane(project['draft'])}*")
            
            # Draft editor
            draft = st.text_area(
                "Draft",
                value=project['draft'],
                height=400,
                key="draft_editor",
                label_visibility="collapsed"
            )
            
            if draft != project['draft']:
                project['draft'] = draft
                project['modified'] = datetime.now().isoformat()
                save_state(state)
            
            # Tool output panel
            if project.get('tool_output'):
                with st.expander("Tool Output", expanded=True):
                    st.text(project['tool_output'])
                    if st.button("Clear Tool Output"):
                        project['tool_output'] = ''
                        save_state(state)
                        st.rerun()
            
            # Action bar
            render_action_bar(state, project)
            
            # Export options
            with st.expander("Export"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("Export Markdown"):
                        md_content = export_as_markdown(project)
                        st.download_button(
                            "Download MD",
                            md_content,
                            file_name=f"{project['title']}.md",
                            mime="text/markdown"
                        )
                
                with col2:
                    if st.button("Export Manuscript"):
                        ms_content = export_as_manuscript(project)
                        st.download_button(
                            "Download TXT",
                            ms_content,
                            file_name=f"{project['title']}_manuscript.txt",
                            mime="text/plain"
                        )
                
                with col3:
                    if st.button("Export HTML"):
                        html_content = export_as_html(project)
                        st.download_button(
                            "Download HTML",
                            html_content,
                            file_name=f"{project['title']}.html",
                            mime="text/html"
                        )
                
                with col4:
                    if st.button("Export Project JSON"):
                        json_content = json.dumps(project, indent=2)
                        st.download_button(
                            "Download JSON",
                            json_content,
                            file_name=f"{project['title']}_project.json",
                            mime="application/json"
                        )
        else:
            st.info(f"No project in {state['current_bay']} bay. Use /create: [Title] to create one.")
    
    with col_sidebar:
        # Voice Bible
        render_voice_bible(state)
        
        # Story Bible
        if project:
            render_story_bible(state, project)
        
        # Import
        with st.expander("Import"):
            uploaded_file = st.file_uploader("Import project JSON", type=['json'])
            if uploaded_file:
                try:
                    imported = json.load(uploaded_file)
                    if 'id' in imported and 'title' in imported:
                        # Import to current bay
                        imported['bay'] = state['current_bay']
                        state['projects'][imported['id']] = imported
                        state['bay_state'][state['current_bay']] = imported['id']
                        state['current_project_id'] = imported['id']
                        save_state(state)
                        st.success("Project imported!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Import failed: {str(e)}")
    
    # Auto-save on any change
    save_state(state)


if __name__ == "__main__":
    main()
