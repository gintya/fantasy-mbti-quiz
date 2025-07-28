from flask import Flask, render_template, request

import random

app = Flask(__name__)

# 質問（MBTIに基づくが、意図がばれにくいよう工夫・シャッフル）
questions_20 = [
    {"id": 1, "text": "街道で珍しい露店を見かけたら？", "options": ["S", "N"], "labels": ["商品の素材を確かめる", "全体の雰囲気から惹かれる"]},
    {"id": 2, "text": "森で道を見失ったとき？", "options": ["T", "F"], "labels": ["冷静に地図を確認する", "一緒にいる人の不安を和らげる"]},
    {"id": 3, "text": "魔法の呪文を学ぶなら？", "options": ["J", "P"], "labels": ["体系立てて学びたい", "試しながら覚えたい"]},
    {"id": 4, "text": "塔の最上階に誰かがいる気がしたら？", "options": ["N", "S"], "labels": ["直感を信じて向かう", "気のせいかもと周囲を見る"]},
    {"id": 5, "text": "大広間での集いに呼ばれたら？", "options": ["I", "E"], "labels": ["静かに過ごしたい", "色んな人と話したい"]},
    {"id": 6, "text": "騎士団の訓練を見て思うことは？", "options": ["F", "T"], "labels": ["皆つらそうで大変そう…", "効率的な訓練だ"]},
    {"id": 7, "text": "仲間と目的地が食い違った時？", "options": ["P", "J"], "labels": ["柔軟に変更に応じる", "計画を守ろうと説得する"]},
    {"id": 8, "text": "初めてのダンジョンに挑むとき？", "options": ["J", "P"], "labels": ["事前準備は万全に", "その場の流れで対応"]},
    {"id": 9, "text": "旅の途中、突然の雨が降ったら？", "options": ["N", "S"], "labels": ["空の色で予兆を感じてた", "そういえば雲が出てた"]},
    {"id": 10, "text": "王宮での伝令役を任されたら？", "options": ["E", "I"], "labels": ["臆せずこなす", "慎重に丁寧にこなす"]},
    {"id": 11, "text": "魔法試験の採点基準を見て？", "options": ["T", "F"], "labels": ["公平で理にかなってるか", "受験者の努力が報われているか"]},
    {"id": 12, "text": "古城で何かの気配を感じたら？", "options": ["S", "N"], "labels": ["風や音の変化を探る", "直感で方角を見定める"]},
    {"id": 13, "text": "宴の準備を任されたら？", "options": ["J", "P"], "labels": ["段取りを決めて動く", "その場の空気で調整"]},
    {"id": 14, "text": "仲間の一人が悩んでいる時？", "options": ["F", "T"], "labels": ["気持ちに寄り添う", "状況を分析して助言"]},
    {"id": 15, "text": "大通りで芸人の芸を見た時？", "options": ["E", "I"], "labels": ["拍手で盛り上げる", "静かに見守る"]},
    {"id": 16, "text": "古文書の読み解き方は？", "options": ["S", "N"], "labels": ["一文ずつ丁寧に", "全体像から理解"]},
    {"id": 17, "text": "敵国との交渉役に任命されたら？", "options": ["T", "F"], "labels": ["理詰めで対話する", "相手の感情も考慮"]},
    {"id": 18, "text": "市場で迷った時は？", "options": ["P", "J"], "labels": ["面白そうな方に進む", "目的の品を探す"]},
    {"id": 19, "text": "戦闘訓練に参加するなら？", "options": ["I", "E"], "labels": ["個別に集中練習", "みんなと実践訓練"]},
    {"id": 20, "text": "高名な魔術師に会えるとしたら？", "options": ["N", "S"], "labels": ["何を教えてくれるか想像する", "まずは人となりを観察"]}
]

random.shuffle(questions_20)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz_20.html", questions=questions_20)

@app.route("/result", methods=["POST"])
def result():
    answers = request.form
    result_score = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for key, value in answers.items():
        if value in result_score:
            result_score[value] += 1

    mbti = ""
    mbti += "E" if result_score["E"] >= result_score["I"] else "I"
    mbti += "S" if result_score["S"] >= result_score["N"] else "N"
    mbti += "T" if result_score["T"] >= result_score["F"] else "F"
    mbti += "J" if result_score["J"] >= result_score["P"] else "P"

    return render_template("result.html", result=mbti)

if __name__ == "__main__":
    app.run(debug=True)
