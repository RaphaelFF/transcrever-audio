import streamlit as st
import whisper
import google.generativeai as genai

GOOGLE_API_KEY = "minha_chave"
genai.configure(api_key=GOOGLE_API_KEY)

#esse whisper faz a transcrição do audio em texto sem usar a gemini, ou seja, de forma gratis.
modelo = whisper.load_model("tiny")


model = genai.GenerativeModel("gemini-1.5-flash")

def gerarResumo(audio_file):
    
    mime_type = None
    if audio_file.name.endswith(".mp3"):
        mime_type = "audio/mpeg"
    elif audio_file.name.endswith(".wav"):
        mime_type = "audio/wav"
    elif audio_file.name.endswith(".m4a"):
        mime_type = "audio/mp4"

    if mime_type is None:
        raise ValueError("Tipo MIME desconhecido")

    sample_audio = genai.upload_file(audio_file, mime_type=mime_type)

    response = model.generate_content(["faça um resumo desse audio file.", sample_audio])
   
    resumo = ""
    for chunk in response:
        resumo += chunk.text + "\n"

    return resumo

def trans(audio_file):
    mime_type = None
    if audio_file.name.endswith(".mp3"):
        mime_type = "audio/mpeg"
    elif audio_file.name.endswith(".wav"):
        mime_type = "audio/wav"
    elif audio_file.name.endswith(".m4a"):
        mime_type = "audio/mp4"

    if mime_type is None:
        raise ValueError("Tipo MIME desconhecido")

    sample_audio = genai.upload_file(audio_file, mime_type=mime_type)

    response = model.generate_content(["mostre apenas a string do valor text que fica no parts[{'text:'}] gerado como resposta desse audio file. Se tiver erros de portugues conserte.", sample_audio])
 
    transR = response

    return transR

def main():
    st.title("Transcrição e Resumo de Áudio")

    
    audio_file = st.file_uploader("Selecione o arquivo de áudio", type=["m4a", "mp3", "wav"])

    if audio_file is not None:
        transR = trans(audio_file)
        resumo = gerarResumo(audio_file)
        

    
        col1, col2 = st.columns(2)
        with col1:
            st.header("Transcrição")
            st.write(transR)
        # with col1:
        #     st.header("Transcrição")
        #     transcricao = modelo.transcribe(audio_file.name)
        #     st.write(transcricao["text"])
        with col2:
            st.header("Resumo")
            st.write(resumo)

if __name__ == "__main__":
    main()
    
    
    
#parei na parte onde eu preciso entender o porque da api gemini não ta transcrevendo o audio