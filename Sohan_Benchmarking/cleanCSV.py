import csv

# Pfad zur bestehenden CSV-Datei
input_csv_path = 'Biotest.csv'

# Pfad zur bereinigten CSV-Datei
output_csv_path = 'Biotest-bereinigt.csv'

# CSV-Datei einlesen, Antworten in Anführungszeichen setzen und in neue Datei schreiben
with open(input_csv_path, mode='r', encoding='utf-8') as infile, open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)  # Alle Felder werden in Anführungszeichen gesetzt
    
    for row in reader:
        writer.writerow(row)

print(f"Bereinigte Daten wurden in '{output_csv_path}' gespeichert.")
