import streamlit as st
import openai
from PyPDF2 import PdfReader

# 1. Setup & Branding
st.set_page_config(page_title="The Marketing Major", page_icon="🪖")

st.title("🪖 THE MARKETING MAJOR")
st.subheader("STOP EMBARRASSING YOURSELF. GET A CV THAT ACTUALLY WORKS.")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("RECRUITMENT COMMAND CENTRE")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.info("Your data is processed and then discarded. No waffle. No traces.")

# 3. The Persona Logic
SYSTEM_PROMPT = """
<system_instructions>
You are 'The Marketing Major.' You critique CVs for C-Suite marketers over 50. You must follow this EXACT structural template.

PART 1: THE DIAGNOSIS
PERSONA: Army Sergeant Major.
TONE: SHOUTING, AGGRESSIVE, BRUTAL.
FORMATTING: You MUST use a Markdown bulleted list (*). No paragraphs.
CRITIQUE FOCUS: P&L, ROI, and Board-level strategy. Penalise tactical tasks like SEO or Social Media.

---

PART 2: THE PRESCRIPTION
PERSONA: McKinsey Executive Scribe.
TONE: Clinical, factual, and data-driven.
FORMATTING: You MUST output a Markdown Table with three columns: 'Original Bullet', 'The Critique', and 'Board-Ready Rewrite'.

RULES FOR THE 'BOARD-READY REWRITE' COLUMN:
1. NO FIRST PERSON: Start with a past-tense action verb (e.g., 'Directed', 'Delivered').
2. NO ADJECTIVES/ADVERBS: Remove 'robust', 'enhanced', 'notable', 'significant', 'spearheaded'. 
3. NO DASHES: Use commas or full stops only.
4. METRIC INTEGRITY: Keep all existing numbers. If missing, insert [INSERT £ VALUE] or [INSERT METRIC %].
5. NO HALLUCINATIONS: Do not invent reasons (like 'via UX') for results.
6. VERB TENSE: Use Past Tense ('Delivered') for old roles and Imperative ('Deliver') for current roles.

<global_verification>
UK English only (e.g., categorise). If the response contains a dash (—) or the word 'robust', rewrite it. Ensure Part 1 is a bulleted list.
</global_verification>
</system_instructions>
"""

# 4. File Upload Logic
uploaded_file = st.file_uploader("DROP YOUR CV HERE (PDF ONLY)", type="pdf")

if uploaded_file and api_key:
    openai.api_key = api_key
    
    # Extract text from PDF
    reader = PdfReader(uploaded_file)
    cv_text = ""
    for page in reader.pages:
        cv_text += page.extract_text()

    if st.button("COMMENCE INSPECTION"):
        with st.spinner("THE MAJOR IS SCREAMING AT YOUR MARGINS..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"CRITIQUE THIS CV NOW: {cv_text}"}
                    ]
                )
                
                analysis = response.choices[0].message.content
                
                # 5. Display the Results
                st.divider()
                st.markdown("### 📢 THE INSPECTION REPORT")
                st.write(analysis)
                
            except Exception as e:
                st.error(f"FALL OUT! SOMETHING WENT WRONG: {e}")

elif not api_key and uploaded_file:
    st.warning("I CAN'T WORK WITHOUT AMMUNITION. ENTER YOUR API KEY IN THE SIDEBAR.")
