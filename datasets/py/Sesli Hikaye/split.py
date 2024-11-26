from pydub import AudioSegment
import os


def convert_to_mono(input_file, output_file):
    # WAV dosyasını yükle
    audio = AudioSegment.from_file(input_file)
    
    # Stereo'dan Mono'ya dönüştür
    mono_audio = audio.set_channels(1)
    
    # Mono olarak dışa aktar
    mono_audio.export(output_file, format="wav")

    print("Bölme işlemi tamamlandı!")

def splitAudio(input_file):

    # Çıktı klasörü oluşturma (eğer yoksa)
    output_dir = "audios"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Wav dosyasını yükleme
    audio = AudioSegment.from_wav(input_file)

    # Ses dosyasının toplam uzunluğu
    duration_ms = len(audio)  # milisaniye cinsinden

    # 10 saniyelik parçalara bölme
    chunk_duration_ms = 10 * 1000  # 10 saniye = 10000 milisaniye
    chunks = []

    # Dosyayı 10 saniyelik parçalara ayırma
    for i, start_ms in enumerate(range(0, duration_ms, chunk_duration_ms)):
        end_ms = min(start_ms + chunk_duration_ms, duration_ms)
        chunk = audio[start_ms:end_ms]
    
        # Dosya ismini output, output1, output2 şeklinde yapma
        chunk_name = os.path.join(output_dir, f"output{i}.wav")
    
        # Parçayı kaydetme
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)
        print(f"Parça {chunk_name} olarak kaydedildi.")
        convert_to_mono(chunk_name,chunk_name)