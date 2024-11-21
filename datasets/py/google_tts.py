import os

from google.cloud import texttospeech
from update_csv import write_to_csv

def generate_speech(text, filename, csv_path, lang='en-US', file_format='wav', output_path="output.wav", credentials_path='credentials.json'):
   # Kimlik doğrulama
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
   
   # Client oluştur
   client = texttospeech.TextToSpeechClient()
   
   # Input ayarları
   synthesis_input = texttospeech.SynthesisInput(text=text)
   
   # Ses ayarları
   voice = texttospeech.VoiceSelectionParams(
       language_code=lang,
       ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
   )
   
   # Audio config
   audio_config = texttospeech.AudioConfig(
       audio_encoding=texttospeech.AudioEncoding.LINEAR16,
       sample_rate_hertz=22050
   )
   
   # İsteği gönder
   response = client.synthesize_speech(
       input=synthesis_input,
       voice=voice,
       audio_config=audio_config
   )
   
   write_to_csv(csv_path, filename, text)
   # Dosyaya kaydet
   fullfilename = filename + "." + file_format
   output_file = os.path.join(output_path, fullfilename)
   with open(output_file, "wb") as out:
       out.write(response.audio_content)
   
   return output_file