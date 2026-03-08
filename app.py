import streamlit as st
import tempfile
import openai
from fpdf import FPDF
from PyPDF2 import PdfReader

# 1. Setup & Branding (Must be the very first Streamlit command)
st.set_page_config(page_title="The Marketing Major", page_icon="🪖")

# 2. PDF Generation Logic (Trial Version)
def generate_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    
    # Updated Header for Trial Version
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="The Inspection Report: The Marketing Major", ln=True, align='C')
    pdf.ln(10)
    
    # Body Text
    pdf.set_font("Arial", size=11)
    clean_text = report_text.replace('**', '')
    safe_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=safe_text)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            pdf_bytes = f.read()
            
    return pdf_bytes

st.title("🪖 THE MARKETING MAJOR")
st.subheader("STOP EMBARRASSING YOURSELF. GET A CV THAT ACTUALLY WORKS.")

# 3. Sidebar for Configuration
with st.sidebar:
    st.header("RECRUITMENT COMMAND CENTRE")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.info("Your data is processed and then discarded. No waffle. No traces.")

# 4. The Persona Logic
SYSTEM_PROMPT = """
<system_instructions>
Act as 'The Marketing Major.' You are auditing CVs for C-Suite candidates. This transaction is strictly confidential. You must follow this two-part structure.

PART 1: THE DIAGNOSIS
- PERSONA: Army Sergeant Major. SHOUTING AND BRUTAL.
- FORMAT: A Markdown bulleted list. Start every single line with an asterisk (*). NO PARAGRAPHS.
- LENGTH & SPECIFICITY: You MUST write exactly 6 bullet points. You MUST quote specific weak, fluffy phrases directly from the CV and tear them apart.
- CONTENT: Attack "I/My" usage. Demand P&L, Board ROI, and commercial proof.

PART 2: THE PRESCRIPTION
- PERSONA: Clinical McKinsey Scribe.
- FORMAT: Use exactly this template for each critique:
  **Original:** [Original text]
  **Board-Ready:** [Rewrite]

- UNBREAKABLE REWRITE LAWS:
  1. NO FIRST PERSON: Start the sentence with a clinical, past-tense action verb (e.g., Directed, Delivered, Executed, Restructured, Aligned).
  2. FORBIDDEN WORDS: You are strictly forbidden from using the following words: enhance, enhancing, improve, improving, optimise, elevate, elevating, bolster, robust, notable, or significant.
  3. MISSING DATA RULE: If the original text lacks hard numbers, append exactly this to the end of your rewrite: "[INSERT £ VALUE]" or "[INSERT METRIC %]". Do not invent numbers.
  4. PUNCTUATION RULE: Use commas or full stops only. Absolutely no em dashes or hyphens used as punctuation.
  5. BREVITY: Keep the rewrite punchy and shorter than the original.

GLOBAL RULES:
- STRICT UK ENGLISH: Use UK spelling exclusively (e.g., armour, programme, commercialise, categorise).
</system_instructions>
"""

# 5. File Upload Logic
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
                
                # 6. Display the Results
                st.divider()
                st.markdown("### 📢 THE INSPECTION REPORT")
                st.write(analysis)
                
                # 7. PDF Download Button
                pdf_data = generate_pdf(analysis)
                st.download_button(
                    label="📥 Download Your Marching Orders (PDF)",
                    data=pdf_data,
                    file_name="The_Marketing_Major_Report.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"FALL OUT! SOMETHING WENT WRONG: {e}")

elif not api_key and uploaded_file:
    st.warning("I CAN'T WORK WITHOUT AMMUNITION. ENTER YOUR API KEY IN THE SIDEBAR.")
