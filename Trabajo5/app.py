from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from users import User

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


usuarios = {
    "juan": User(1, "juan", "1234", "admin"),
    "maria": User(2, "maria", "abcd", "user")
}

class UserLogin(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.username = user.username
        self.role = user.role

@login_manager.user_loader
def load_user(user_id):
    for user in usuarios.values():
        if str(user.id) == user_id:
            return UserLogin(user)
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = usuarios.get(username)
        if user and user.verify_password(password):
            login_user(UserLogin(user))
            return redirect(url_for("dashboard"))
        return "Credenciales inválidas"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", nombre=current_user.username, rol=current_user.role)

if __name__ == "__main__":
    app.run(debug=True)