import streamlit as st
from clima import clima_atual
from previsao import previsao_5dias
from graficos import df_previsao_5dias, plot_temp_5dias, analises_5dias_graficos
from PIL import Image
import base64
from io import BytesIO

st.title("Clima Tempo")

API_key = st.secrets["OPENWEATHER_API_KEY"] 

cidade = st.text_input("Busque uma cidade:")

icone_path = "imagem/previsaoclima.png"
img = Image.open(icone_path)
buffered = BytesIO()
img.save(buffered, format="PNG")
img_b64 = base64.b64encode(buffered.getvalue()).decode()

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

desc = "–"
temp = "–"
vento_kmh = "–"

if st.button("Buscar clima") and cidade:
    resultado = clima_atual(cidade, API_key)
    if resultado:
        cidade, temp, vento_kmh, desc, lat, lon = resultado
        vento_kmh = f"{float(vento_kmh):.1f} km/h"
    else:
        st.warning("Não foi possível obter o clima desta cidade.")
        temp = vento_kmh = desc = "–"

# Container para responsividade
st.markdown('<div class="previsao-container">', unsafe_allow_html=True)

# Caixa principal
st.markdown(f"""
<div class="previsao-box">
    <div class="texto">
        <h1 style="margin:0; text-align:left; font-size:50px;">{cidade}</h1>
        <h3 style="margin:0;">Clima: {desc}</h3>
        <p style="margin:0;">Temp: {temp}°C</p>
        <p style="margin:0;">Vento: {vento_kmh}</p>
    </div>
    <img class="icon" src="data:image/png;base64,{img_b64}">
</div>
""", unsafe_allow_html=True)

# Caixas mini
if cidade and desc != "–":
    previsoes = previsao_5dias(cidade, API_key)
    if previsoes:
        previsoes_restantes = list(previsoes.items())[1:]
        for dia, info in previsoes_restantes[:5]:
            desc_dia = info["desc"]
            icone_path = "imagem/chuva_png.png" if "chuva" in desc_dia.lower() else "imagem/sol_e_nuvem.png"
            img = Image.open(icone_path)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()

            st.markdown(f"""
            <div class="previsao-box-mini">
                <img src="data:image/png;base64,{img_b64}" style="width:50px; height:50px; margin-right:10px;">
                <div class="texto">
                    <span>{dia}</span>
                    <span>{desc_dia}</span>
                    <span>Min: {info['temp_min']}°C | Max: {info['temp_max']}°C</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Fecha o container

# Gráficos
if cidade and desc != "–" and previsoes:
    df_grafico = df_previsao_5dias(dict(previsoes_restantes), cidade)
    fig_temp = plot_temp_5dias(df_grafico)
    st.plotly_chart(fig_temp)

    st.subheader("Análises dos próximos 5 dias")
    figs_analises = analises_5dias_graficos(df_grafico)
    for f in figs_analises:
        st.plotly_chart(f)
