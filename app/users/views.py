from flask import Blueprint, render_template, request,flash, redirect, url_for, jsonify
from app.users.models import Users, UsersSchema
from app.roles.models import Roles
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from flask_restful import Resource, Api




users = Blueprint('users', __name__)
#http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = UsersSchema()

api = Api(users)

class Auth(Resource):
    def post(self):
        data=request.get_json(force=True)
        #print(data['user'][0]['password'])
        email=data['user'][0]['username']
        password=data['user'][0]['password']
        user=Users.query.filter_by(email=email).first()
        if user == None:           
           return jsonify({"message":"invalid username/password"})
        if check_password_hash(user.password,password) and login_user(user):
                 return jsonify({"message":"success"})
        else:
             return jsonify({"message":"invalid password/username"})

api.add_resource(Auth, '/auth')             

#Users
@users.route('/' )
@login_required
def user_index():
    results = Users.query.all()
    #results = schema.dump(users, many=True).data
    return render_template('/users/index.html', results=results)

@users.route('/add' , methods=['POST', 'GET'])

def user_add():
    if request.method == 'POST':
        #http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
            name=request.form['name']
            email=request.form['email'].lower()
            password=generate_password_hash(request.form['password'])
            is_enabled=request.form['is_enabled']
            user=Users(email, name,password, is_enabled)
            roles = request.form.getlist('role')
            for r in roles:
                role = Roles.query.filter_by(name=r).first()
                user.roles.append(role)
            return add(user, success_url = 'users.user_index', fail_url = 'users.user_add')
        else:
           flash(form_errors)

    return render_template('/users/add.html')

@users.route('/update/<int:id>' , methods=['POST', 'GET'])
@login_required
def user_update (id):
    #Get user by primary key:
    user=Users.query.get_or_404(id)
    current_role = [role.name for role in user.roles]

    if request.method == 'POST':
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
           user.name = request.form['name']
           user.email = request.form['email'].lower()
           user.is_enabled=request.form['is_enabled']
           new_role = request.form.getlist('role')
           print(new_role)

           #Add new roles
           for role in new_role:
                if role not in current_role:
                  role = Roles.query.filter_by(name=role).first()
                  user.roles.append(role)
            #Remove old roles.
           for role in current_role:
                if role not in new_role:
                      role = Roles.query.filter_by(name=role).first()
                      user.roles.remove(role)
           if not request.form['password']:
               return update(user , id, success_url = 'users.user_index', fail_url = 'users.user_update')
           else:
               user.password=generate_password_hash(request.form['password'])


           return update(user , id, success_url = 'users.user_index', fail_url = 'users.user_update')
        else:
           flash(form_errors)

    return render_template('/users/update.html', user=user, current_role = current_role)


@users.route('/delete/<int:id>' , methods=['POST', 'GET'])
@login_required
def user_delete (id):
     user = Users.query.get_or_404(id)
     return delete(user, fail_url = 'users.user_index')


#Initialize the LoginManager from Flask-Login
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@users.route('/login', methods=['POST', 'GET'])
def login ():
  if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user=Users.query.filter_by(email=email).first()
        if user == None:
           flash("invalid username/password")
           return render_template('login.html')
        if check_password_hash(user.password,password) and login_user(user):
                 return redirect(url_for('users.user_index'))
        else:
             flash("invalid username/password")
  return render_template('login.html')

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))



#End Login Manager


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
