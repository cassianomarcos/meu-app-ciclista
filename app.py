import streamlit as st
import googlemaps
import requests
from datetime import datetime, timedelta, time

# --- CONFIGURAÇÕES DE API ---
# Você precisará dessas duas chaves para o app ser 100% funcional
GOOGLE_MAPS_KEY = "SUA_CHAVE_GOOGLE_AQUI"
OPENWEATHER_KEY = "SUA_CHAVE_OPENWEATHER_AQUI"

gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY) if GOOGLE_MAPS_KEY != "SUA_CHAVE_GOOGLE_AQUI" else None

st.set_page_config(page_title="CicloPrevisão Ida e Volta", page_icon="🚴")

def buscar_clima(cidade):
    if OPENWEATHER_KEY == "SUA_CHAVE_OPENWEATHER_AQUI": return None
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={OPENWEATHER_KEY}&units=metric&lang=pt_br"
    try:
        r = requests.get(url).json()
        return {"temp": r['main']['temp'], "desc": r['weather'][0]['description'].capitalize(), "vento": r['wind']['speed'] * 3.6}
    except: return None

st.title("🚴 Planejador de Treino (Ida e Volta)")

# --- ENTRADA DE DADOS ---
with st.sidebar:
    st.header("Configurações")
    origem = st.text_input("📍 Ponto de Início", "Taubaté, SP")
    destino = st.text_input("🏁 Ponto de Retorno", "Campos do Jordão, SP")
    v_media = st.number_input("⚡ Velocidade Média (km/h)", min_value=1.0, value=25.0)
    hora_saida = st.time_input("⏰ Horário de Saída", value=time(8, 0), key="hr_saida")

# --- CONSULTA GOOGLE MAPS ---
distancia_total = 0
if gmaps:
    try:
        # Consulta a distância de ida no Google Maps (modo ciclismo)
        resultado = gmaps.distance_matrix(origem, destino, mode="bicycling")
        if resultado['rows'][0]['elements'][0]['status'] == "OK":
            distancia_ida_metros = resultado['rows'][0]['elements'][0]['distance']['value']
            distancia_ida_km = distancia_ida_metros / 1000
            distancia_total = distancia_ida_km * 2  # IDA E VOLTA
            st.success(f"🗺️ Distância detectada: {distancia_ida_km:.1f}km (Total Ida/Volta: {distancia_total:.1f}km)")
        else:
            st.error("Não foi possível calcular a rota entre esses endereços.")
    except Exception as e:
        st.error(f"Erro na API do Google: {e}")
else:
    st.warning("Insira a Google Maps API Key para calcular a distância automática.")
    distancia_total = st.number_input("Distância Manual Total (km)", value=90.0)

# --- CÁLCULOS DE CRONOGRAMA ---
if distancia_total > 0:
    tempo_total_h = distancia_total / v_media
    inicio_dt = datetime.combine(datetime.today(), hora_saida)
    chegada_dt = inicio_dt + timedelta(hours=tempo_total_h)
    meio_dt = inicio_dt + timedelta(hours=tempo_total_h / 2)

    st.markdown(f"""
    ### ⏱️ Cronograma Estimado
    * **Saída:** {inicio_dt.strftime('%H:%M')}
    * **Chegada no Retorno (Meio):** {meio_dt.strftime('%H:%M')}
    * **Fim do Treino (Volta):** {chegada_dt.strftime('%H:%M')}
    * **Duração Total:** {int(tempo_total_h * 60)} min
    """)

    st.divider()

    # --- CLIMA ---
    if st.button("Verificar Clima para o Percurso"):
        c_inicio = buscar_clima(origem)
        c_retorno = buscar_clima(destino)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Clima na Saída ({origem})**")
            if c_inicio:
                st.metric("Temp", f"{c_inicio['temp']}°C")
                st.write(f"💨 Vento: {c_inicio['vento']:.1f} km/h")
        with col2:
            st.write(f"**Clima no Retorno ({destino})**")
            if c_retorno:
                st.metric("Temp", f"{c_retorno['temp']}°C")
                st.write(f"💨 Vento: {c_retorno['vento']:.1f} km/h")
