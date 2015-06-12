from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

from app import create_app
from app.users.models import Users, db
from app.roles.models import Roles

app = create_app('config')

name='Leo'
email='leo@leog.in'
password=generate_password_hash('password')
is_enabled=True
admin_role_name="admin"
user=Users(email, name,password, is_enabled)

def db_commit():
    try:
          db.session.commit()
          print("{} was added successfully".format(email))
          return True
    except SQLAlchemyError as e:
          reason=str(e)
          print (reason)
          return False

with app.app_context():
    admin_role = Roles(admin_role_name)
    no_role = Roles("None")
    db.session.add_all([admin_role, no_role])
    if db_commit():
        user_role = Roles.query.filter_by(name=admin_role_name).first()
        user.roles.append(user_role)
        db.session.add(user)
        db_commit()
