# app/home/views.py

from flask import abort, render_template
from flask_login import current_user, login_required
from ..models import Customer,Employee
from . import home
from flask_login import login_required, login_user, logout_user

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    logout_user()
    print(f'Customer: {Customer}')
    print(f'isinstance(current_user, Customer): {isinstance(current_user, Customer)}')
    return render_template('home/index.html', title="Welcome",Customer=Customer)

@home.route('/customer/dashboard')
@login_required
def customer_dashboard():
    
    #Render the dashboard template on the 
    
    return render_template('home/customer_dashboard.html', title="Dashboard",Customer=Customer)

@home.route('/dashboard')
@login_required
def dashboard():
    
    return render_template('home/dashboard.html', title="Dashboard",Customer=Customer)
"""
@home.route('/dashboard')
@login_required
def dashboard():
    
    #Render the dashboard template on the /dashboard route
   
    return render_template('home/dashboard.html', title="Dashboard",isinstance=isinstance, Customer=Customer)
"""
# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

