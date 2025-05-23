from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
