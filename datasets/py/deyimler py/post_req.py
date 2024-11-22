import requests

def send_tts_request(text, lang='tr', format='wav'):
    url = 'http://localhost:8070/tts'
    
    # Parametreleri hazırlıyoruz
    data = {
        'text': text,
        'lang': lang,
        'format': format
    }
    
    # POST isteği gönderiyoruz
    try:
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print('İstek başarıyla gönderildi.')
        else:
            print(f'Hata oluştu, HTTP durumu: {response.status_code}')
    except Exception as e:
        print(f'Bir hata oluştu: {e}')