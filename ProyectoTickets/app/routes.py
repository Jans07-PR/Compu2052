from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import TicketForm, ChangePasswordForm
from app.models import db, User, Ticket

# Blueprint principal que maneja el dashboard, gestión de cursos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra los tickets según el rol.
    """
    tickets = Ticket.query.all()
    return render_template('dashboard.html', tickets=tickets)

@main.route('/crear_ticket', methods=['GET', 'POST'])
@login_required
def crear_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            asunto=form.asunto.data,
            descripcion=form.descripcion.data,
            prioridad=form.prioridad.data,
            tecnico_id=current_user.id
              )
        db.session.add(ticket)
        db.session.commit()
        print("Ticket guardado:", ticket)
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form)


@main.route('/editar_ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    form = TicketForm(obj=ticket)

    if form.validate_on_submit():
        ticket.asunto = form.asunto.data
        ticket.descripcion = form.descripcion.data
        ticket.prioridad = form.prioridad.data
        db.session.commit()
        flash('Ticket actualizado con éxito.')
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form, editar=True)

@main.route('/eliminar_ticket/<int:id>', methods=['POST'])
@login_required
def eliminar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    # Opcional: permisos para que solo admin o dueño pueda eliminar
    if current_user.role.name != 'Admin' and ticket.tecnico_id != current_user.id:
        flash('No tienes permiso para eliminar este ticket.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket eliminado con éxito.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)
