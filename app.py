import streamlit as st
from google import genai
import time

# Configuración de la página al estilo Pokédex
st.set_page_config(page_title="PokéVideo Creator", page_icon="⚡")
st.title("⚡ PokéVideo Creator AI")
st.markdown("### ¡Transforma tus ideas en animaciones con el poder de un Rotom!")

# Sidebar para la API Key y configuración del modelo
with st.sidebar:
    st.header("Configuración de Entrenador")
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.info("Consigue tu llave en [Google AI Studio](https://aistudio.google.com/)")
    
    st.divider()
    st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png", width=100)

# Inicializar el Cliente de GenAI
if api_key:
    client = genai.Client(api_key=api_key)
    
    # Entrada del usuario: El "Ataque" o Prompt
    user_prompt = st.text_area(
        "Describe la escena que quieres generar:",
        placeholder="Ejemplo: Un Pikachu corriendo por un bosque eléctrico, estilo cinematográfico, 4k."
    )

    # Botón de acción
    if st.button("¡Yo te elijo! (Generar Video)"):
        if user_prompt:
            with st.spinner("⏳ Rotom-PC está procesando los frames... Esto puede tardar unos momentos."):
                try:
                    # Llamada al modelo de generación de video (Veo)
                    # Nota: Asegúrate de que el modelo 'veo-2' esté disponible en tu región/cuenta
                    operation = client.models.generate_video(
                        model="veo-2",
                        prompt=user_prompt,
                    )
                    
                    # El proceso de video es asíncrono
                    while operation.metadata.state == "PROCESSING":
                        time.sleep(5)
                        operation = client.operations.get(operation.name)
                    
                    if operation.result:
                        st.subheader("¡Video Generado con Éxito!")
                        # El resultado suele ser una URL o bytes de video
                        # st.video(operation.result.video.uri) # Si es por URI
                        # st.video(operation.result.video.bytes) # Si el SDK devuelve bytes
                        
                        # Dependiendo de la versión del SDK, aquí mostramos el resultado:
                        st.video(operation.result.output_file_path)
                        st.balloons()
                    
                except Exception as e:
                    st.error(f"¡Hubo un error en el combate!: {e}")
        else:
            st.warning("¡Necesitas darle una orden a tu Pokémon! Escribe un prompt.")
else:
    st.warning("⚠️ Por favor, ingresa tu API Key en el panel lateral para encender la Poké-máquina.")

# Decoración extra
st.markdown("---")
st.caption("Powered by Google Veo & Streamlit - Hazte con todos los frames.")