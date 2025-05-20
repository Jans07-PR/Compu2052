from app import create_app, db
from app.models import User, Role

app = create_app()

with app.app_context():
    # Crear rol si no existe
    admin_role = Role.query.filter_by(name='Admin').first()
    if not admin_role:
        admin_role = Role(name='Admin')
        db.session.add(admin_role)
        db.session.commit()
        print("Rol 'Admin' creado.")

    # Verificar si ya existe el usuario admin
    existing = User.query.filter_by(username='admin').first()
    if existing:
        print("El usuario admin ya existe.")
    else:
        # Crear usuario admin
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role_id=admin_role.id
        )
        admin_user.set_password('admin123')  # Usa el método del modelo
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Usuario admin creado con éxito.")