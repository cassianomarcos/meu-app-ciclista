import streamlit as st
import requests
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO ---
API_KEY =  "28b242d7b3ec3a44102b94b2c8a35446" # Coloque sua chave entre as aspas

st.set_page_config(page_title="CicloPrevisão Real", page_icon="🚴")

def buscar_clima(cidade):
    # Busca coordenadas e depois o clima
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    response = requests.get(url).json()
    if response.get("cod") == 200:
        return {
            "temp": response['main']['temp'],
            "desc": response['weather'][0]['description'].capitalize(),
            "vento": response['wind']['speed'] * 3.6  # Converte m/s para km/h
        }
    return None

st.title("🚴 CicloPrevisão Real-Time")

# --- ENTRADA ---
with st.sidebar:
    origem = st.text_input("Cidade de Início", "Taubaté")
    destino = st.text_input("Cidade de Destino", "Campos do Jordão")
    distancia = st.number_input("Distância (km)", value=45.0)
    v_media = st.number_input("Velocidade Média (km/h)", value=25.0)
    hora_inicio = st.time_input("Início", datetime.now().time())

# --- CÁLCULOS ---
tempo_h = distancia / v_media
chegada_dt = datetime.combine(datetime.today(), hora_inicio) + timedelta(hours=tempo_h)

st.metric("Previsão de Chegada", chegada_dt.strftime("%H:%M"))

# --- BUSCA REAL ---
if st.button("Consultar Clima Agora"):
    clima_inicio = buscar_clima(origem)
    clima_fim = buscar_clima(destino)
    
    col1, col2 = st.columns(2)
    
    if clima_inicio:
        with col1:
            st.success(f"Partida: {origem}")
            st.write(f"🌡️ {clima_inicio['temp']}°C")
            st.write(f"☁️ {clima_inicio['desc']}")
            st.write(f"💨 Vento: {clima_inicio['vento']:.1f} km/h")
            
    if clima_fim:
        with col2:
            st.info(f"Chegada: {destino}")
            st.write(f"🌡️ {clima_fim['temp']}°C")
            st.write(f"☁️ {clima_fim['desc']}")
            st.write(f"💨 Vento: {clima_fim['vento']:.1f} km/h")
