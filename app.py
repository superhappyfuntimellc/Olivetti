import streamlit as st

st.set_page_config(
    page_title="Olivetti",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ Olivetti")
st.subheader("authorital authors editing muse")

st.markdown("---")

# Main text editor
st.markdown("### Your Writing Space")
text_content = st.text_area(
    "Start writing...",
    height=400,
    placeholder="Begin your creative journey here..."
)

# Display character and word count
if text_content:
    word_count = len(text_content.split()) if text_content.strip() else 0
    char_count = len(text_content)
    line_count = len(text_content.splitlines()) if text_content.strip() else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Characters", char_count)
    with col2:
        st.metric("Words", word_count)
    with col3:
        st.metric("Lines", line_count)

st.markdown("---")
st.markdown("*A simple, elegant writing space for authors and creators.*")
