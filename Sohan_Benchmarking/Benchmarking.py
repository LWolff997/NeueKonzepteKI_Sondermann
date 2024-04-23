from openai import OpenAI
import os
import time
from dotenv import load_dotenv
from termcolor import colored
import pandas as pd
import re  # Zum Extrahieren der Antwortnummern aus den Volltextantworten

# Load environment variables
load_dotenv()

# Retrieve the env variables
model = os.getenv('MODEL')
api_endpoint = os.getenv('API_ENDPOINT')

openai_api_base = api_endpoint + '/v1'

# FYI, a runpod api key only needs to be set if using serverless.
runpod_api_key = os.getenv('RUNPOD_API_KEY') if os.getenv('RUNPOD_API_KEY') is not None else "EMPTY"

# Initialize the OpenAI client
client = OpenAI(
    api_key=runpod_api_key,  # Replace with your actual API key if required
    base_url=openai_api_base,
)

def get_llm_answer(question, choices):
    messages = [
        {"role": "system", "content": "Dies ist eine Multiple-Choice-Frage. Bitte wähle die korrekte Antwort aus den folgenden Optionen und antworte bitte völlig ausschließlich mit der korrekten Antwortnummer (z.B. <Antwort xx.x>, nur ohne < > und mit den entsprechenden Zahlen anstatt dem x) und mit nichts weiterem. Gehe dabei sicher, dass deine Antwort unweigerlich und definitiv aus der richtigen Antwortzahl besteht und das Ergebnis dann am Ende 'Antwort xy.z' Format hat."},
        #{"role": "system", "content": "Dies ist eine Multiple-Choice-Frage. Bitte wähle die korrekte Antwort aus den folgenden Optionen und antworte bitte völlig ausschließlich mit der korrekten Antwortnummer (z.B. <Antwort xx.x>, nur ohne < > und mit den entsprechenden Zahlen anstatt dem x) und mit nichts weiterem. Gehe dabei sicher, dass deine Antwort unweigerlich und definitiv aus der richtigen Antwortzahl besteht und das Ergebnis dann am Ende 'Antwort xy.z' Format hat. Das ist unglaublich wichtig. Ich bitte dich wirklich: Habe immer neben der richtigen Antwortnummer auch 'Antwort' mit dabei, dass man das richtig erkennen kann. Und bitte bitte bitte generiere keine neuen Fragen nachdem du die aktuelle beantwortet hast, sondern beantworte IMMER nur die aktuelle Frage."},
        {"role": "user", "content": f"{question}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}"}
    ]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0, #must be strictly positive for the TGI openai endpoint.
            max_tokens=60
        )
        full_response = response.choices[0].message.content.strip()
        # Sucht nach dem Muster "Antwort xx.x" im Antworttext
        match = re.search(r'Antwort (\d+\.\d+)', full_response)
        if match:
            # Extrahiert die Antwortnummer aus dem Text
            answer_number = match.group(1)
            return answer_number, full_response
        else:
            return "0", full_response  # Wenn das Muster nicht gefunden wurde
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten bei der Frage: {question}")
        print(str(e))
        return "0", "Fehler: Antwort konnte nicht verarbeitet werden."

def process_questions(questions_file, answers_file):
    questions_df = pd.read_csv(questions_file)
    assert len(questions_df) == 100, "Die Anzahl der Fragen in der CSV-Datei entspricht nicht 100."
    
    answers_data = {'Index.Antwort': [], 'LLM_Vollständige_Antwort': []}
    
    for index, row in questions_df.iterrows():
        question = row['Frage']
        choices = [row['Antwort1'], row['Antwort2'], row['Antwort3'], row['Antwort4']]
        llm_answer, full_response = get_llm_answer(question, choices)
        answers_data['Index.Antwort'].append(llm_answer)
        answers_data['LLM_Vollständige_Antwort'].append(full_response)
    
    # Speichern der LLM-Antworten und der vollständigen Antworten in einer CSV-Datei
    answers_df = pd.DataFrame(answers_data)
    answers_df.to_csv('llm_answers.csv', index=False)
    
    with open(answers_file, 'r') as f:
        correct_answers = f.read().splitlines()

    correct_count = sum(1 for llm_a, correct_a in zip(answers_data['Index.Antwort'], correct_answers) if f"{llm_a.split('.')[0]}.{llm_a.split('.')[1]}" == correct_a)

    print(f"Das LLM hat {correct_count} von {len(correct_answers)} Fragen richtig beantwortet.")

# Ersetzen Sie 'Biotest-bereinigt.csv' und 'Antworten.txt' mit den entsprechenden Pfaden zu Ihren Dateien.
process_questions('Biotest-bereinigt.csv', 'Antworten.txt')
