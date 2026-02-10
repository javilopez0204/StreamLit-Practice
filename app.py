import streamlit as st
from google import genai
from google.genai import types
import time

# Configuración de página
st.set_page_config(page_title="PokeVeo Creator", page_icon="🐉")

st.title("🐉 PokéVeo: Entrenador de Video AI")
st.markdown("¡Hola! Soy tu asistente de IA. Pídeme que genere un video de cualquier Pokémon en una situación épica.")

# --- Inicialización del Cliente de Google Gen AI ---
# Asegúrate de tener la variable de entorno o estar autenticado
client = genai.Client(vertexai=True, project="TU_PROYECTO_ID", location="us-central1")

# --- Gestión de Historial de Chat ---
if "messages" not in st. session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "video_url" in message:
            st.video(message["video_url"])

# --- Input del Usuario ---
if prompt := st.chat_input("Ej: Un Charizard volando sobre un volcán activo en estilo cinemático"):
    
    # Añadir mensaje del usuario al chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del bot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Invocando a Veo para generar tu video Pokémon...*")
        
        try:
            # Llamada a Google Veo (Modelo 'veo-001' o similar según disponibilidad)
            # Nota: Veo suele requerir un proceso asíncrono o de espera
            operation = client.models.generate_video(
                model='veo-3.1-fast-generate-preview',
                prompt=f"A Pokémon video of: {prompt}, high quality, 4k, cinematic animation",
            )
            
            # Simulación de espera de procesamiento (Veo genera videos en segundos/minutos)
            with st.spinner("Generando frames..."):
                while not operation.done:
                    time.sleep(5)
            
            video_result = operation.result
            video_url = video_result.generated_samples[0].video.uri # Depende del formato de salida

            message_placeholder.markdown("¡Aquí tienes tu video Pokémon!")
            st.video(video_url)
            
            # Guardar en historial
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "¡Video generado con éxito!", 
                "video_url": video_url
            })

        except Exception as e:
            st.error(f"Hubo un error con Google Veo: {e}")