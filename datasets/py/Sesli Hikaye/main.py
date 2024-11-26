#main.py

from download_audio import download_audio_from_youtube
from split import splitAudio
from google_sr import recognize_speech_from_files_in_audios

if __name__ == "__main__":
   url = input("Lütfen youtube dosyasının linkini sağlayın: ")
   path = download_audio_from_youtube(url)
   splitAudio(path)
   recognize_speech_from_files_in_audios()
   
   
   
   