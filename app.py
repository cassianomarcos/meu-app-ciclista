import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO (COLOQUE SUA CHAVE AQUI) ---
# Se ainda não tiver a chave, o app mostrará um aviso amigável.
API_KEY = "SUA_CHAVE_AQUI" 

st.set_page_config(page_title="Planejador de Pedal", page_icon="🚴")

# Função para buscar clima real
def buscar_clima(cidade):
    if API_KEY == "SUA_CHAVE_AQUI":
        return {"erro": "Falta a API Key"}
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={API_KEY}&units=metric&lang=pt_br"
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            return {
                "temp": response['main']['temp'],
                "desc": response['weather'][0]['description'].capitalize(),
                "vento": response['wind']['speed'] * 3.6
            }
    except:
        return None
    return None

st.title("🚴 Planejador de Treino: Taubaté e Região")

# --- 2. ENTRADA DE DADOS (CAMPOS SOLICITADOS) ---
st.markdown("### 📋 Dados do Treino")
col_a, col_b = st.columns(2)

with col_a:
    origem = st.text_input("Endereço/Cidade de Início", "Taubaté")
    destino = st.text_input("Endereço/Cidade de Destino", "Campos do Jordão")

with col_b:
    # Campo de Horário de Saída
    hora_saida = st.time_input("Horário de Início do Pedal", datetime.now().time())
    v_media = st.number_input("Velocidade Média (km/h)", min_value=1.0, value=25.0)

distancia = st.number_input("Distância Total Estimada (km)", min_value=1.0, value=45.0)

# --- 3. LÓGICA DE CRONOGRAMA ---
tempo_total_horas = distancia / v_media
hoje = datetime.today()
inicio_dt = datetime.combine(hoje, hora_saida)
chegada_dt = inicio_dt + timedelta(hours=tempo_total_horas)

st.divider()

# --- 4. EXIBIÇÃO DO CLIMA ---
st.markdown(f"### 🌤️ Previsão para o Percurso")

clima_origem = buscar_clima(origem)
clima_destino = buscar_clima(destino)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Partida ({inicio_dt.strftime('%H:%M')})")
    if clima_origem and "temp" in clima_origem:
        st.metric("Temperatura", f"{clima_origem['temp']}°C")
        st.write(f"**Condição:** {clima_origem['desc']}")
        st.write(f"**Vento:** {clima_origem['vento']:.1f} km/h")
    else:
        st.warning("Insira uma API Key válida para ver o clima real.")

with col2:
    st.subheader(f"Chegada ({chegada_dt.strftime('%H:%M')})")
    if clima_destino and "temp" in clima_destino:
        st.metric("Temperatura", f"{clima_destino['temp']}°C")
        st.write(f"**Condição:** {clima_destino['desc']}")
        st.write(f"**Vento:** {clima_destino['vento']:.1f} km/h")
    else:
        st.write("Aguardando dados...")

st.info(f"💡 **Resumo:** Seu pedal terá duração de **{tempo_total_horas:.2f}h**. Se sair às {inicio_dt.strftime('%H:%M')}, chegará por volta de **{chegada_dt.strftime('%H:%M')}**.")
