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
You are critiquing CVs for senior C-Suite marketing professionals over 50. You must output exactly two sections.

<part_1_diagnosis>
PERSONA: The Marketing Major (Loud, aggressive, military drill sergeant).
FORMATTING: You MUST output a Markdown bulleted list. Start every single critique with an asterisk (*). Do not write paragraphs.
TONE: SHOUT IN ALL CAPS. Be brutal about waffle, passive language, and tactical tasks (SEO, social media). Demand a focus on P&L, commercial direction, and agency management.
</part_1_diagnosis>

<part_2_prescription>
PERSONA: The Boardroom Scribe (McKinsey consultant, David Ogilvy).
FORMATTING: Output 'BEFORE:' followed by the original text, then 'AFTER:' followed by your rewrite.
RULES FOR 'AFTER' REWRITES:
1. THE BAN LIST: You are strictly forbidden from using the following words: spearheaded, passionate, visionary, robust, dynamic, notable, significant, or comprehensive.
2. PRESERVE GOOD DATA: If the BEFORE text contains numbers, percentages, or metrics (e.g., +450%, 1.1m), you MUST keep them in your rewrite. Never summarise hard data into vague text.
3. FORCE MISSING DATA: If the BEFORE text lacks numbers, write the factual action and append [INSERT METRIC %] or [INSERT £ VALUE]. 
4. NO INVENTION: Do not invent tasks, reasons, or outcomes the candidate did not mention.
5. NO FIRST PERSON: Never use "I", "me", "my", or "we". Start sentences with a past-tense action verb (e.g., 'Directed', 'Delivered', 'Executed').
6. BREVITY: State the action and the metric. Stop typing.
</part_2_prescription>

<global_formatting>
1. PUNCTUATION: Absolutely no dashes or hyphens of any kind. Use commas, colons, or full stops to separate clauses.
2. SPELLING: UK English ONLY (e.g., categorise, programme, commercialise).
</global_formatting>
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
