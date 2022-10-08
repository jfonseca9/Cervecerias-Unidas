import db
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Base, UserMixin):

    __tablename__ = 'empleados'

    id = Column(Integer, primary_key=True)
    nombres = Column(String(80), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_superadmin = Column(Boolean, default=False)

    def __init__(self, nombres, email, password, is_admin=False, is_superadmin=False):
        self.nombres = nombres
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_superadmin = is_superadmin

    def __repr__(self):
        return f'<User {self.email}>'

    def __str__(self):
        return self.nombres

    def check_password(self, password):
        return check_password_hash(self.password, password)