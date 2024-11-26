import os
import speech_recognition as sr
from google.cloud import speech
from save_metadata import write_to_metadata

# API anahtarının bulunduğu dosyayı belirtmek
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

# Google Cloud Speech-to-Text API kullanarak ses tanıma işlemi
def recognize_speech_from_files_in_audios(wav_file):

    # Google Cloud Speech API client oluşturuluyor
    client = speech.SpeechClient()

    wav_file_path = wav_file
    wav_file_name = wav_file_path.replace("audios\\","")
        
    # WAV dosyasını okuma
    with open(wav_file_path, 'rb') as audio_file:
        content = audio_file.read()

    # Google Cloud Speech API'ye gönderilecek ses dosyasının özelliklerini ayarlama
    audio = speech.RecognitionAudio(content=content)

    # Ses dosyasının özelliklerini ayarlama (WAV formatı, PCM kodlama)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=22050,
        language_code="tr-TR",
    )
    # Tanıma işlemi
    try:
        response = client.recognize(config=config, audio=audio)
        # Tanımlanan metni yazdırma
        for result in response.results:
            print(f"{wav_file_name} - Tanınan metin: {result.alternatives[0].transcript}")
            write_to_metadata(wav_file_name, result.alternatives[0].transcript)
    except Exception as e:
        print(f"{wav_file_name} - Google Cloud Speech API'ye bağlanırken hata oluştu: {e}")
