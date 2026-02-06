from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# 🔑 Put your Gemini API key here
genai.configure(api_key="AIzaSyD6pWZ5pZ5pZ5pZ5pZ5pZ5pZ5pZ5pZ5pZ5")

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form["subject"]
        level = request.form["level"]
        duration = request.form["duration"]
        goal = request.form["goal"]

        prompt = f"""
        You are an expert curriculum designer.

        Create a detailed {duration} curriculum for {level} level students on the subject "{subject}".
        Goal: {goal}.

        Include:
        1. Course overview
        2. Week-wise plan
        3. Topics per week
        4. Learning objectives
        5. Assessment plan

        Format it clearly with headings.
        """

        response = model.generate_content(prompt)
        curriculum = response.text

        return render_template("result.html", result=curriculum)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
