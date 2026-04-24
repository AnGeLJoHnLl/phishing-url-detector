import streamlit as st
import joblib
import pandas as pd
from feature_extractor import extract_features

st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🔐",
    layout="wide"
)

model = joblib.load("model.pkl")

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top center, rgba(0, 180, 255, 0.20), transparent 35%),
        radial-gradient(circle at left, rgba(168, 85, 247, 0.22), transparent 35%),
        linear-gradient(135deg, #020617 0%, #050816 45%, #020617 100%);
    color: white;
}

.block-container {
    padding-top: 3rem;
    max-width: 1100px;
}

.hero {
    text-align: center;
    margin-bottom: 35px;
}

.icon {
    font-size: 70px;
    margin-bottom: 10px;
    filter: drop-shadow(0 0 18px #8b5cf6);
}

.title {
    font-size: 64px;
    font-weight: 900;
    line-height: 1.1;
}

.gradient-text {
    background: linear-gradient(90deg, #a855f7, #2563eb, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 20px;
    color: #cbd5e1;
    margin-top: 15px;
}

.input-label {
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 10px;
}

.stTextInput input {
    background-color: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(148, 163, 184, 0.35);
    border-radius: 14px;
    height: 58px;
    color: white;
    font-size: 18px;
}

.stButton button {
    height: 58px;
    border-radius: 14px;
    border: none;
    font-size: 19px;
    font-weight: 800;
    color: white;
    background: linear-gradient(90deg, #a855f7, #2563eb, #06b6d4);
    box-shadow: 0 0 25px rgba(6, 182, 212, 0.35);
}

.stButton button:hover {
    transform: scale(1.01);
    box-shadow: 0 0 35px rgba(168, 85, 247, 0.55);
}

.feature-card {
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.20);
    border-radius: 22px;
    padding: 28px;
    min-height: 180px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.feature-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 10px;
}

.feature-text {
    color: #cbd5e1;
    font-size: 15px;
}

.info-box {
    background: rgba(30, 41, 59, 0.60);
    border: 1px solid rgba(14, 165, 233, 0.35);
    border-radius: 22px;
    padding: 25px;
    margin-top: 30px;
}

.safe-box {
    background: rgba(22, 163, 74, 0.18);
    border: 1px solid #22c55e;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    font-size: 24px;
    font-weight: 800;
}

.danger-box {
    background: rgba(220, 38, 38, 0.18);
    border: 1px solid #ef4444;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    font-size: 24px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="icon">🛡️</div>
    <div class="title">Phishing <span class="gradient-text">URL Detector</span></div>
    <div class="subtitle">Sistema inteligente para analizar URLs sospechosas usando Machine Learning</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-label">🔗 Ingresa una URL para analizar</div>', unsafe_allow_html=True)

url = st.text_input(
    label="URL",
    placeholder="Ejemplo: https://google.com",
    label_visibility="collapsed"
)

analizar = st.button("🔍 Analizar URL", use_container_width=True)

st.write("")
st.write("")

cols = st.columns(4)

cards = [
    ("🛡️", "Protección Inteligente", "Detecta patrones sospechosos en URLs."),
    ("📈", "Análisis Rápido", "Obtén resultados instantáneos del modelo."),
    ("🎯", "Alta Precisión", "Modelo entrenado para identificar amenazas."),
    ("🔐", "Seguridad Primero", "Analiza antes de hacer clic.")
]

for col, card in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{card[0]}</div>
            <div class="feature-title">{card[1]}</div>
            <div class="feature-text">{card[2]}</div>
        </div>
        """, unsafe_allow_html=True)

if analizar:
    st.write("")
    if url.strip() == "":
        st.warning("Ingresa una URL válida.")
    else:
        features = extract_features(url)
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]

        if prediction == 1:
            st.markdown('<div class="danger-box">⚠️ Posible URL de phishing</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="safe-box">✅ URL probablemente segura</div>', unsafe_allow_html=True)

        st.metric("Probabilidad de phishing", f"{probability * 100:.2f}%")
        st.progress(float(probability))

        with st.expander("Ver detalles técnicos"):
            feature_names = [
                "Longitud de URL",
                "Cantidad de puntos",
                "Cantidad de guiones",
                "Cantidad de @",
                "Cantidad de ?",
                "Cantidad de =",
                "Cantidad de %",
                "Cantidad de números",
                "Usa HTTPS",
                "Usa IP",
                "Longitud del dominio",
                "Palabras sospechosas"
            ]

            df_features = pd.DataFrame({
                "Característica": feature_names,
                "Valor": features
            })

            st.dataframe(df_features, use_container_width=True)

st.markdown("""
<div class="info-box">
    <b>ℹ️ Importante</b><br>
    Esta herramienta analiza la estructura de la URL y no realiza navegación real.
    Los resultados son referenciales.
</div>
""", unsafe_allow_html=True)