
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

api_key = "your_api_key"

api_url = "https://api.groq.com/openai/v1/chat/completions"


@app.route("/", methods=["GET", "POST"])
def home():

    reply = ""

    if request.method == "POST":

        message = request.form["message"]

        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {
                        "role": "system",
                        "content": """
                        You are an AI Recipe Generator and Cooking Assistant.

                        If the user provides ingredients:
                        - Suggest a suitable recipe.
                        - List the ingredients.
                        - Mention additional ingredients if needed.
                        - Give preparation time.
                        - Give cooking time.
                        - Give clear step-by-step cooking instructions.
                        - Give cooking tips.

                        If the user asks for a particular recipe:
                        - Give the ingredients.
                        - Give preparation time.
                        - Give cooking time.
                        - Give numbered cooking steps.
                        - Give useful cooking tips.

                        Keep everything simple and beginner-friendly.
                        Always format your answers clearly and professionally.

Rules:
- Use bullet points whenever explaining information.
- Use numbered lists for step-by-step instructions.
- Keep paragraphs short.
- Use headings when the answer has multiple sections.
- Highlight important words using bold texts.
- Avoid giving long blocks of plain text.
- Make answers easy to read and scan.
- If there are multiple points, separate them into bullet points.
- Give concise but useful answers.
                        """
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
        )

        if response.ok:

            data = response.json()

            reply = data["choices"][0]["message"]["content"]

        else:

            try:
                data = response.json()

                reply = data.get(
                    "error", {}
                ).get(
                    "message",
                    "Something went wrong."
                )

            except:
                reply = "Unable to connect to the AI service."

    return render_template("index.html", reply=reply)


if __name__ == "__main__":
    app.run(debug=True)

