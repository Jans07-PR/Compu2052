from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'  # Necesario para usar Flask-WTF

# Formulario dentro de app.py
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El nombre es obligatorio.'),
        Length(min=3, message='El nombre debe tener al menos 3 caracteres.')
    ])
    correo = StringField('Correo', validators=[
        DataRequired(message='El correo es obligatorio.'),
        Email(message='Formato de correo inválido.')
    ])
    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria.'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')
    ])
    enviar = SubmitField('Registrarse')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        contraseña = form.contraseña.data
        return f"¡Usuario {nombre} registrado con éxito!"
    return render_template('registro.html.jinja2', form=form)

if __name__ == '__main__':
    app.run(debug=True)