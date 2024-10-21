import yt_dlp
import os
from pydub import AudioSegment
import speech_recognition as sr

# URL do vídeo do YouTube
video_url = "https://www.youtube.com/watch?v=Q267RF1I3GE"  # Substitua pelo ID do seu vídeo

# Opções para o yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'audio.%(ext)s',
}

# Baixar o vídeo e extrair o áudio
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Verifica se o arquivo MP3 foi criado
    audio_file_mp3 = 'audio.mp3'
    if os.path.exists(audio_file_mp3):
        # Converte MP3 para WAV
        wav_file = 'audio.wav'
        audio = AudioSegment.from_mp3(audio_file_mp3)
        audio.export(wav_file, format='wav')

except Exception as e:
    print(f"Ocorreu um erro ao baixar o vídeo: {e}")

# Cria um reconhecedor
recognizer = sr.Recognizer()

# Tenta reconhecer o áudio
try:
    if os.path.exists(wav_file):
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)  # lê o áudio

        texto = recognizer.recognize_google(audio_data, language='pt-BR')  # para português
        print("Texto reconhecido:", texto)
    else:
        print("Arquivo WAV não encontrado.")
except sr.UnknownValueError:
    print("O Google Speech Recognition não conseguiu entender o áudio.")
except sr.RequestError as e:
    print(f"Erro ao solicitar resultados do Google Speech Recognition; {e}")