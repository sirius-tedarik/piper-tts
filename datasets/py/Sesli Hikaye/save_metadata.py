import csv

def write_to_metadata(name, text):
    """
    Verilen name ve text değerini metadata.csv dosyasına yazar.
    
    Args:
    - name (str): Çıktı dosyasının adı (örneğin, 'output0', 'output1' vb.).
    - text (str): Speech recognition'dan elde edilen metin.
    """
    
    # CSV dosyasına yazmak için aç
    with open('metadata.csv', mode='a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Verileri CSV dosyasına yaz
        writer.writerow([name, text])

    print(f"{myname} dosyasının metni başarıyla kaydedildi.")
    
