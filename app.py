from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # セッション用の秘密鍵（本番では固定値に）

# 100問の質問データを自動生成
questions = []
question_texts = [
    ("遺跡で謎を解くとき、あなたは？", ("A", "ひらめきで突破する"), ("B", "論理的に順序立てて考える")),
    ("魔法の試験を受けるとき、あなたの準備方法は？", ("A", "一夜漬けで直感を頼る"), ("B", "計画的に練習する")),
    ("仲間との冒険で、あなたの役割は？", ("A", "先陣を切って突き進む"), ("B", "後方から冷静にサポート")),
    ("古代の魔導書を読むとき、あなたは？", ("A", "全体像から読み解く"), ("B", "細部を丁寧に理解する"))
]
for i in range(100):
    base = question_texts[i % len(question_texts)]
    questions.append({
        "id": i + 1,
        "text": f"Q{i+1}: {base[0]}",
        "options": [base[1], base[2]]
    })

def calculate_mbti(responses):
    counts = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for qid, answer in responses.items():
        if int(qid) % 4 == 0:
            counts["E"] += answer == "A"
            counts["I"] += answer == "B"
        elif int(qid) % 4 == 1:
            counts["S"] += answer == "B"
            counts["N"] += answer == "A"
        elif int(qid) % 4 == 2:
            counts["T"] += answer == "B"
            counts["F"] += answer == "A"
        elif int(qid) % 4 == 3:
            counts["J"] += answer == "B"
            counts["P"] += answer == "A"

    mbti = ""
    mbti += "E" if counts["E"] >= counts["I"] else "I"
    mbti += "S" if counts["S"] >= counts["N"] else "N"
    mbti += "T" if counts["T"] >= counts["F"] else "F"
    mbti += "J" if counts["J"] >= counts["P"] else "P"
    return mbti

@app.route("/")
def index():
    session.clear()  # 新規セッションスタートで回答リセット
    return render_template("index.html")

@app.route("/quiz/<int:qid>", methods=["GET", "POST"])
def quiz(qid):
    if "responses" not in session:
        session["responses"] = {}

    if request.method == "POST":
        answer = request.form.get("answer")
        responses = session["responses"]
        responses[str(qid)] = answer
        session["responses"] = responses

        if qid < len(questions):
            return redirect(url_for("quiz", qid=qid+1))
        else:
            return redirect(url_for("result"))

    question = questions[qid - 1]
    return render_template("quiz.html", question=question)

@app.route("/result")
def result():
    responses = session.get("responses", {})
    mbti = calculate_mbti(responses)
    return render_template("result.html", mbti=mbti)

# Flask CLIで起動する想定なので app.run() はなし
if __name__ == "__main__":
    print("Flaskアプリの起動は、flask run を使ってください。例: FLASK_APP=app.py flask run")

