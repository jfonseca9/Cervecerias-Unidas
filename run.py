import db
from flask import Flask, render_template, request, redirect, url_for
from forms import loginform, registerform
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "home"
from models import User

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('editar'))
    form = loginform()
    if form.validate_on_submit():
        user = User.get_by_email(form.emailLogin.data)
        if user is not None and user.check_password(form.passwordLogin.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('editar'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    form = registerform()
    error = None
    if request.method == 'POST':
        nombreRegistro = form.nombreRegistro.data
        emailRegister = form.emailRegister.data
        passwordRegister = form.passwordRegister.data
        user = db.session.query(User).filter_by(email=emailRegister).first()
        if user is not None:
            error = f'El email {emailRegister} ya está siendo utilizado por otro usuario'
        else:
            user = User(nombres=nombreRegistro, email=emailRegister, password=generate_password_hash(passwordRegister))
            db.session.add(user)
            db.session.commit()
    return render_template("registro.html", form=form, error=error)

@app.route('/buscar/')
#@login_required
def buscar():    
    return render_template('buscar.html')

@app.route('/editar/')
def editar():    
    return render_template('editar.html')

@app.route('/home/')
def home():    
    return render_template('hola.html')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)