from functools import wraps
from flask import render_template
from flask_login import current_user

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_superadmin = getattr(current_user, 'is_superadmin', False)
        if not is_superadmin:
            return render_template('error.html')
        return f(*args, **kws)
    return decorated_function