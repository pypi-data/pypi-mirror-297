# pdfFileCheck/check.py
import os

def check_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                print("The file is not a valid PDF.")
                return

            file_size = os.path.getsize(file_path)
            size_kb = file_size / 1024
            size_mb = size_kb / 1024

            print(f"File is a valid PDF.")
            print(f"Size: {size_kb:.2f} KB")
            print(f"Size: {size_mb:.2f} MB")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: pdfFileCheck <file_path>")
    else:
        check_pdf(sys.argv[1])