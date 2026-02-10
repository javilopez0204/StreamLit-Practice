import streamlit as st
import time
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview import vision_models # Para modelos de imagen/video

# 1. Usar la librería de Vertex AI directamente es más seguro para Veo
import vertexai
from vertexai.preview.vision_models import VideoGenerationModel

# Configuración de página
st.set_page_config(page_title="PokeVeo Creator", page_icon="🐉")

st.title("🐉 PokéVeo: Entrenador de Video AI")

# --- Inicialización ---
PROJECT_ID = "TU_PROYECTO_ID" 
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Cargar el modelo de Veo
# El ID del modelo suele ser 'veo-001' (verifica disponibilidad en tu consola)
try:
    model = VideoGenerationModel.from_pretrained("veo-001")
except Exception as e:
    st.error(f"Error cargando el modelo: {e}")

# --- Gestión de Historial ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "video_path" in message:
            st.video(message["video_path"])

# --- Input del Usuario ---
if prompt := st.chat_input("Pide tu video de Pokémon..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("🎬 Google Veo está creando tu animación... (esto puede tardar)"):
                # En la SDK de Vertex, el método es generate_video
                job = model.generate_video(
                    prompt=f"Cinematic pokemon animation, high quality, 4k: {prompt}",
                    # Opcional: negative_prompt="blurry, low resolution",
                    # Opcional: fps=24
                )
                
                # Veo genera un archivo de salida
                output_file = "pokemon_generated.mp4"
                job.save(output_file)
            
            message_placeholder.markdown("¡Aquí tienes tu video Pokémon!")
            st.video(output_file)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "¡Video generado!", 
                "video_path": output_file
            })

        except Exception as e:
            st.error(f"Error detallado: {e}")