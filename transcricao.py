import re
import speech_recognition as sr
from moviepy import VideoFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks

def extrair_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def converter_para_wav(audio_path, wav_path):
    audio = AudioSegment.from_file(audio_path)
    audio.export(wav_path, format="wav")

def transcrever_audio_com_timestamps(wav_path, chunk_length_ms=30000):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(wav_path)
    chunks = make_chunks(audio, chunk_length_ms)
    texto_completo = ""
    timestamp_formatado = lambda ms: f"{int(ms / 60000)}:{int((ms % 60000) / 1000):02}"

    for i, chunk in enumerate(chunks):
        chunk_wav_path = f"chunk{i}.wav"
        chunk.export(chunk_wav_path, format="wav")
        with sr.AudioFile(chunk_wav_path) as source:
            audio_chunk = recognizer.record(source)
        
        try:
            texto = recognizer.recognize_google(audio_chunk, language="pt-BR")
            timestamp = timestamp_formatado(chunk_length_ms * i)
            texto_completo += f"[{timestamp}] {texto}\n\n"
        except sr.RequestError as e:
            timestamp = timestamp_formatado(chunk_length_ms * i)
            texto_completo += f"[{timestamp}] Erro de rede ou serviço: {e}\n\n"
        except sr.UnknownValueError:
            timestamp = timestamp_formatado(chunk_length_ms * i)
            texto_completo += f"[{timestamp}] Não foi possível entender o áudio\n\n"

    return texto_completo

# Exemplo de uso
video_path = "seu_video.mp4"
audio_path = "audio_extraido.mp3"
wav_path = "audio_extraido.wav"

extrair_audio(video_path, audio_path)
converter_para_wav(audio_path, wav_path)
texto_transcrito = transcrever_audio_com_timestamps(wav_path)

with open('transcricao_formatada_com_timestamps.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write(texto_transcrito)

print("Transcrição formatada com timestamps salva em 'transcricao_formatada_com_timestamps.txt'")
