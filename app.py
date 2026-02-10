import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="Conchita AI", page_icon="🐚")
st.title("🐚 Conchita AI Assistant")

# Sidebar for API Key
with st.sidebar:
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.info("Get your key at [Google AI Studio](https://aistudio.google.com/)")

# Initialize the Gemini Client
if api_key:
    client = genai.Client(api_key=api_key)
    
    # User Input
    user_query = st.text_input("How can Conchita help you today?")

    if st.button("Ask Conchita"):
        if user_query:
            with st.spinner("Conchita is thinking..."):
                try:
                    # Call Gemini 2.5 Flash
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=user_query
                    )
                    
                    # Display Results
                    st.subheader("Response:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a question first!")
else:
    st.warning("Please enter your API Key in the sidebar to start.")