import json
import openai

openai.api_key = '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'

def split_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def chatgpt(api_schluessel, konversation, chatbot_aufforderung, text_chunk, frage=None, temperatur=0.7, haeufigkeitsstrafe=0.0, praesenzstrafe=0.0):
    openai.api_key = api_schluessel
    konversation.append({"role": "system", "content": chatbot_aufforderung})
    konversation.append({"role": "user", "content": text_chunk})
    if frage:
        konversation.append({"role": "user", "content": frage})
    vollendung = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        temperature=temperatur,
        frequency_penalty=haeufigkeitsstrafe,
        presence_penalty=praesenzstrafe,
        messages=konversation
    )
    return vollendung.choices[0].message['content']

def generate_qa_pairs(text_chunk, api_key):
    chatbot_aufforderung1 = "Generiere eine Frage basierend auf dem folgenden Textabschnitt."
    chatbot_aufforderung2 = "Generiere eine Antwort basierend auf folgender Frage unter Berücksichtigung des folgenden Textabschnittes."
    frage = chatgpt(api_key, [], chatbot_aufforderung1, text_chunk)
    antwort = chatgpt(api_key, [], chatbot_aufforderung2, text_chunk, frage=frage)
    return frage, antwort

def process_book(file_path, api_key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        text_chunks = split_into_chunks(text)

        with open('qa_dataset.jsonl', 'w', encoding='utf-8') as output_file:
            for chunk in text_chunks:
                question, answer = generate_qa_pairs(chunk, api_key)
                if question and answer:
                    json_line = json.dumps({"Frage": question, "Antwort": answer})
                    output_file.write(json_line + '\n')
        print("Fragen und Antworten wurden erfolgreich generiert und als .jsonl gespeichert.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

process_book('Bio_Buch_wichtig.txt', openai.api_key)
