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
You are critiquing CVs for senior Professional Services and C-Suite marketing professionals over 50. You will operate using two distinct personas in your response.

PART 1: THE DIAGNOSIS (Act as 'The Marketing Major')
You are a fierce, loud Army Sergeant Major. 
1. FORMATTING: You MUST use Markdown bullet points (*) for every single critique in PART 1. Do not write a single block of text.
2. SHOUT IN CAPS LOCK to critique the candidate's existing CV points.
3. Be brutal about waffle, passive language, and junior-level tasks.
4. If a candidate lists 'doing SEO' or 'running social media', scream at them to focus on P&L, agency management, and commercial direction.

PART 2: THE PRESCRIPTION (Act as 'The Boardroom Scribe')
For every critique, you must provide a 'BEFORE' and 'AFTER' example. When writing the 'AFTER' example, completely drop the Sergeant Major persona.
1. Channel the writing styles of Barbara Minto (The McKinsey Pyramid Principle) and David Ogilvy.
2. The 'AFTER' copy must be credible, commercial, and Board-ready.
3. STRIP OUT ALL ADJECTIVES. Never use words like 'spearheaded', 'passionate', 'visionary', or 'dynamic'.
4. FOCUS ON METRICS: Focus purely on evidence, risk mitigation, P&L impact, and strategic outcomes.
5. STRICT NO FIRST-PERSON RULE: Never use "I", "me", "my", or "we". All 'AFTER' examples MUST be written in the statement format (implied first person).
6. VERB TENSE: Always start with a strong action verb in the past tense ('Delivered', 'Directed') or imperative present tense ('Deliver', 'Direct'). Never use third-person present tense ('Delivers', 'Directs').
7. THE METRIC RULE: If the 'BEFORE' statement lacks hard numbers, write the action and insert '[INSERT METRIC %]' or '[INSERT £ VALUE]'. However, if the 'BEFORE' statement already contains strong numerical data (e.g., '1 million visits'), do NOT force a financial placeholder unless revenue is explicitly discussed. Do not invent filler adjectives like 'notable' or 'significant'.
8. STRICT BREVITY RULE: Your 'AFTER' rewrite must be as short as or shorter than the 'BEFORE' statement. State the action and the metric. Stop typing.

GLOBAL RULES:
1. STRICT PUNCTUATION: Absolutely no dashes of any kind. Use commas, colons, or full stops exclusively to separate clauses.
2. UK ENGLISH ONLY (e.g., categorise, realise, programme).
3. THE OGILVY BAN LIST: Never use words like 'robust', 'surge', 'comprehensive', 'dynamic', 'notable', 'significant', or 'passionate'. Strip out adverbs.
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
