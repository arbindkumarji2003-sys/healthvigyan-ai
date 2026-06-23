import streamlit as st
from google import genai
from google.genai import types

# 1. 📱 Page Setup (Pure HealthVigyan Branding)
st.set_page_config(page_title="HealthVigyan AI", page_icon="🧬", layout="centered")

st.markdown("""
<style>
    div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input { 
        background-color: #161b22; color: #00e676; border-radius: 8px; 
    }
    .main-header { font-size: 28px; font-weight: bold; color: #00b0ff; text-align: center; margin-bottom: 2px; }
    .sub-header { font-size: 13px; color: #8b949e; text-align: center; margin-bottom: 22px; }
</style>
""", unsafe_allow_html=True)

# 2. 🧠 Gemini API Setup
API_KEY = "AQ.Ab8RN6Iwakmg838mU3TIuHYiBwrtqkESUT17M3fBPXzUqoAB2Q"
client = genai.Client(api_key=API_KEY)

# =====================================================================
# 🎭 THE 4 MASTER PROMPTS (100% Raghav-Free Edition)
# =====================================================================

PROMPT_DECODER = """
You are HealthVigyan AI, an expert Indian Pathologist. Explain the patient's lab report (text or PDF) in simple, reassuring Desi Hindi.
Structure strictly in 4 bullet points with emojis:
1. 📊 रिपोर्ट का सीधा मतलब (2 simple sentences)
2. 🟢 घबराने की बात है या नहीं?
3. 🍎 देसी सलाह / परहेज
4. 👨‍⚕️ डॉक्टर से क्या पूछें?
Strictly end with: "⚠️ ध्यान दें: यह जानकारी आपकी समझ के लिए है। पक्के इलाज और क्लीनिकल सलाह के लिए कृपया अपने डॉक्टर से संपर्क करें।"
"""

PROMPT_PRE_TEST = """
You are HealthVigyan AI. The user will give you a Pathology Test name. 
Give them strict pre-test instructions in simple Desi Hindi in 3 bullet points:
1. ⏰ खाली पेट (Fasting) रहना है या नहीं? (अगर हाँ, तो कितने घंटे)
2. 💧 पानी पी सकते हैं या नहीं?
3. ⚠️ खास सावधानी (जैसे: रात को शराब न पिएं, या सुबह की थायराइड की गोली का नियम)
Strictly end with: "⚠️ टेस्ट से पहले अपनी चुनी हुई पैथोलॉजी लैब के लोकल नियमों का भी पालन करें।"
"""

PROMPT_SYMPTOM_MAPPER = """
You are HealthVigyan AI. The user will describe their physical symptoms.
Suggest 2 or 3 standard routine pathology tests that doctors usually order for these symptoms. 
Explain in 1 simple sentence *why* for each test.
Strictly end with: "⚠️ ध्यान दें: मैं एक AI हूँ। कृपया कोई भी टेस्ट करवाने से पहले अपने डॉक्टर से सलाह जरूर लें।"
"""

PROMPT_PRICE_FINDER = """
You are HealthVigyan AI, an expert diagnostic consultant in Indian Healthcare. 
The user will give you a pathology test name. Provide the typical average market price range and turnaround time (TAT) across India (especially Delhi NCR/Gurgaon area) in simple Desi Hindi.
Structure strictly in 3 bullet points with emojis:
1. 💵 मार्केट का औसत रेट: (Give realistic Gurgaon/NCR price range in ₹, e.g. ₹250 - ₹450)
2. ⏳ रिपोर्ट आने का समय (TAT): (Typical hours/days for results)
3. 🔍 यह टेस्ट किसलिए होता है?: (1 short sentence explanation)
Strictly end with: "⚠️ ध्यान दें: यह एक सामान्य औसत मार्केट रेट है। असली कीमत अलग-अलग ब्रांडेड लैब्स (जैसे Lal PathLabs, SRL, Metropolis) या आपकी लोकल लैब में थोड़ी अलग हो सकती है।"
"""

# 🏥 UI Header (The Original Ecosystem)
st.markdown('<div class="main-header">🏥 HealthVigyan AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">आपका कंप्लीट AI पैथोलॉजी इकोसिस्टम (v4.0)</div>', unsafe_allow_html=True)

# 💡 THE 4 SUPER-TOOLS AS PREMIUM TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 रिपोर्ट डिकोडर", "🍽️ टेस्ट की तैयारी", "🤒 लक्षण ➔ टेस्ट", "💰 टेस्ट प्राइस गाइड"])

# ---------------------------------------------------------------------
# 🛠️ TOOL 1: REPORT DECODER
# ---------------------------------------------------------------------
with tab1:
    report_text = st.text_area("👇 अपनी रिपोर्ट का टेक्स्ट यहाँ पेस्ट करें:", height=110, key="txt_dec")
    uploaded_pdf = st.file_uploader("📁 या अपनी पैथोलॉजी PDF रिपोर्ट यहाँ अपलोड करें:", type=["pdf"], key="pdf_dec")
    
    if st.button("⚡ रिपोर्ट डिकोड करें", type="primary", key="btn_dec", use_container_width=True):
        if uploaded_pdf:
            with st.spinner("🔬 PDF स्कैन हो रही है..."):
                doc_part = types.Part.from_bytes(data=uploaded_pdf.read(), mime_type="application/pdf")
                res = client.models.generate_content(model='gemini-2.5-flash', contents=[PROMPT_DECODER, doc_part])
                st.markdown(res.text)
        elif report_text.strip():
            with st.spinner("🔬 टेक्स्ट पढ़ा जा रहा है..."):
                res = client.models.generate_content(model='gemini-2.5-flash', contents=f"{PROMPT_DECODER}\n\n{report_text}")
                st.markdown(res.text)
        else: st.warning("अरे भाई! पहले टेक्स्ट या PDF कुछ तो डालो!")

# ---------------------------------------------------------------------
# 🛠️ TOOL 2: PRE-TEST GUIDE
# ---------------------------------------------------------------------
with tab2:
    test_name = st.text_input("🧪 किस टेस्ट की तैयारी जाननी है?", placeholder="उदाहरण: Lipid Profile, Fasting Blood Sugar...", key="input_prep")
    if st.button("💡 तैयारी के नियम जानें", type="primary", key="btn_prep", use_container_width=True):
        if test_name.strip():
            with st.spinner("नियम निकाले जा रहे हैं..."):
                res = client.models.generate_content(model='gemini-2.5-flash', contents=f"{PROMPT_PRE_TEST}\n\nTest Name: {test_name}")
                st.markdown(res.text)
        else: st.warning("टेस्ट का नाम तो लिखिए!")

# ---------------------------------------------------------------------
# 🛠️ TOOL 3: SYMPTOM MAPPER
# ---------------------------------------------------------------------
with tab3:
    symptoms = st.text_area("🤒 अपने लक्षण अपनी भाषा में लिखें:", height=110, placeholder="उदाहरण: हर वक्त थकान रहती है, चक्कर आते हैं...", key="txt_sym")
    if st.button("🔍 संभावित टेस्ट जानें", type="primary", key="btn_sym", use_container_width=True):
        if symptoms.strip():
            with st.spinner("लक्षणों का मेडिकल विश्लेषण जारी है..."):
                res = client.models.generate_content(model='gemini-2.5-flash', contents=f"{PROMPT_SYMPTOM_MAPPER}\n\nSymptoms: {symptoms}")
                st.markdown(res.text)
        else: st.warning("पहले अपने लक्षण तो लिखिए!")

# ---------------------------------------------------------------------
# 🛠️ TOOL 4: TEST PRICE FINDER (Neutral All-India Market Brain)
# ---------------------------------------------------------------------
with tab4:
    price_test = st.text_input("💰 किस टेस्ट का रेट और समय जानना है?", placeholder="उदाहरण: CBC, Vitamin D, HbA1c, Thyroid Profile...", key="input_price")
    if st.button("💵 कीमत और समय का पता करें", type="primary", key="btn_price", use_container_width=True):
        if price_test.strip():
            with st.spinner("मार्केट रेट का लाइव विश्लेषण जारी है..."):
                res = client.models.generate_content(model='gemini-2.5-flash', contents=f"{PROMPT_PRICE_FINDER}\n\nTest Name: {price_test}")
                st.markdown(res.text)
        else: st.warning("टेस्ट का नाम टाइप कीजिए, भाई!")