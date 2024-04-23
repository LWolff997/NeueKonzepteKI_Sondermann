import PyPDF2
import os

def pdf_to_text(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text = page.extract_text() if page.extract_text() else ""
            text += extracted_text
    
    # Verwendung von encoding='utf-8' und errors='ignore' beim Schreiben der Datei
    with open(txt_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(text)

def main():
    summary = []
    paths_to_check = ['data/train.pdf', 'data/test.pdf']
    
    for pdf_path in paths_to_check:
        # Extrahiere den Basisnamen, um den TXT-Dateinamen zu erstellen
        base_name = os.path.basename(pdf_path).split('.')[0]
        txt_path = f'data/raw_{base_name}.txt'
        
        # Überprüfe, ob die PDF existiert
        if os.path.exists(pdf_path):
            pdf_to_text(pdf_path, txt_path)
            summary.append(f"Converted {pdf_path} to {txt_path}.")
        else:
            summary.append(f"{pdf_path} was not found.")
    
    # Drucke Zusammenfassung
    print("Summary:")
    for item in summary:
        print(f"- {item}")

if __name__ == "__main__":
    main()