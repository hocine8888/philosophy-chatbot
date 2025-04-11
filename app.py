import openai
import os
from flask import Flask, request, jsonify

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

philosophers = {
    "Freud": "Tu es Freud. Tu parles de l’inconscient, des désirs refoulés et des conflits psychiques.",
    "Socrate": "Tu es Socrate. Tu utilises la maïeutique, tu poses des questions pour amener l'autre à réfléchir.",
    "Descartes": "Tu es Descartes. Tu utilises le doute méthodique pour chercher la vérité.",
    "Marx": "Tu es Marx. Tu parles de lutte des classes, d’idéologie et d'économie politique.",
    "Nietzsche": "Tu es Nietzsche. Tu parles de volonté de puissance, de dépassement de soi et de critique de la morale.",
    "Sartre": "Tu es Sartre. Tu parles de liberté absolue, de responsabilité, et de l’angoisse existentielle."
}

def get_openai_response(philosopher, question):
    style = philosophers.get(philosopher)
    if not style:
        return "Ce philosophe n'est pas disponible."

    prompt = f"{style}\nQuestion : {question}\nRéponse :"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question")
    philosopher = data.get("philosopher")
    if not question or not philosopher:
        return jsonify({"error": "question et philosopher requis"}), 400

    response = get_openai_response(philosopher, question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
