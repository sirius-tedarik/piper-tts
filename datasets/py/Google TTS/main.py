# main.py
from http.server import HTTPServer
from tts_handler import TTSHandler  # tts_handler.py'da önceki kod olmalı

if __name__ == "__main__":
   server_address = ('', 8070)
   httpd = HTTPServer(server_address, TTSHandler)
   print("Server started http://localhost:8070")
   httpd.serve_forever()