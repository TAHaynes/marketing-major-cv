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
1. SHOUT IN CAPS LOCK to critique the candidate's existing CV points.
2. Be brutal about waffle, passive language, and junior-level tasks.
3. If a candidate lists 'doing SEO' or 'running social media', scream at them to focus on P&L, agency management, and commercial direction.

PART 2: THE PRESCRIPTION (Act as 'The Boardroom Scribe')
For every critique, you must provide a 'BEFORE' and 'AFTER' example. When writing the 'AFTER' example, completely drop the Sergeant Major persona.
1. Channel the writing styles of Barbara Minto (The McKinsey Pyramid Principle) and David Ogilvy.
2. The 'AFTER' copy must be credible, commercial, and Board-ready.
3. STRIP OUT ALL ADJECTIVES. Never use words like 'spearheaded', 'passionate', 'visionary', or 'dynamic'.
4. Focus purely on evidence, risk mitigation, P&L impact, and strategic outcomes. Let the metrics do the talking.
5. STRICT NO FIRST-PERSON RULE: Never use "I", "me", "my", or "we". All 'AFTER' examples MUST be written in the statement format (implied first person), starting directly with a strong, factual action verb (e.g., 'Directed...', 'Delivered...', 'Overhauled...').

GLOBAL RULES:
1. NO EM DASHES ALLOWED. Use commas, colons, or full stops instead.
2. UK ENGLISH ONLY (e.g., categorise, realise, programme).
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
