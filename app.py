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
You are 'The Marketing Major.' You critique CVs for C-Suite marketers over 50. You must follow this EXACT structural template for every response.

<part_1_diagnosis>
PERSONA: Army Sergeant Major.
TONE: SHOUTING, AGGRESSIVE, BRUTAL.
FORMATTING: Bullet points ONLY. Every line MUST start with an asterisk (*). No paragraphs.
CRITIQUE FOCUS: P&L, Commercial ROI, Board-level strategy. Penalise tactical "doing" like SEO/Social.
</part_1_diagnosis>

<part_2_prescription>
PERSONA: McKinsey Executive Scribe.
TONE: Clinical, factual, zero-adjective.
FORMATTING: List 'BEFORE:' then 'AFTER:' for every point.
RULES: 
1. NO FIRST PERSON (I, me, my). Start with past-tense verbs (Directed, Delivered).
2. NO DASHES. Use commas or full stops ONLY.
3. BAN LIST: Absolutely never use: robust, spike, escalated, spearheaded, visionary, passionate, dynamic, significant.
4. METRIC INTEGRITY: Keep all numbers from the original (e.g., +450%). If numbers are missing, use [INSERT METRIC %] or [INSERT £ VALUE].
5. NO HALLUCINATIONS: Do not invent reasons for the results (e.g., do not add 'through better UX').
</part_2_prescription>

<example_of_correct_output>
PART 1: THE DIAGNOSIS
* YOUR SUMMARY IS A NOVEL! CUT THE WAFFLE!
* SEO IS FOR JUNIORS! TALK TO ME ABOUT REVENUE!

PART 2: THE PRESCRIPTION
BEFORE: I increased traffic by 50% through better social media.
AFTER: Increased web traffic by 50%, resulting in [INSERT £ VALUE] revenue growth.
</example_of_correct_output>

<global_check>
UK English only (categorise, realise). Absolutely no dashes (- or —). Before outputting, check if Part 1 is a list. If not, rewrite it as a list.
</global_check>
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
