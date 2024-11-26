from http.server import SimpleHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs
from google_tts import generate_speech


class TTSHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if not self.path.startswith('/tts'):
            return
        
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8-sig')
        
        # İçeriğin tipini kontrol et
        content_type = self.headers.get('Content-Type', '').lower()

        # JSON formatında gelen veri işleniyor
        if 'application/json' in content_type:
            try:
                json_data = json.loads(body)  # JSON verisini çözümle
                text = json_data.get('text', '')
                lang = json_data.get('lang', 'en')
                audioformat = json_data.get('format', 'wav')
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON format")
                return
        # Eğer form verisi varsa işleme al
        elif 'application/x-www-form-urlencoded' in content_type:
            form = parse_qs(body)
            text = form.get('text', [''])[0]
            lang = form.get('lang', ['en'])[0]
            audioformat = form.get('format', ['wav'])[0]
        # Multipart form verisi ile gelen data işleniyor
        elif 'multipart/form-data' in content_type:
            # Boundary'i bul ve veriyi parçala
            boundary = self.headers['Content-Type'].split('=')[1]
            form = self.parse_multipart_form_data(body, boundary)
            text = form.get('text', '')
            lang = form.get('lang', 'en')
            audioformat = form.get('format', 'wav')
        else:
            self.send_error(400, "Invalid Content-Type")
            return

        # Parametrelerin kontrolü
        if not text:
            self.send_error(400, "Missing required parameter: text")
            return

        if lang not in ['en', 'tr']:
            self.send_error(400, "Invalid language code. Use 'en' or 'tr'")
            return
        
        if audioformat not in ['wav', 'mp3']:
            self.send_error(400, "Invalid format. Use 'wav' or 'mp3'")
            return

        # Dil ve çıkış dosya yolu ayarları
        if lang == "en":
            lang = "en-US"
            output_path = "../../english/wavs"
            filename = self.get_unique_filename(output_path, "output", audioformat)
            csv_path = "../english"
        elif lang == "tr":
            lang = "tr-TR"
            output_path = "../../turkish/wavs"
            filename = self.get_unique_filename(output_path, "output", audioformat)
            csv_path = "../turkish"
        else:
            output_path = ".."
            filename = self.get_unique_filename(output_path, "output", audioformat)
            csv_path = ".."

        try:
            if 'application/json' in content_type:
                output_file = generate_speech(text, filename, csv_path, lang, audioformat, output_path)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            else:
                # Ses dosyasını oluştur
                output_file = generate_speech(text, filename, csv_path, lang, audioformat, output_path)
                self.send_response(200)
                self.send_header('Content-type', f'audio/{audioformat}')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Content-Disposition', f'inline; filename="output.{audioformat}"')
                self.end_headers()
                with open(output_file, 'rb') as f:
                    self.wfile.write(f.read())
        except Exception as e:
            self.send_error(500, str(e))

    def parse_multipart_form_data(self, body, boundary):
        """
        Multipart form verisini parse eder ve key-value dictionary olarak döner.
        """
        form = {}
        parts = body.split('--' + boundary)
        for part in parts:
            if 'Content-Disposition: form-data; name="' in part:
                name = part.split('name="')[1].split('"')[0]
                value = part.split('\r\n\r\n')[1].split('\r\n')[0]
                form[name] = value
        return form

    def get_unique_filename(self, base_path, base_name, extension):
        """
        Dosya ismi oluşturur ve çakışma varsa, index ekleyerek yeni bir isim verir.
        """
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        index = 0
        while True:
            # İlk dosya için index'siz isim
            if index == 0:
                filename = f"{base_name}"
                filenameWextension = f"{base_name}.{extension}"
            else:
                filename = f"{base_name}{index}"
                filenameWextension = f"{base_name}{index}.{extension}"
            
            full_path = os.path.join(base_path, filenameWextension)
            
            # Dosya yoksa bu ismi kullan
            if not os.path.exists(full_path):
                return filename
            
            # Varsa index'i artır
            index += 1
