from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate
from flask.ext.login import UserMixin

db = SQLAlchemy()

# Relationships

user_roles=db.Table('user_roles',

                             db.Column('user_id', db.Integer,db.ForeignKey('users.id'), nullable=False),
                             db.Column('role_id',db.Integer,db.ForeignKey('roles.id'),nullable=False),
                             db.PrimaryKeyConstraint('user_id', 'role_id')
                             )

class UserRoles():
    def __init__(self,user_id,role_id):
      self.user_id=user_id
      self.role_id=role_id

db.mapper(UserRoles, user_roles)

class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(250), unique=True, nullable=False)
  name = db.Column(db.String(250), nullable=False)
  password = db.Column(db.String(250), nullable=False)
  is_enabled = db.Column(db.Boolean(), nullable=False, server_default='False')
  roles = db.relationship('Roles', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))


  def __init__(self,email, name, password, is_enabled):
    self.email=email
    self.name=name
    self.password = password
    self.is_enabled = is_enabled

  def add(self,user):
     db.session.add(user)
     return session_commit ()

  def update(self):
      return session_commit()

  def delete(self,user):
     db.session.delete(user)
     return session_commit()

  def is_active(self):
      return self.is_enabled


class UsersSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    name = fields.String(validate=not_blank)
    email = fields.Email()
    #Need to make this field not blank on add
    password = fields.String()
    is_active = fields.Boolean(validate=not_blank)
    role = fields.String()

    class Meta:
       fields = ('id', 'email', 'name', 'is_enabled')




def  session_commit ():
      try:
        db.session.commit()
      except SQLAlchemyError as e:
         db.session.rollback()
         reason=str(e)
         return reason
