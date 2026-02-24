from flask import Flask, render_template_string, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # 產生隨機金鑰以加密 session

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>猜數字遊戲</title></head>
<body>
    <h1>1 ~ 100 猜數字遊戲</h1>
    <p>{{ message }}</p>
    <form method="POST">
        <input type="number" name="guess" min="1" max="100" required>
        <button type="submit">送出</button>
    </form>
    <br>
    <a href="/reset">重新開始</a>
    <hr>
    <small>目前運行的 Pod 名稱: {{ pod_name }}</small>
</body>
</html>
"""
@app.route("/healthz")
def healthz():
    return "OK", 200


@app.route("/", methods=["GET", "POST"])
def index():
    # 如果 session 裡沒數字，就產生一個
    if "target" not in session:
        session["target"] = random.randint(1, 100)
        session["message"] = "遊戲開始！請輸入 1 到 100 之間的數字。"

    pod_name = os.getenv("HOSTNAME", "Local Environment")
    
    if request.method == "POST":
        try:
            guess = int(request.form.get("guess"))
            target = session["target"]
            
            if guess < target:
                session["message"] = f"數字 {guess} 太小了！"
            elif guess > target:
                session["message"] = f"數字 {guess} 太大了！"
            else:
                session["message"] = f"恭喜你猜中了！數字就是 {target}。"
                session.pop("target") # 猜中後清除數字
        except ValueError:
            session["message"] = "請輸入有效的數字。"

    return render_template_string(HTML_TEMPLATE, message=session.get("message"), pod_name=pod_name)

@app.route("/reset")
def reset():
    session.clear()
    return "已重置，<a href='/'>回首頁</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)