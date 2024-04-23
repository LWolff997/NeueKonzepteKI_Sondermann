from docx import Document
import csv

# Pfad zur Word-Datei
doc_path = 'Biotest.docx'

# Die Word-Datei öffnen
doc = Document(doc_path)

# Die CSV-Datei wird im gleichen Verzeichnis mit dem Namen 'Biotest.csv' erstellt
csv_path = 'Biotest.csv'

# CSV-Datei öffnen und zum Schreiben bereit machen
with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Schreibe die Kopfzeile in die CSV-Datei
    csv_writer.writerow(['Frage', 'Antwort1', 'Antwort2', 'Antwort3', 'Antwort4'])
    
    # Initialisieren einer Liste, um die Fragen und Antworten zu sammeln
    qa_list = []
    
    # Gehe durch jeden Absatz in der Word-Datei
    for para in doc.paragraphs:
        # Füge den Text jedes Absatzes in die qa_list ein
        # Hier nehmen wir an, dass Fragen und Antworten durch eine neue Zeile getrennt sind
        if para.text.startswith('Frage') or para.text.startswith('Antwort'):
            qa_list.append(para.text)
            
            # Wenn es vier Antworten gesammelt hat, schreibe sie in die CSV-Datei
            if len(qa_list) == 5:
                # Schreibe die Frage und die vier Antworten in die CSV-Datei
                csv_writer.writerow(qa_list)
                # Setze die qa_list zurück, um die nächste Frage und die Antworten zu sammeln
                qa_list = []

# Prüfe, ob noch eine Frage ohne vier Antworten am Ende verblieben ist
if qa_list:
    # Fülle die fehlenden Antworten mit leeren Strings auf
    while len(qa_list) < 5:
        qa_list.append('')
    csv_writer.writerow(qa_list)
