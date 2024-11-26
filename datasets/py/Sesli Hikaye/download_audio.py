import yt_dlp
import subprocess
import os

def download_audio_from_youtube(video_url):
    """
    Verilen YouTube video URL'sinden ses dosyasını indirir ve WAV formatında kaydeder.
    Args:
    - video_url (str): YouTube video URL'si.
    Returns:
    - str: Kaydedilen dosyanın ismi.
    """
    # yt-dlp seçenekleri
    ydl_opts = {
        'format': 'bestaudio/best',   # En yüksek ses kalitesinde dosyayı seç
        'outtmpl': 'audio_file.%(ext)s',  # Çıktı dosyasının ismi
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',  # Sesi çıkarmak için doğru post-processor
                'preferredcodec': 'wav',  # WAV formatına dönüştür
            }
        ],
    }

    # Ses indirme işlemi
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Kaydedilen dosyanın yolu
    audio_file_path = 'audio_file.wav'

    # Örnekleme hızını 22050 Hz'e dönüştür
    returnvalue = convert_sample_rate(audio_file_path)

    return returnvalue

def convert_sample_rate(audio_file):
    """
    WAV dosyasının örnekleme hızını 22050 Hz'e dönüştürür.
    Args:
    - audio_file (str): WAV dosyasının yolu.
    """
    print(f"{audio_file} dosyasını 22050 Hz'e dönüştürülüyor...")
    audio_file_22050 = 'audio_file22050.wav'
    # ffmpeg ile dosya örnekleme hızını dönüştür
    subprocess.run(['ffmpeg', '-i', audio_file, '-ar', '22050', audio_file_22050, '-y'])

    print(f"Dönüştürme tamamlandı: {audio_file}")
    os.remove(audio_file)
    return audio_file_22050
