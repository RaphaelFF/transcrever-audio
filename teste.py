import streamlit as st
import whisper
import google.generativeai as genai
import tempfile
import os

GOOGLE_API_KEY = "AIzaSyDhBxq0OSGCZ1M8t6xQoaZL3D1eKPS-sAU"
genai.configure(api_key=GOOGLE_API_KEY)


modelo = whisper.load_model("tiny")


model = genai.GenerativeModel("gemini-1.5-flash")


def gerarResumo(audio_file):
 
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, audio_file.name)
        with open(tmp_file, 'wb') as f:
            f.write(audio_file.getvalue())

        mime_type = None
        if audio_file.name.endswith(".mp3"):
            mime_type = "audio/mpeg"
        elif audio_file.name.endswith(".wav"):
            mime_type = "audio/wav"
        elif audio_file.name.endswith(".m4a"):
            mime_type = "audio/mp4"

        if mime_type is None:
            raise ValueError("Tipo MIME desconhecido")

 
        sample_audio = genai.upload_file(tmp_file, mime_type=mime_type)

        response = model.generate_content(["faça um resumo desse audio file.", sample_audio])
   
        resumo = ""
        for chunk in response:
            resumo += chunk.text + "\n"

        return resumo

def main():
    st.title("Transcrição e Resumo de Áudio")

    

    audio_file = st.file_uploader("Selecione o arquivo de áudio", type=["m4a", "mp3", "wav"]) 


    if audio_file is not None:
  
        resumo =gerarResumo(audio_file)

        #resumo = gerarResumo(audio_file)
        col1, col2 = st.columns(2)

        with col1:
            st.header("Transcrição")
            transcricao = modelo.transcribe(audio_file.name)
            st.write(transcricao["text"])
        with col2:
             st.header("Resumo")
             st.write(resumo)

if __name__ == "__main__":
    main()