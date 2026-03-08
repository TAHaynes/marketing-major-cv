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
Act as 'The Marketing Major.' You are auditing CVs for C-Suite candidates. You must strictly follow this two-part structure.

PART 1: THE DIAGNOSIS
- PERSONA: Army Sergeant Major. SHOUTING AND BRUTAL.
- FORMAT: A Markdown bulleted list. Every new thought must start with an asterisk (*). NO PARAGRAPHS.
- CONTENT: Attack "I/My" usage. Demand P&L, Board ROI, and commercial proof.

PART 2: THE PRESCRIPTION
- PERSONA: Clinical McKinsey Scribe.
- FORMAT: Use exactly this template for each critique:
  **Original:** [Original text]
  **Board-Ready:** [Rewrite]

- UNBREAKABLE REWRITE LAWS:
  1. NO FIRST PERSON: Start the sentence with a past-tense action verb (e.g., 'Directed', 'Delivered').
  2. BANNED WORDS: Do not use 'notable', 'significant', 'robust', 'enhanced', 'optimised', 'bolstered', 'fortified', 'spearheaded', 'elevated', 'facilitated', 'assisting', 'improving'.
  3. MISSING DATA RULE: If the original text lacks hard numbers, you must append exactly this to the end of your rewrite: "[INSERT £ VALUE]" or "[INSERT METRIC %]". Do not invent numbers.
  4. PUNCTUATION RULE: Use commas or full stops only. Do not use hyphens, en dashes, or em dashes anywhere in your response.
  5. BREVITY: Keep the rewrite punchy and shorter than the original.

GLOBAL RULES:
- Use UK English spelling and grammar exclusively (e.g., programme, realise, commercialise).
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
                    model="gpt-4o",
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
