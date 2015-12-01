from flask import Blueprint, render_template, request,flash, redirect, url_for, jsonify, current_app
from app.images.models import Images, ImagesSchema
from app.users.models import db
from app.users.views import Resource
from werkzeug import secure_filename
from config import UPLOAD_FOLDER
import os


import subprocess
from flask_restful import Api

images = Blueprint('images', __name__)
#http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = ImagesSchema()
new_schema = ImagesSchema()

# API START

api = Api(images)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class ImagesList(Resource):
    def get(self):
        query =  Images.query.all()
        images = new_schema.dump(query, many=True).data
        return jsonify({"images":images})

    def post(self):
         name=request.form['name']
         description=request.form['description']
         tag = request.form['tag']
         file = request.files['file']
         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

         image = Images(name, file_path, description, tag )
         add = image.add(image)
         #if does not return any error
         if not add :
            return jsonify({"message":"success"})
         else:
            return jsonify({"message":add})
         #else:
           # print(form_errors)
            

class ImagesUpdate(Resource):

    def get(self, id):
        query =  Images.query.get(id)
        site = new_schema.dump(query).data
        return jsonify({"site":site})


    def put(self, id):
        site=Images.query.get_or_404(id)
        data=request.get_json(force=True)
        form_errors = schema.validate(data['site'])
        if not form_errors:
               site.url = data['site']['url']
               site.content = data['site']['content']
               site.tag = data['site']['tag']
               site.reddit_score = data['site']['reddit_score']
               site.ycombinator_score = data['site']['ycombinator_score']
               update = site.update()
               #if does not return any error
               if not update :
                  return jsonify({"message":"success"})
               else:
                  return jsonify({"message":update})

    def delete(self, id):
        site=Images.query.get_or_404(id)
        delete=site.delete(site)
        if not delete :
                 return jsonify({"message":"success"})

        else:
            return jsonify({"message":delete})




api.add_resource(ImagesList, '/')
api.add_resource(ImagesUpdate, '/<int:id>')

### SEARCH START ###
@images.route('/search', methods=['GET'])
def search():

   return render_template('search.html')


@images.route('/results/<int:page>', methods=['GET'] )
@images.route('/results', defaults={'page': 1}, methods=['GET'] )
def results(page):
           search_string = request.args['search']
           query = Images.query.search(search_string)
           results = query.paginate(page=page, per_page=10)
           return render_template('results.html', results=results)


@images.route('/tags', methods=['GET'])
def tags():
    query = Images.query.with_entities(Images.id,Images.tag).order_by(Images.tag)
    tags = schema.dump(query, many=True).data
    return jsonify({"tags":tags})

## For testing only
@images.route('/tag', methods=['GET'])

def tag():

    return render_template('tag.html')
## End testing
### SEARCH END ###

"""
#Images
@images.route('/' , methods=['GET'])
@login_required
def site_index():
    return render_template('/images/index.html')

new_schema = ImagesSchema()
@images.route('/images', methods=['GET'])
@login_required
def images_all():
    query =  Images.query.all()
    images = new_schema.dump(query, many=True).data
    return jsonify({"images":images})


@images.route('/add' , methods=['POST', 'GET'])
@login_required
def site_add():

    if request.method == 'POST':
        #Validate form values by de-serializing the request, http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation


    return render_template('/images/add.html')

@images.route('/update/<int:id>' , methods=['POST', 'GET'])
@login_required
def site_update (id):
    #Get site by primary key:
    site=Images.query.get_or_404(id)
    if request.method == 'POST':
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
           site.url = request.form['url']
           site.content = request.form['content']
           site.tag = request.form['tag']
           return update(site , id, success_url = 'images.site_index', fail_url = 'images.site_update')
        else:
           flash(form_errors)


    return render_template('/images/update.html', site=site)


@images.route('/delete/<int:id>' , methods=['POST', 'GET'])
@login_required
def site_delete (id):
     site = Images.query.get_or_404(id)
     return delete(site, fail_url = 'images.site_index')

#CRUD FUNCTIONS
#Arguments  are data to add, function to redirect to if the add was successful and if not
def add (data, success_url = '', fail_url = ''):
    add = data.add(data)
    #if does not return any error
    if not add :
       flash("Add was successful")
       return redirect(url_for(success_url))
    else:
       message=add
       flash(message)
       return redirect(url_for(fail_url))


def update (data, id, success_url = '', fail_url = ''):

            update=data.update()
            #if does not return any error
            if not update :
              flash("Update was successful")
              return redirect(url_for(success_url))
            else:
               message=update
               flash(message)
               return redirect(url_for(fail_url, id=id))



def delete (data, fail_url=''):
     delete=data.delete(data)
     if not delete :
              flash("Delete was successful")

     else:
          message=delete
          flash(message)
     return redirect(url_for(fail_url))
"""

