from flask import Flask, flash, render_template, request, redirect, session, url_for
from forms import loginform, registerform, updateForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os, decoratorsAdmin, decoratorsSuperAdmin
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///DBCervezas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

# Creación del modelo de  la base de datos - Inicio #

class Empleado(db.Model):

    __tablename__ = 'empleado'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombres = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    celular = db.Column(db.String(80), unique=True, nullable=False)
    fechaFirmaC = db.Column(db.String(80), nullable=False)
    fechaFinC = db.Column(db.String(80), nullable=False)
    cargo = db.Column(db.String(80), nullable=False)
    area = db.Column(db.String(80), nullable=False)
    salario = db.Column(db.String(80), nullable=False)
    calificacion = db.Column(db.String(80), default='Sin Calificar')
    estado_civil = db.Column(db.String(80), nullable=False)
    tipo_contrato = db.Column(db.String(80), nullable=False)
    user_id = db.relationship("User", cascade="all,delete", backref="empleado", uselist=False)
    ubicacion_id = db.relationship("Ubicacion", cascade="all,delete", backref="empleado", uselist=False)

    def __repr__(self):
        return f'<Empleado {self.nombres}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return Empleado.query.filter_by(email=email).first()

class Ubicacion(db.Model, UserMixin):

    __tablename__ = 'ubicacion'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.Integer, db.ForeignKey('empleado.email', ondelete='CASCADE'), nullable=False, unique=True)
    barrio = db.Column(db.String(128), nullable=False)
    direccion = db.Column(db.String(128), nullable=False)
    departamento = db.Column(db.String(128), nullable=False)
    ciudad = db.Column(db.String(128), nullable=False)
    pais = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return Ubicacion.query.filter_by(email=email).first()

class User(db.Model, UserMixin):

    __tablename__ = 'sesion'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.Integer, db.ForeignKey('empleado.email', ondelete='CASCADE'), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superadmin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

# Creación del modelo de la base de datos - Final #

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        user = User.get_by_email(session["user"])
        empleado = Empleado.get_by_email(session["user"])
        ubicacion = Ubicacion.get_by_email(session["user"])
        return render_template('user.html', user=user, empleado=empleado, ubicacion=ubicacion)
    form = loginform()
    if form.validate_on_submit():
        user = User.get_by_email(form.emailLogin.data)
        empleado = Empleado.get_by_email(form.emailLogin.data)
        ubicacion = Ubicacion.get_by_email(form.emailLogin.data)
        session["user"] = form.emailLogin.data
        if user is not None and user.check_password(form.passwordLogin.data):
            login_user(user, remember=form.remember_me.data)
            return render_template('user.html', user=user, empleado=empleado, ubicacion=ubicacion)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop("user", None)
    logout_user()
    return redirect(url_for('login'))

@app.route('/registro/', methods=['GET', 'POST'])
@login_required
@decoratorsAdmin.admin_required
def registro():
    form = registerform()
    error = 'None'
    if form.validate_on_submit():
        nombreRegistro = form.nombreRegistro.data
        apellidoRegistro = form.apellidoRegistro.data
        fechaNacimientoRegistro = form.fechaNacimientoRegistro.data
        emailRegister = form.emailRegister.data
        passwordRegister = form.passwordRegister.data
        cargoRegistro = form.cargoRegistro.data
        tipoContratoRegistro = form.tipoContratoRegistro.data
        celularRegistro = form.celularRegistro.data
        areaRegistro = form.areaRegistro.data
        fechaFirmaC = form.fechaFirmaCRegistro.data
        fechaFinC = form.fechaFinCRegistro.data
        ciudadRegistro = form.ciudadRegistro.data
        barrioRegistro = form.barrioRegistro.data
        salarioRegistro = form.salarioRegistro.data
        estadoCivilRegistro = form.estadoCivilRegistro.data
        direccionRegistro = form.direccionRegistro.data
        departamentoRegistro = form.departamentoRegistro.data
        paisRegistro = form.paisRegistro.data

        user = User.get_by_email(emailRegister)
        if user is not None:
            error = f'El email {emailRegister} ya está siendo utilizado por otro usuario'
        else:
            empleado = Empleado(nombres=nombreRegistro, apellido=apellidoRegistro, fecha_nacimiento=fechaNacimientoRegistro, email=emailRegister, celular=celularRegistro, fechaFirmaC=fechaFirmaC, fechaFinC=fechaFinC, cargo=cargoRegistro, area=areaRegistro, salario=salarioRegistro, estado_civil=estadoCivilRegistro, tipo_contrato=tipoContratoRegistro)
            ubicacion = Ubicacion(barrio=barrioRegistro, direccion=direccionRegistro, departamento=departamentoRegistro, ciudad=ciudadRegistro, pais=paisRegistro, empleado=empleado)
            user = User(empleado=empleado)
            user.set_password(passwordRegister)
            empleado.save()
            ubicacion.save()
            user.save()
            flash('Empleado Registrado')
    return render_template("registro.html", form=form, error=error)

@app.route('/buscar/', methods=['GET', 'POST'])
@login_required
@decoratorsAdmin.admin_required
def buscar():
    form = updateForm()
    if request.method == 'POST':
        empleado = Empleado.get_by_email(form.emailUser.data)
        return render_template('buscar.html', form=form, empleado=empleado)
    else:    
        return render_template('buscar.html', form=form)

@app.route('/editar/')
@login_required
@decoratorsAdmin.admin_required
def editar():
    empleados = Empleado.query.all()
    return render_template('editar.html', empleados=empleados)

@app.route('/calificar/<id>/', methods=['GET', 'POST'])
@login_required
@decoratorsAdmin.admin_required
def modificar(id):
    empleado = Empleado.query.filter_by(id=int(id)).first()
    empleado.calificacion = request.form['calificar']
    db.session.commit()
    return redirect(url_for('buscar'))

@app.route('/delete/<id>/')
@login_required
@decoratorsAdmin.admin_required
def delete(id):
    Empleado.query.filter_by(id=int(id)).delete()
    User.query.filter_by(id=int(id)).delete()
    Ubicacion.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('editar'))

@app.route('/usuario/')
@login_required
def usuario():    
    return render_template('user.html')

@app.route('/setrol/', methods=['GET', 'POST'])
@login_required
@decoratorsAdmin.admin_required
@decoratorsSuperAdmin.superadmin_required
def setrol():
    form = updateForm()
    if request.method == 'POST':
        empleado = Empleado.get_by_email(form.emailUser.data)
        user = User.get_by_email(form.emailUser.data)
        return render_template('cambiorol.html', form=form, empleado=empleado, user=user)
    else:
        return render_template('cambiorol.html', form=form)

@app.route('/cambiorol/<id>/', methods=['GET', 'POST'])
@login_required
@decoratorsAdmin.admin_required
@decoratorsSuperAdmin.superadmin_required
def cambiorol(id):
    user = User.query.filter_by(id=int(id)).first()
    setrol = request.form['setrol']
    if (setrol == 'A'):
        user.is_admin = True
        user.is_superadmin = False
        db.session.commit()
    elif (setrol == 'S'):
        user.is_superadmin = True
        user.is_admin = True
        db.session.commit()
    else:
        user.is_superadmin = False
        user.is_admin = False
        db.session.commit()
    return redirect(url_for('setrol'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)