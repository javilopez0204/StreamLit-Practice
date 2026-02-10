import streamlit as st
from google import genai
import time

# Configuración de la página
st.set_page_config(page_title="PokéVideo Creator", page_icon="⚡")
st.title("⚡ PokéVideo Creator AI")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    

if api_key:
    # Inicializamos el cliente
    client = genai.Client(api_key=api_key)
    
    user_prompt = st.text_area(
        "Describe la escena Pokémon:",
        placeholder="Ejemplo: Un Charizard volando sobre un volcán en estilo anime."
    )

    if st.button("¡Lanzar Pokéball! (Generar Video)"):
        if user_prompt:
            with st.spinner("⏳ Rotom-PC procesando... Esto puede tomar hasta 2-3 minutos."):
                try:
                    # El método correcto para generación de video en el nuevo SDK 
                    # suele ser a través de .models.generate_content pero especificando
                    # el modelo Veo si tienes acceso, o usando la función dedicada:
                    
                    operation = client.models.generate_video(
                        model="veo-2",  # Verifica que tengas acceso a este modelo
                        prompt=user_prompt,
                    )

                    # Esperamos a que la operación termine
                    while not operation.done:
                        time.sleep(10)
                        operation = client.operations.get(operation.name)
                        st.write("Sigo trabajando en ello... 🔨")

                    # Mostramos el resultado
                    video_uri = operation.result.video.uri
                    st.subheader("¡Tu video está listo!")
                    st.video(video_uri)
                    st.balloons()

                except Exception as e:
                    # Si el error persiste, es probable que el modelo no esté disponible 
                    # en tu región o cuenta de API específica todavía.
                    st.error(f"❌ Error en la Pokédex: {e}")
                    st.info("Nota: La generación de video (Veo) está en despliegue gradual.")
        else:
            st.warning("Escribe una descripción primero.")
else:
    st.warning("Introduce tu API Key para comenzar.")