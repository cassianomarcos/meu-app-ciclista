import streamlit as st
import requests
from datetime import datetime, timedelta, time

# --- 1. CONFIGURAÇÃO ---
# Substitua pela sua chave do OpenWeatherMap
API_KEY = "SUA_CHAVE_AQUI" 

st.set_page_config(page_title="CicloPrevisão Pro", page_icon="🚴")

def buscar_clima(cidade):
    if not API_KEY or API_KEY == "SUA_CHAVE_AQUI":
        return None
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={API_KEY}&units=metric&lang=pt_br"
    try:
        r = requests.get(url, timeout=5).json()
        if r.get("cod") == 200:
            return {"temp": r['main']['temp'], "desc": r['weather'][0]['description'].capitalize(), "vento": r['wind']['speed'] * 3.6}
    except:
        return None
    return None

st.title("🚴 Planejador de Treino")

# --- 2. ENTRADA DE DADOS ---
# Usando colunas para organizar melhor o layout
col_dados, col_tempo = st.columns(2)

with col_dados:
    origem = st.text_input("📍 Início (Cidade)", "Taubaté")
    destino = st.text_input("🏁 Destino (Cidade)", "Campos do Jordão")
    distancia = st.number_input("📏 Distância (km)", min_value=1.0, value=45.0)

with col_tempo:
    v_media = st.number_input("⚡ Vel. Média (km/h)", min_value=1.0, value=25.0)
    
    # CORREÇÃO DO HORÁRIO: Usando um valor padrão de objeto 'time' e uma 'key'
    # Se o erro persistir no celular, tente clicar no ícone de relógio
    hora_saida = st.time_input(
        "⏰ Horário de Saída", 
        value=time(8, 0), # Começa às 08:00 por padrão
        key="horario_pedal"
    )

# --- 3. CÁLCULOS ---
try:
    tempo_total_h = distancia / v_media
    minutos_totais = int(tempo_total_h * 60)
    
    # Criando o objeto de data/hora para o cálculo
    inicio_dt = datetime.combine(datetime.today(), hora_saida)
    chegada_dt = inicio_dt + timedelta(minutes=minutos_totais)
    
    st.success(f"✅ **Resumo:** Partida às **{inicio_dt.strftime('%H:%M')}** | Chegada prevista: **{chegada_dt.strftime('%H:%M')}**")
    st.info(f"⏱️ Tempo total de pedal: **{minutos_totais} minutos**")
except Exception as e:
    st.error("Erro ao calcular tempo. Verifique a velocidade.")

st.divider()

# --- 4. CLIMA REAL ---
if st.button("🔄 Atualizar Previsão do Tempo"):
    with st.spinner("Buscando clima atual..."):
        c_origem = buscar_clima(origem)
        c_destino = buscar_clima(destino)
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f"**Partida: {origem}**")
            if c_origem:
                st.metric("Temp", f"{c_origem['temp']}°C")
                st.caption(f"{c_origem['desc']} | Vento: {c_origem['vento']:.1f} km/h")
            else:
                st.warning("Verifique a API Key")

        with c2:
            st.markdown(f"**Chegada: {destino}**")
            if c_destino:
                st.metric("Temp", f"{c_destino['temp']}°C")
                st.caption(f"{c_destino['desc']} | Vento: {c_destino['vento']:.1f} km/h")
            else:
                st.write("Dados indisponíveis")
