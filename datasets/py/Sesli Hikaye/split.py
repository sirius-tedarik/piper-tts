from pydub import AudioSegment
import os
from google_sr import recognize_speech_from_files_in_audios


def convert_to_mono(input_file, output_file):
    """
    WAV dosyasını stereo'dan mono'ya dönüştürür ve dışa aktarır.
    """
    # WAV dosyasını yükle
    audio = AudioSegment.from_file(input_file)
    
    # Stereo'dan Mono'ya dönüştür
    mono_audio = audio.set_channels(1)
    
    # Mono olarak dışa aktar
    mono_audio.export(output_file, format="wav")
    print(f"{output_file} mono olarak kaydedildi.")


def splitAudio(input_file):
    """
    WAV dosyasını 10 saniyelik parçalara böler ve mono'ya çevirir.
    Mevcut dosyaların devamına yeni numaralarla kaydeder.
    """
    # Çıktı klasörü oluşturma (eğer yoksa)
    output_dir = "audios"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Var olan dosyaları kontrol ederek en büyük numarayı bul
    existing_files = [f for f in os.listdir(output_dir) if f.startswith("output") and f.endswith(".wav")]
    existing_numbers = [
        int(f.replace("output", "").replace(".wav", ""))
        for f in existing_files
        if f.replace("output", "").replace(".wav", "").isdigit()
    ]
    next_index = max(existing_numbers, default=-1) + 1  # En büyük numaradan sonra başla

    # Wav dosyasını yükleme
    audio = AudioSegment.from_wav(input_file)

    # Ses dosyasının toplam uzunluğu
    duration_ms = len(audio)  # milisaniye cinsinden

    # 10 saniyelik parçalara bölme
    chunk_duration_ms = 10 * 1000  # 10 saniye = 10000 milisaniye

    # Dosyayı 10 saniyelik parçalara ayırma
    for start_ms in range(0, duration_ms, chunk_duration_ms):
        end_ms = min(start_ms + chunk_duration_ms, duration_ms)
        chunk = audio[start_ms:end_ms]
    
        # Dosya ismini outputX şeklinde oluştur (X: sıradaki numara)
        chunk_name = os.path.join(output_dir, f"output{next_index}.wav")
        next_index += 1  # Sıradaki numarayı artır
        
        # Parçayı kaydetme
        chunk.export(chunk_name, format="wav")
        print(f"Parça {chunk_name} olarak kaydedildi.")

        # Stereo'dan mono'ya çevirme
        convert_to_mono(chunk_name, chunk_name)

        # Ses dosyasından konuşma tanıma
        recognize_speech_from_files_in_audios(chunk_name)

    print("Tüm parçalar başarıyla işlendi!")
