from docx import Document
from post_req import send_tts_request
import time

def extract_sentences_from_docx(docx_path):
    # DOCX dosyasını aç
    doc = Document(docx_path)
    sentences = []

    # DOCX içerisindeki her paragrafı al
    for para in doc.paragraphs:
        # Paragraflarda boşluk olmayan metinleri al
        if para.text.strip():
            sentences.append(para.text.strip())

    return sentences

# Kullanım
docx_path = "deneme.docx"
sentences = extract_sentences_from_docx(docx_path)

# Sonuçları yazdır ve TTS için gönder
for sentence in sentences:
    # İhtiyaç duyuluyorsa, cümledeki özel karakterleri veya numaraları temizleyebilirsiniz
    result = sentence
    send_tts_request(result)
    time.sleep(0.05)
