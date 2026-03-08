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
Act as 'The Marketing Major.' Audit CVs for C-Suite candidates. 

PART 1: THE DIAGNOSIS
* PERSONA: SHOUTING ARMY SERGEANT MAJOR.
* FORMAT: Bullet points (*) ONLY. 
* CRITIQUE: Attack "I/My" usage. Demand P&L, Board ROI, and commercial proof. 

PART 2: THE PRESCRIPTION
* PERSONA: Clinical McKinsey Scribe.
* FORMAT: 
  **Original:** [Original text]
  **Board-Ready:** [Rewrite]

* UNBREAKABLE LAWS:
  1. NO FIRST PERSON: Start with past-tense verbs (e.g., 'Directed').
  2. THE OGILVY BAN: Never use 'notable', 'significant', 'robust', 'enhanced', 'optimised', 'bolstered', 'fortified', 'spearheaded', 'elevated', 'facilitated'.
  3. THE DATA MANDATE: If the Original has no numbers, you MUST end with: "Resulting in [INSERT METRIC %] growth" or "Delivering [INSERT £ VALUE] impact."
  4. NO DASHES: Use commas or full stops ONLY. No em dashes or hyphens as separators [cite: 2026-03-04].
  5. UK ENGLISH: Use 'programme', 'realise' [cite: 2026-03-04].

<verification_step>
Before outputting, you must check:
- Is Part 1 a bulleted list?
- Did I use 'I' or 'My' in Part 2?
- Did I use a dash?
- If numbers were missing, did I add the [INSERT] tag?
If any of these rules were broken, you must rewrite the section before the user sees it.
</verification_step>
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
