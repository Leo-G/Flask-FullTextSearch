from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate
from app.users.models import db

import datetime



class Images(db.Model):
 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250), nullable=False)
  file_path = db.Column(db.Text, nullable=False)
  description = db.Column(db.Text)
  tag = db.Column(db.String(250), nullable=False)
  creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


  def __init__(self,name, file_path, description, tag):
    self.name = name
    self.file_path = file_path
    self.tag = tag
    self.description = description
    

  def add(self,image):
     db.session.add(image)
     return session_commit ()

  def update(self):
      return session_commit()

  def delete(self,image):
     db.session.delete(image)
     return session_commit()

class ImagesSchema(Schema):
    #http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation
    #http://marshmallow.readthedocs.org/en/latest/api_reference.html?highlight=api%20fields#module-marshmallow.fields
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    name = fields.String(validate=not_blank)
    file_path = fields.String(validate=not_blank)
    description = fields.String()
    tag = fields.String(required = True, validate = not_blank)

    class Meta:
       fields = ('id', 'name', 'file_path', 'description', 'tag', 'creation_date')


def  session_commit ():
      try:
        db.session.commit()
      except SQLAlchemyError as e:
         db.session.rollback()
         reason=str(e)
         return reason
