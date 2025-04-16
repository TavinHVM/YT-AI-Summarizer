from flask import Flask, render_template, request
from summarizer import summarize_video

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    error = ""
    if request.method == "POST":
        url = request.form.get("url")
        try:
            summary = summarize_video(url)
        except Exception as e:
            error = f"Erro ao processar: {str(e)}"
    return render_template("index.html", summary=summary, error=error)

if __name__ == "__main__":
    app.run(debug=True)
