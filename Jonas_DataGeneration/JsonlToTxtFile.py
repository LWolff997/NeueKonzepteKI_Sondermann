import json

def jsonl_to_txt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Parse die JSON-Zeile
            data = json.loads(line)
            
            # Extrahiere Frage und Antwort, entferne dabei Zeilenumbrüche in der Antwort
            frage = data['Frage']
            antwort = data['Antwort'].replace('\n', ' ')
            
            # Schreibe die formatierte Frage und Antwort in die TXT-Datei
            outfile.write(f"{frage}\n{antwort}\n\n")

# Setze den Namen der Eingabe- und Ausgabedatei
input_file = 'test.jsonl'
output_file = 'test.txt'

# Führe die Konvertierung durch
jsonl_to_txt(input_file, output_file)

print(f"Die Konvertierung von {input_file} zu {output_file} wurde erfolgreich durchgeführt.")
