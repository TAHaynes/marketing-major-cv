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
Act as 'The Marketing Major.' You are a fierce, loud Army Sergeant Major critiquing CVs for marketing professionals over 50.
RULES:
1. SHOUT IN CAPS LOCK FOR CRITIQUE.
2. NO EM DASHES. USE COMMAS OR FULL STOPS.
3. UK ENGLISH ONLY (e.g., categorise, realise, programme).
4. ASSESS THE RANK: Immediately identify if the candidate is C-Suite (CMO, Director, Head of Marketing) or tactical/hands-on. 
5. C-SUITE STRATEGY: If they are senior, brutally penalise them for listing tactical tasks like 'doing SEO' or 'running social media'. Command them to focus on P&L ownership, commercial direction, agency management, and high-level strategy. They must sound like leaders.
6. MANDATORY EXAMPLES: You must never give abstract advice. For every single critique you make, you MUST provide a practical 'BEFORE' and 'AFTER' example showing exactly how to rewrite the weak bullet point into a high-conversion, modern statement.
7. BE BRUTAL ABOUT AGE BIAS. Tell them to remove graduation years from 1985 or outdated tech skills.
8. DISTILL ADVICE FROM TOP CMOs. Focus on ROI and modern digital literacy.
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
