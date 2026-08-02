import json
import re
import requests
import streamlit as st

st.set_page_config(
    page_title="Zomato / Swiggy Review Analyser",
    page_icon="🍽️",
    layout="centered"
)

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

st.markdown('''
<style>
.stApp { background-color: #212121; color: #ececec; }
.block-container { max-width: 920px; padding-top: 1.5rem; padding-bottom: 6rem; }
[data-testid="stSidebar"] { background-color: #171717; }
[data-testid="stSidebar"] * { color: #ececec; }
.hero { text-align: center; padding: 18px 10px 18px 10px; }
.hero-title { font-size: 34px; font-weight: 800; color: #ffffff; margin-bottom: 6px; }
.hero-subtitle { font-size: 15px; color: #b4b4b4; }
.ai-badge {
    display: inline-block; background: #2f2f2f; color: #fbbf24;
    padding: 6px 13px; border-radius: 999px; font-size: 13px;
    margin-bottom: 10px; border: 1px solid #3f3f46;
}
.stTextArea textarea {
    background-color: #2f2f2f !important; color: #ffffff !important;
    border: 1px solid #4b5563 !important; border-radius: 16px !important;
}
.stButton button {
    width: 100%; border-radius: 14px; background-color: #ffffff;
    color: #111827; border: none; font-weight: 700; padding: 0.7rem 1rem;
}
.stButton button:hover { background-color: #e5e7eb; color: #111827; }
.result-card {
    background: #2f2f2f; border: 1px solid #3f3f46;
    border-radius: 18px; padding: 18px; margin: 10px 0;
}
.result-title { font-size: 19px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
.result-text { color: #ececec; line-height: 1.7; }
.good, .bad, .warn, .info {
    border-radius: 14px; padding: 10px 12px; margin: 6px 0;
}
.good { background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.35); }
.bad { background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.35); }
.warn { background: rgba(251, 191, 36, 0.12); border: 1px solid rgba(251, 191, 36, 0.35); }
.info { background: rgba(59, 130, 246, 0.12); border: 1px solid rgba(59, 130, 246, 0.35); }
.metric-box {
    background: #2f2f2f; border: 1px solid #3f3f46;
    border-radius: 18px; padding: 15px; text-align: center;
}
.metric-label { color: #b4b4b4; font-size: 13px; }
.metric-value { color: #ffffff; font-size: 22px; font-weight: 800; margin-top: 4px; }
.input-card { background: #2f2f2f; border-radius: 22px; padding: 16px; border: 1px solid #3f3f46; }
.small-muted { color: #9ca3af; font-size: 13px; }
hr { border-color: #3f3f46; }
</style>
''', unsafe_allow_html=True)


def check_ollama_running():
    try:
        response = requests.get("http://localhost:11434", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return json.loads(match.group())
    raise ValueError("Could not parse JSON from model response. Try temperature 0.1 or 0.2.")


def analyse_reviews_ollama(reviews_text, output_language, model_name, temperature):
    system_prompt = '''
You are an expert restaurant review analyst.
You convert unstructured customer reviews into a clean structured business report.
Return valid JSON only.
No markdown.
No explanation outside JSON.
'''
    user_prompt = f'''
Analyse these restaurant reviews from Zomato / Swiggy / Google reviews.

REVIEWS:
{reviews_text}

Return ONLY valid JSON in this exact format:
{{
  "overall_sentiment": "Positive / Neutral / Negative / Mixed",
  "estimated_rating_out_of_5": 4.2,
  "one_line_verdict": "short verdict",
  "summary": "short paragraph summary",
  "top_positives": ["point 1", "point 2", "point 3"],
  "top_negatives": ["point 1", "point 2", "point 3"],
  "customer_pain_points": ["point 1", "point 2", "point 3"],
  "business_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
  "best_for": ["family", "friends", "quick snack"],
  "keywords": ["food", "service", "ambience"]
}}

Output language: {output_language}
Keep the response practical, concise and useful.
'''
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"temperature": temperature}
    }
    response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=180)
    response.raise_for_status()
    raw_text = response.json()["message"]["content"]
    return extract_json(raw_text)


with st.sidebar:
    st.title("🍽️ Review Analyser")
    st.caption("AI School of India — Module 1 Project")

    model_name = st.selectbox(
        "Ollama Model",
        ["qwen2.5:3b", "llama3.2:1b", "llama3.2", "mistral"],
        index=0
    )

    output_language = st.selectbox(
        "Output Language",
        ["English", "Telugu", "Tenglish"],
        index=0
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Low temperature gives more stable structured JSON output."
    )

    if st.button("Clear Result"):
        st.session_state.pop("analysis_result", None)
        st.rerun()

    st.markdown("---")
    st.markdown("### Setup Commands")
    st.code("ollama pull qwen2.5:3b\nstreamlit run app.py", language="bash")


st.markdown('''
<div class="hero">
    <div class="ai-badge">Powered by Ollama + Qwen2.5:3b</div>
    <div class="hero-title">Zomato / Swiggy Review Analyser</div>
    <div class="hero-subtitle">Paste restaurant reviews and convert them into a clear AI-powered business report.</div>
</div>
''', unsafe_allow_html=True)

if not check_ollama_running():
    st.error("Ollama is not running.")
    st.info("Open PowerShell and run: ollama serve")
    st.code("ollama serve\nollama pull qwen2.5:3b", language="bash")
    st.stop()

sample_reviews = '''Food was amazing and biryani quantity was good.
Delivery was very late and food became cold.
Paneer starter was tasty but too spicy.
Packaging was neat and no leakage.
Prices are high compared to quantity.
Customer support was not helpful.
Ambience is good for family.
Service was slow during weekend.
Desserts were excellent.
Overall food taste is good but delivery needs improvement.'''

st.markdown('<div class="input-card">', unsafe_allow_html=True)
reviews_text = st.text_area(
    "Paste 5–20 restaurant reviews",
    value=sample_reviews,
    height=260,
    help="Paste one review per line for better analysis."
)
review_count = len([r for r in reviews_text.splitlines() if r.strip()])
st.markdown(f'<div class="small-muted">Detected reviews: {review_count}</div>', unsafe_allow_html=True)
analyse_button = st.button("Analyse Reviews 🚀")
st.markdown("</div>", unsafe_allow_html=True)

if analyse_button:
    if not reviews_text.strip():
        st.warning("Please paste some reviews first.")
    else:
        with st.spinner("Analysing reviews locally using Ollama..."):
            try:
                result = analyse_reviews_ollama(reviews_text, output_language, model_name, temperature)
                st.session_state["analysis_result"] = result
            except requests.exceptions.HTTPError as e:
                st.error(f"HTTP Error: {e}")
                st.info(f"If model is missing, run: ollama pull {model_name}")
                st.stop()
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Try temperature 0.1 or 0.2 if JSON parsing fails.")
                st.stop()

if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]

    st.markdown("---")
    st.markdown("## 📊 Analysis Result")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Overall Sentiment</div><div class="metric-value">{result.get("overall_sentiment", "N/A")}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Estimated Rating</div><div class="metric-value">{result.get("estimated_rating_out_of_5", "N/A")}/5</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Verdict</div><div class="metric-value" style="font-size:16px;">{result.get("one_line_verdict", "N/A")}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="result-card"><div class="result-title">🧾 Summary</div><div class="result-text">{result.get("summary", "No summary available.")}</div></div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="result-card"><div class="result-title">✅ Top Positives</div>', unsafe_allow_html=True)
        for item in result.get("top_positives", []):
            st.markdown(f'<div class="good">{item}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="result-card"><div class="result-title">🔑 Keywords</div>', unsafe_allow_html=True)
        st.write(", ".join(result.get("keywords", [])))
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="result-card"><div class="result-title">❌ Top Negatives</div>', unsafe_allow_html=True)
        for item in result.get("top_negatives", []):
            st.markdown(f'<div class="bad">{item}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="result-card"><div class="result-title">👥 Best For</div>', unsafe_allow_html=True)
        st.write(", ".join(result.get("best_for", [])))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="result-card"><div class="result-title">😟 Customer Pain Points</div>', unsafe_allow_html=True)
    for item in result.get("customer_pain_points", []):
        st.markdown(f'<div class="warn">{item}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="result-card"><div class="result-title">💡 Business Suggestions</div>', unsafe_allow_html=True)
    for item in result.get("business_suggestions", []):
        st.markdown(f'<div class="info">{item}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="Download Analysis as JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="restaurant_review_analysis.json",
        mime="application/json"
    )
