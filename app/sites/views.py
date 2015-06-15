#resource, resources, Resources
from flask import Blueprint, render_template, request,flash, redirect, url_for, jsonify
from app.sites.models import Sites, SitesSchema
from app.users.models import db
from flask.ext.login import login_required

sites = Blueprint('sites', __name__)
#http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = SitesSchema(only=('id','tag'))

### SEARCH START ###
@sites.route('/search', methods=['GET'])
def search():
  
   return render_template('search.html')
   

@sites.route('/results/<int:page>', methods=['GET'] )      
@sites.route('/results', defaults={'page': 1}, methods=['GET'] )
def results(page):
           search_string = request.args['search']
           query = Sites.query.search(search_string)           
           results = query.paginate(page=page, per_page=10)
           return render_template('results.html', results=results)
       
       
@sites.route('/tags', methods=['GET'])
def tags():
    query = Sites.query.with_entities(Sites.id,Sites.tag).order_by(Sites.tag)
    tags = schema.dump(query, many=True).data
    return jsonify({"tags":tags})

## For testing only
@sites.route('/tag', methods=['GET'])

def tag():
    
    return render_template('tag.html')
## End testing  
### SEARCH END ###

#Sites
@sites.route('/<int:page>' )
@sites.route('/' )
@login_required
def site_index(page=1):
    sites = Sites.query
    results = sites.paginate(page=page, per_page=10)
    return render_template('/sites/index.html', results=results)

@sites.route('/add' , methods=['POST', 'GET'])
@login_required
def site_add():
   
    if request.method == 'POST':
        #Validate form values by de-serializing the request, http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
            url = request.form['url']
            content = request.form['content']
            tag = request.form['tag']
            site = Sites(url, content, tag)
            return add(site, success_url = 'sites.site_index', fail_url = 'sites.site_add')
        else:
            flash(form_errors)      

    return render_template('/sites/add.html')

@sites.route('/update/<int:id>' , methods=['POST', 'GET'])
@login_required
def site_update (id):
    #Get site by primary key:
    site=Sites.query.get_or_404(id)
    if request.method == 'POST':
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
           site.url = request.form['url']
           site.content = request.form['content']
           site.tag = request.form['tag']
           return update(site , id, success_url = 'sites.site_index', fail_url = 'sites.site_update')
        else:
           flash(form_errors)


    return render_template('/sites/update.html', site=site)


@sites.route('/delete/<int:id>' , methods=['POST', 'GET'])
@login_required
def site_delete (id):
     site = Sites.query.get_or_404(id)
     return delete(site, fail_url = 'sites.site_index')
     
     
     
     
###GITHUB WEBHOOK START ###
import subprocess
 
@sites.route('/github_payload', methods=['POST'])
def github_payload():
      data = request.get_json()
      print(data['commits']['distinct'])
      cmd = subprocess.Popen(['./sites/flask_search/github-webhook.bash'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      out,error = cmd.communicate()
      print(out.splitlines())      
      ok = 200
      return ok
        
        
   


###GITHUB WEBHOOK END ###
     
     
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
     
#Create  Triggers and Functions
@sites.route('/trigger', methods=['GET'])
def trig():
   SQL_index = db.text("""CREATE INDEX tsv_idx ON sites USING gin(search) """)
   db.engine.execute(SQL_index)
   SQL = db.text("""CREATE OR REPLACE FUNCTION search_trigger() RETURNS trigger AS $$
                begin
                  new.search :=
                    setweight(to_tsvector(coalesce(new.url,'')), 'B') ||
                    setweight(to_tsvector(coalesce(new.content,'')), 'C')||
                    setweight(to_tsvector(coalesce(new.tag,'')), 'A');
                  return new;
                end
                $$ LANGUAGE plpgsql""")
   db.engine.execute(SQL)
   SQL1 = db.text("""CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
               ON sites FOR EACH ROW EXECUTE PROCEDURE search_trigger();""")
   db.engine.execute(SQL1)
   return "Done"