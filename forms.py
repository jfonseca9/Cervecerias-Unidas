from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length

class loginform(FlaskForm):
    emailLogin = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@dominio.com"})
    passwordLogin = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "minimo 8 caracteres"})
    remember_me = BooleanField('Recuérdame')
    submitLogin = SubmitField('Ingresar')

class registerform(FlaskForm):
    nombreRegistro = StringField('Nombres', validators=[DataRequired()])
    apellidoRegistro = StringField('Apellidos', validators=[DataRequired()])
    fechaNacimientoRegistro = DateField('Fecha de Nacimiento', validators=[DataRequired()]) 
    ciudadRegistro = StringField('Ciudad', validators=[DataRequired()])
    departamentoRegistro = StringField('Departamento', validators=[DataRequired()])
    paisRegistro = StringField('País', validators=[DataRequired()])
    direccionRegistro = StringField('Dirección', validators=[DataRequired()])
    barrioRegistro = StringField('Barrio', validators=[DataRequired()])
    estadoCivilRegistro = SelectField('Estado Civil', choices=[('Casado', 'Casado'), ('Soltero', 'Soltero'), ('Unión Libre', 'Unión Libre'), ('Viudo', 'Viudo')])
    celularRegistro = StringField('Celular', validators=[DataRequired()])
    emailRegister = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@dominio.com"})
    passwordRegister = PasswordField('Asignar Contraseña', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "minimo 8 caracteres"})
    tipoContratoRegistro = SelectField('Tipo de Contrato', validators=[DataRequired()], choices=[('Termino Fijo', 'Termino Fijo'), ('Termino Indefinido', 'Termino Indefinido'), ('Prestación de Servicios', 'Prestación de Servicios')])
    fechaFirmaCRegistro = DateField('Fecha de Firma Contrato', validators=[DataRequired()]) 
    fechaFinCRegistro = DateField('Fecha de Fin Contrato', validators=[DataRequired()]) 
    cargoRegistro = StringField('Cargo', validators=[DataRequired()])
    areaRegistro = StringField('Área', validators=[DataRequired()])
    salarioRegistro = StringField('Salario', validators=[DataRequired()])
    epsRegistro = StringField('EPS', validators=[DataRequired()])
    arlRegistro = StringField('ARL', validators=[DataRequired()])
    pensionRegistro = StringField('Fondo de Pensión', validators=[DataRequired()])
    submitRegister = SubmitField('Registrar Empleado')

class updateForm(FlaskForm):
    emailUser = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@dominio.com"})
    submitUser = SubmitField('Buscar Empleado')