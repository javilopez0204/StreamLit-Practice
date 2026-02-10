import streamlit as st
from google import genai
from google.genai import types
import time

# --- Configuración de la Interfaz ---
st.set_page_config(page_title="PokéVeo Studio 2026", page_icon="🐉", layout="centered")

# Estilo personalizado para el chat
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .pokemon-title { color: #FFCB05; text-shadow: 2px 2px #3D7HAL; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🐉 PokéVeo: Entrenador de Video AI")
st.caption("Generador de cinemáticas Pokémon con Google Veo")

# --- Configuración de Cliente ---
# Nota: En Streamlit Cloud, añade PROJECT_ID a Settings > Secrets
PROJECT_ID = st.secrets.get("PROJECT_ID", "tu-proyecto-id") 
LOCATION = "us-central1"

client = genai.Client(
    vertexai=True, 
    project=PROJECT_ID, 
    location=LOCATION
)

# --- Lógica de Negocio ---
def validar_pokemon(prompt):
    """Usa Gemini para verificar si el prompt es sobre Pokémon."""
    check_prompt = f"El usuario quiere generar un video. ¿El siguiente texto trata sobre Pokémon? Responde solo 'S' o 'N': {prompt}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=check_prompt)
    return "S" in response.text.upper()

# --- Gestión de Historial ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderizar mensajes guardados
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "video_data" in message:
            st.video(message["video_data"])

# --- Chat Input ---
if prompt := st.chat_input("Ej: Un Mewtwo meditando en una cueva de cristal..."):
    
    # 1. Mostrar prompt del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Respuesta del Asistente
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        
        # Validación previa
        if not validar_pokemon(prompt):
            error_msg = "Lo siento, como experto en Pokémon, solo puedo generar videos relacionados con el mundo Pokémon. ¡Inténtalo de nuevo!"
            status_placeholder.warning(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            status_placeholder.info("✨ Analizando ADN Pokémon y conectando con Google Veo...")
            
            try:
                # Llamada a Veo (Generación asíncrona)
                # El modelo 'veo-001' es el estándar para producción en 2026
                operation = client.models.generate_video(
                    model='veo-001',
                    prompt=f"Cinematic 3D animation of {prompt}. Pokémon art style, high detail, 4k, smooth motion.",
                )
                
                with st.spinner("🎬 Generando cinemática... Esto puede tomar un minuto."):
                    # Esperar a que la operación termine
                    while not operation.done:
                        time.sleep(5)
                
                # Obtener resultado
                video_result = operation.result
                # Accedemos al primer video generado
                video_bytes = video_result.generated_samples[0].video.bytes
                
                status_placeholder.success("¡Video generado con éxito!")
                st.video(video_bytes)
                
                # Guardar en historial (guardamos bytes para que persista en la sesión)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Aquí tienes tu video de: {prompt}", 
                    "video_data": video_bytes
                })

            except Exception as e:
                st.error(f"Error técnico: {str(e)}")
                if "403" in str(e):
                    st.info("💡 Tip: Revisa si tu cuenta de Google Cloud tiene habilitada la cuota para 'Veo Video Generation'.")
