# app.py
import streamlit as st
from pathlib import Path
from text_utils import (
    to_upper, to_lower, strip_text, replace_text,
    count_substring, get_stats, add_timestamp
)

st.title("📝 Text Helper App")

# 1. Upload & check
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file is not None:
    file_ext = Path(uploaded_file.name).suffix
    if file_ext != ".txt":
        st.error("Only .txt files are supported.")
    else:
        text = uploaded_file.read().decode("utf-8")

        # 2. Open mode
        mode = st.radio("Select mode:", ["Read", "Append"])

        # 3. Preview
        lines = text.splitlines()
        preview_text = "\n".join(lines[:20])
        st.subheader("📄 Preview (first 20 lines)")
        st.text_area("Preview", preview_text, height=200, key="preview")

        line_count, word_count, char_count = get_stats(text)
        st.write(f"**Lines:** {line_count} | **Words:** {word_count} | **Characters:** {char_count}")

        # 4. String tools
        st.subheader("🔧 String Tools")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("UPPERCASE"):
                text = to_upper(text)
        with col2:
            if st.button("lowercase"):
                text = to_lower(text)
        with col3:
            if st.button("strip"):
                text = strip_text(text)

        old = st.text_input("Replace: old")
        new = st.text_input("Replace: new")
        if st.button("Replace"):
            text = replace_text(text, old, new)

        substring = st.text_input("Count substring:")
        if st.button("Count"):
            count = count_substring(text, substring)
            st.info(f"The substring '{substring}' appears {count} times.")

        # 5. Save (only in Append mode)
        if mode == "Append":
            st.subheader("💾 Append and Save")
            extra_text = st.text_area("Extra text to append", height=100)
            if st.button("Save"):
                final_text = text + "\n" + extra_text
                final_text = add_timestamp(final_text)
                st.download_button(
                    label="Download Edited File",
                    data=final_text,
                    file_name="edited_text.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Saving is disabled in Read mode.")
else:
    st.info("Please upload a .txt file to begin.")
