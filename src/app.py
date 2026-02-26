from flask import Flask, render_template, session
import os
from guess_number import guess_bp
from guess_bc import bc_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(guess_bp)
app.register_blueprint(bc_bp)

@app.route("/")
def index():
    pod_name = os.getenv("HOSTNAME", "Local Environment")
    return render_template("index.html", pod_name=pod_name)

@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
