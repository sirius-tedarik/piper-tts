import csv
import os

def write_to_csv(path, filename, text):
    csv_path = os.path.join(path, 'metadata.csv')
    file_exists = os.path.exists(csv_path)

    # Text'i UTF-8'e çevir
    line = (filename + "|" + text + "\n").encode('utf-8')
    
    try:
        if file_exists:
            # Append binary mode
            with open(csv_path, 'ab') as file:
                file.write(line)
        else:
            # Write binary mode with BOM
            with open(csv_path, 'wb') as file:
                file.write(b'\xef\xbb\xbf')  # UTF-8 BOM
                file.write(line)
                
    except Exception as e:
        print(f"Debug - Exception:", str(e))
        raise e