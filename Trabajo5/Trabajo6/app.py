from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity
from users import usuarios, User

app = Flask(__name__)
app.secret_key = "clave_supersecreta"

login_manager = LoginManager(app)
login_manager.login_view = "login"

principals = Principal(app)

# Permisos por rol
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))
user_permission = Permission(RoleNeed('user'))

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

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = usuarios.get(username)
        if user and user.verify_password(password):
            user_login = UserLogin(user)
            login_user(user_login)
            identity_changed.send(app, identity=Identity(user_login.id))
            return redirect(url_for("dashboard"))
        return "Credenciales inválidas"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", nombre=current_user.username, rol=current_user.role)

@app.route("/admin")
@admin_permission.require(http_exception=403)
def admin():
    return "Vista de administrador"

@app.route("/edit")
@editor_permission.require(http_exception=403)
def edit():
    return "Zona para editores"

@app.route("/read")
@user_permission.require(http_exception=403)
def read():
    return "Zona de lectura (cualquier usuario)"

if __name__ == "__main__":
    app.run(debug=True)