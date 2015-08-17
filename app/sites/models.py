from flask.ext.sqlalchemy import SQLAlchemy,BaseQuery
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate
from app.users.models import db
#http://sqlalchemy-utils.readthedocs.org/en/latest/installation.html
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
from sqlalchemy_searchable import SearchQueryMixin
import datetime

make_searchable()

class SitesQuery(BaseQuery, SearchQueryMixin):
    pass

class Sites(db.Model):
  query_class = SitesQuery
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(250), nullable=False)
  content = db.Column(db.Text)
  tag = db.Column(db.String(250), nullable=False)
  creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
  reddit_score = db.Column(db.Integer, default = 0)
  ycombinator_score = db.Column(db.Integer, default = 0)
  search = db.Column(TSVectorType('url', 'content', 'tag'))

  def __init__(self,url, content, tag, reddit_score=0, ycombinator_score=0 ):
    self.url = url
    self.content = content
    self.tag = tag
    self.reddit_score = reddit_score
    self.ycombinator_score = ycombinator_score

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
       fields = ('id', 'url', 'tag', 'content','creation_date', 'reddit_score', 'ycombinator_score')


def  session_commit ():
      try:
        db.session.commit()
      except SQLAlchemyError as e:
         db.session.rollback()
         reason=str(e)
         return reason
