import PyPDF2

def extract_pages(pdf_path, output_path, start_page, end_page):
    # PDF-Dateien zählen Seiten ab 0, deshalb -1 für Start und Ende
    start_page -= 1
    end_page -= 1
    
    # PDF-Reader-Objekt erstellen
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        
        # PDF-Writer-Objekt erstellen
        writer = PyPDF2.PdfWriter()
        
        # Gewünschte Seiten hinzufügen
        for i in range(start_page, end_page + 1):
            # Überprüfen, ob die Seitennummer innerhalb des gültigen Bereichs ist
            if i < len(reader.pages):
                writer.add_page(reader.pages[i])
        
        # Ausgabedatei schreiben
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

# Pfad zur Quell-PDF
source_pdf = "Biologie.pdf"
# Pfad zur Ziel-PDF
target_pdf = "Biologie_extracted.pdf"
# Seitenbereich, der extrahiert werden soll
extract_pages(source_pdf, target_pdf, 20, 70)
