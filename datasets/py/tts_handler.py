from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google_tts import generate_speech

import os
import re


class TTSHandler(SimpleHTTPRequestHandler):
    def validate_params(self, query_components):
       if 'text' not in query_components:
           self.send_error(400, "Missing required parameter: text")
           return False
           
       format = query_components.get('format', ['wav'])[0]
       if format not in ['wav', 'mp3']:
           self.send_error(400, "Invalid format. Use wav or mp3")
           return False
           
       lang = query_components.get('lang', ['en'])[0]
       if not re.match(r'^[a-z]{2}$', lang):
           self.send_error(400, "Invalid language code. Use xx-XX format")
           return False
           
       return True

    def do_POST(self):
        if not self.path.startswith('/tts'):
            return
        
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8-sig')
    
        # Boundary'i bul
        boundary = self.headers['Content-Type'].split('=')[1]
    
        # Form verilerini parse et
        form = {}
        parts = body.split('--' + boundary)
        for part in parts:
            if 'Content-Disposition: form-data; name="' in part:
                # İsim ve değeri çıkar
                name = part.split('name="')[1].split('"')[0]
                value = part.split('\r\n\r\n')[1].split('\r\n')[0]
                form[name] = value

        text = form.get('text', '')
        lang = form.get('lang', 'en')
        audioformat = form.get('format', 'wav')
        
        if lang == "en":
            lang = "en-US"
            output_path = "../english/wavs"
            filename = self.get_unique_filename(output_path,"output",audioformat)
            csv_path = "../english"
            if not os.path.exists(csv_path):
                os.makedirs(csv_path)

        elif lang=="tr":
            lang = "tr-TR"
            output_path ="../turkish/wavs"
            filename = self.get_unique_filename(output_path,"output",audioformat)
            csv_path = "../turkish"
            if not os.path.exists(csv_path):
                os.makedirs(csv_path)
        else:
            output_path =".."
            filename = self.get_unique_filename(output_path,"output",audioformat)
            csv_path = ".."
        try:
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
               
    def get_unique_filename(self, base_path, base_name, extension):
       
       if not os.path.exists(base_path):
        os.makedirs(base_path)
       
       index = 0
       while True:
       # İlk dosya için index'siz isim
           if index == 0:
               filename = f"{base_name}"
               filenameWextension=f"{base_name}.{extension}"
           else:
               filename = f"{base_name}{index}"
               filenameWextension=f"{base_name}{index}.{extension}"
           
           full_path = os.path.join(base_path, filenameWextension)
       
           # Dosya yoksa bu ismi kullan
           if not os.path.exists(full_path):
               return filename
           
           # Varsa index'i artır
           index += 1