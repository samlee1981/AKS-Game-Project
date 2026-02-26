from flask import Blueprint, render_template_string, request, session, url_for, redirect
import random
import os

guess_bp = Blueprint('guess', __name__, url_prefix='/guess')

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
    <a href="{{ url_for('guess.reset') }}">重新開始</a>
    <hr>
    <a href="/">回首頁 (選遊戲)</a>
    <hr>
    <small>目前運行的 Pod 名稱: {{ pod_name }}</small>
</body>
</html>
"""

@guess_bp.route("/", methods=["GET", "POST"])
def index():
    if "guess_num_target" not in session:
        session["guess_num_target"] = random.randint(1, 100)
        session["guess_num_message"] = "遊戲開始！請輸入 1 到 100 之間的數字。"

    pod_name = os.getenv("HOSTNAME", "Local Environment")

    message = session.get("guess_num_message")

    if request.method == "POST":
        try:
            guess_str = request.form.get("guess")
            if not guess_str:
                session["guess_num_message"] = "請輸入有效的數字。"
            else:
                guess = int(guess_str)
                target = session.get("guess_num_target")

                if target is None: # handle case where target is lost
                     session["guess_num_target"] = random.randint(1, 100)
                     target = session["guess_num_target"]

                if guess < target:
                    session["guess_num_message"] = f"數字 {guess} 太小了！"
                elif guess > target:
                    session["guess_num_message"] = f"數字 {guess} 太大了！"
                else:
                    session["guess_num_message"] = f"恭喜你猜中了！數字就是 {target}。"
                    session.pop("guess_num_target", None) # 猜中後清除數字
        except ValueError:
            session["guess_num_message"] = "請輸入有效的數字。"

        message = session.get("guess_num_message")

    return render_template_string(HTML_TEMPLATE, message=message, pod_name=pod_name)

@guess_bp.route("/reset")
def reset():
    session.pop("guess_num_target", None)
    session.pop("guess_num_message", None)
    return redirect(url_for('guess.index'))
