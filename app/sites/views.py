#resource, resources, Resources
from flask import Blueprint, render_template, request,flash, redirect, url_for
from app.sites.models import Sites, SitesSchema

sites = Blueprint('sites', __name__)
#http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = SitesSchema()

#Sites
@sites.route('/' )
def site_index():
    sites = Sites.query.all()
    results = schema.dump(sites, many=True).data
    return render_template('/sites/index.html', results=results)

@sites.route('/add' , methods=['POST', 'GET'])
def site_add():
    if request.method == 'POST':
        #Validate form values by de-serializing the request, http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:        
            name=request.form['name']
            email=request.form['email']
            site=Sites(email, name)
            return add(site, success_url = 'sites.site_index', fail_url = 'sites.site_add')
        else:
           flash(form_errors)        

    return render_template('/sites/add.html')

@sites.route('/update/<int:id>' , methods=['POST', 'GET'])

def site_update (id):
    #Get site by primary key:
    site=Sites.query.get_or_404(id)
    if request.method == 'POST':
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
           site.name = request.form['name']
           site.email = request.form['email']
           return update(site , id, success_url = 'sites.site_index', fail_url = 'sites.site_update')
        else:
           flash(form_errors)

    return render_template('/sites/update.html', site=site)


@sites.route('/delete/<int:id>' , methods=['POST', 'GET'])
def site_delete (id):
     site = Sites.query.get_or_404(id)
     return delete(site, fail_url = 'sites.site_index')
     
     
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