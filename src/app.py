from flask import Flask, redirect, render_template, request, session
from services import quiz

app: Flask = Flask(
    __name__,
    template_folder="../client/templates",
    static_folder="../client/static",
)
app.secret_key = "yes"


@app.route("/")
def index():
    print(session.get("quiz"))
    return render_template("home.html")


@app.route("/quiz", methods=["GET"])
def quiz_view():
    session["quiz"] = []
    session["task"] = quiz.get_task()
    return render_template("quiz.html", task=session["task"].task)


@app.route("/quiz", methods=["POST"])
def quiz_process():
    try:
        answer = request.form.get("answer") or ""
        action = request.form.get("action") or ""
        assert action in {"next", "finish"}
        session["task"]["user_answer"] = int(answer)
        session["quiz"].append(session["task"])
    except (ValueError, KeyError, AssertionError):
        return quiz_view()

    session["task"] = quiz.get_task()

    if action == "finish":
        return redirect("/results")
    return render_template("quiz.html", task=session["task"].task)


@app.route("/results", methods=["GET"])
def quiz_result_view():
    if "quiz" not in session or not session["quiz"]:
        return render_template("result.html", error="Quiz not found")
    return render_template(
        "result.html",
        quiz=session["quiz"],
        right=quiz.count_right_answers(session["quiz"]),
    )
