import streamlit as st
from datetime import datetime, timedelta

# Configuração da Página
st.set_page_config(page_title="CicloPrevisão - Planejador de Treino", page_icon="🚴")

st.title("🚴 CicloPrevisão")
st.subheader("Planeje seu treino com base no clima e performance")

# --- ENTRADA DE DADOS ---
with st.sidebar:
    st.header("Configurações do Pedal")
    origem = st.text_input("Endereço de Início", "Taubaté, SP")
    destino = st.text_input("Endereço de Destino", "Campos do Jordão, SP")
    
    distancia = st.number_input("Distância estimada (km)", min_value=1.0, value=45.0)
    v_media = st.number_input("Sua Velocidade Média (km/h)", min_value=5.0, value=25.0)
    
    hora_inicio = st.time_input("Horário de Início", datetime.now().time())

# --- LÓGICA DE CÁLCULO ---
# Tempo = Distância / Velocidade
tempo_total_horas = distancia / v_media
tempo_total_minutos = int(tempo_total_horas * 60)

# Cálculo dos Horários
inicio_dt = datetime.combine(datetime.today(), hora_inicio)
chegada_dt = inicio_dt + timedelta(minutes=tempo_total_minutos)
meio_dt = inicio_dt + timedelta(minutes=tempo_total_minutos // 2)

# --- EXIBIÇÃO DOS RESULTADOS ---
st.info(f"⏱️ **Duração Estimada:** {tempo_total_minutos} minutos ({tempo_total_horas:.2f}h)")

col1, col2, col3 = st.columns(3)
col1.metric("Partida", inicio_dt.strftime("%H:%M"))
col2.metric("Meio (Checkpoint)", meio_dt.strftime("%H:%M"))
col3.metric("Chegada", chegada_dt.strftime("%H:%M"))

st.divider()

# --- SIMULAÇÃO DE CRONOGRAMA DE PREVISÃO ---
st.write("### 🌤️ Cronograma de Previsão do Tempo")

# Aqui no futuro conectaremos com a API (OpenWeather)
# Por enquanto, mostramos como os dados aparecerão:
dados_simulados = [
    {"hora": inicio_dt.strftime("%H:%M"), "local": origem, "temp": "22°C", "condicao": "☀️ Limpo", "vento": "12 km/h SE"},
    {"hora": meio_dt.strftime("%H:%M"), "local": "Meio do Caminho", "temp": "25°C", "condicao": "⛅ Nublado", "vento": "15 km/h E"},
    {"hora": chegada_dt.strftime("%H:%M"), "local": destino, "temp": "18°C", "condicao": "🌧️ Chuva Leve", "vento": "8 km/h S"},
]

for ponto in dados_simulados:
    with st.expander(f"{ponto['hora']} - {ponto['local']}"):
        st.write(f"**Temperatura:** {ponto['temp']}")
        st.write(f"**Condição:** {ponto['condicao']}")
        st.write(f"**Vento:** {ponto['vento']}")

if "Chuva" in dados_simulados[-1]['condicao']:
    st.warning("⚠️ Atenção: Previsão de chuva para o horário da sua chegada!")
