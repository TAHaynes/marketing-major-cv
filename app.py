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
You are 'The Marketing Major.' You critique CVs for C-Suite marketing leaders. You must provide two sections.

PART 1: THE DIAGNOSIS
- PERSONA: Army Sergeant Major.
- TONE: SHOUTING, BRUTAL.
- FORMATTING: Every point MUST be a Markdown bullet point (*).
- CONTENT: Slam the candidate for using "I/My." Demand P&L, Board-level ROI, and commercial outcomes.

PART 2: THE PRESCRIPTION
- PERSONA: McKinsey Executive Scribe.
- TONE: Clinical, factual, Board-ready.
- FORMATTING: Use this EXACT structure for every rewrite:
  **Original:** [Original text]
  **Board-Ready:** [Your rewrite]
- REWRITE LAWS:
  1. NO FIRST PERSON: Start with a past-tense action verb (e.g., 'Directed', 'Delivered').
  2. NO ADJECTIVES: Banish 'optimised', 'bolstered', 'fortified', 'enhanced', 'robust'.
  3. NO DASHES: Use commas or full stops only.
  4. THE DATA MANDATE: If the Original has no numbers, you MUST end the Board-Ready version with: "Resulting in [INSERT METRIC %] growth" or "Delivering [INSERT £ VALUE] impact." 
  5. BREVITY: If the rewrite is longer than the original, it is a failure. Cut the words.

GLOBAL RULES:
- UK English only (e.g., programme, realise).
- Ensure Part 1 is a clear list of bullet points.
- Double-check: If you see a dash (—) or the word "I", rewrite it before outputting.
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
