from flask import Flask, render_template_string, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Bulls and Cows (幾A幾B)</title></head>
<body>
    <h1>4 數字猜幾 A 幾 B</h1>
    <p>{{ message }}</p>
    <form method="POST">
        <input type="text" name="guess" maxlength="4" pattern="\d{4}" placeholder="例如 1234" required>
        <button type="submit">送出</button>
    </form>
    <br>
    <a href="./reset">重新開始</a>
    <hr>
    <small>目前運行的 Pod 名稱: {{ pod_name }}</small>
</body>
</html>
"""

def generate_target():
    return "".join(random.sample("0123456789", 4))

@app.route("/healthz")
def healthz():
    return "OK", 200

@app.route("/", methods=["GET", "POST"])
def index():
    if "target_bc" not in session:
        session["target_bc"] = generate_target()
        session["message_bc"] = "遊戲開始！請輸入 4 個不重複的數字。"

    pod_name = os.getenv("HOSTNAME", "Local Environment")
    
    if request.method == "POST":
        guess = request.form.get("guess")
        target = session["target_bc"]
        
        if len(set(guess)) != 4:
            session["message_bc"] = "請輸入 4 個不重複的數字！"
        else:
            a = sum(1 for t, g in zip(target, guess) if t == g)
            b = len(set(target) & set(guess)) - a
            if a == 4:
                session["message_bc"] = f"恭喜猜中了！答案就是 {target}。"
                session.pop("target_bc")
            else:
                session["message_bc"] = f"你的輸入 {guess}: 結果為 {a}A{b}B"

    return render_template_string(HTML_TEMPLATE, message=session.get("message_bc"), pod_name=pod_name)

@app.route("/reset")
def reset():
    session.clear()
    return "已重置，<a href='./'>回首頁</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)