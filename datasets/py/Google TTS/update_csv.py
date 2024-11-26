import os

def write_to_csv(path, filename, text):
    """
    Her çağrıldığında bir satır yazar. Dosya mevcutsa ekleme (append) yapar,
    yoksa yeni bir dosya oluşturur.
    """
    csv_path = os.path.join(path, 'metadata.csv')

    try:
        # Satırı temizle ve hazırlık yap
        text = str(text).strip()
        filename = str(filename).strip()
        line = f"{filename}|{text}\n"

        # Dosyayı ekleme (append) ya da oluşturma (write) modunda aç
        with open(csv_path, mode='a', encoding='utf-8-sig', newline='') as file:
            file.write(line)  # Satırı yaz
            file.flush()  # Buffer'ı hemen temizle
    except Exception as e:
        print(f"Hata: {e}")
