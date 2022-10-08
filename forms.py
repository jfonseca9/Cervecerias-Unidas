from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length

class loginform(FlaskForm):
    emailLogin = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@dominio.com"})
    passwordLogin = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "minimo 8 caracteres"})
    remember_me = BooleanField('Recuérdame')
    submitLogin = SubmitField('Ingresar')

class registerform(FlaskForm):
    nombreRegistro = StringField('Nombres')
    apellidoRegistro = StringField('Apellidos')
    fechaNacimientoRegistro = DateField('Fecha De Nacimiento') 
    ciudadRegistro = StringField('Ciudad')
    departamentoRegistro = StringField('Departamento')
    paisRegistro = StringField('País')
    direccionRegistro = StringField('Dirección')
    barrioRegistro = StringField('Barrio')
    estadoCivilRegistro = SelectField('Estado Civil', choices=[('Casado', 'Casado'), ('Soltero', 'Soltero'), ('Unión Libre', 'Unión Libre'), ('Viudo', 'Viudo')])
    celularRegistro = StringField('Celular')
    emailRegister = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@dominio.com"})
    passwordRegister = PasswordField('Asignar Contraseña', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "minimo 8 caracteres"})
    tipoContratoRegistro = SelectField('Tipo de Contrato', choices=[('Termino Fijo', 'Termino Fijo'), ('Termino Indefinido', 'Termino Indefinido'), ('Prestación de Servicios', 'Prestación de Servicios')])
    fechaFirmaCRegistro = DateField('Fecha de Firma Contrato') 
    fechaFinCRegistro = DateField('Fecha de Fin Contrato') 
    cargoRegistro = StringField('Cargo')
    areaRegistro = StringField('Área')
    salarioRegistro = StringField('Salario')
    epsRegistro = StringField('EPS')
    arlRegistro = StringField('ARL')
    pensionRegistro = StringField('Fondo de Pensión')
    submitRegister = SubmitField('Registrar Empleado')