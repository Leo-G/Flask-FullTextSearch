from flask.ext.sqlalchemy import SQLAlchemy,BaseQuery
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate
from app.users.models import db
#http://sqlalchemy-utils.readthedocs.org/en/latest/installation.html
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
from sqlalchemy_searchable import SearchQueryMixin

make_searchable()

class SitesQuery(BaseQuery, SearchQueryMixin):
    pass

class Sites(db.Model):
  query_class = SitesQuery
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(250), nullable=False)
  content = db.Column(db.Text)
  tag = db.Column(db.String(250), nullable=False)
  search = db.Column(TSVectorType('url', 'content', 'tag'))

  def __init__(self,url, content, tag):
    self.url = url
    self.content = content
    self.tag = tag

  def add(self,site):
     db.session.add(site)
     return session_commit ()

  def update(self):
      return session_commit()

  def delete(self,site):
     db.session.delete(site)
     return session_commit()

class SitesSchema(Schema):
    #http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation
    #http://marshmallow.readthedocs.org/en/latest/api_reference.html?highlight=api%20fields#module-marshmallow.fields
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    url = fields.Url()
    content = fields.String()
    #add import sqlalchemy_utils in alembic file
    tag = fields.String(required = True, validate = not_blank)

    class Meta:
       fields = ('id', 'url', 'content', 'tag', 'search')


def  session_commit ():
      try:
        db.session.commit()
      except SQLAlchemyError as e:
         db.session.rollback()
         reason=str(e)
         return reason
