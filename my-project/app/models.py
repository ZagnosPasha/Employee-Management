# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager

task_assignments = db.Table('task_assignments',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True)
)

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    remaining_leave_days = db.Column(db.Integer, default = 30)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(100))

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)
    

# Set up user_loader
#@login_manager.user_loader
#def load_user(user_id):
#    return Employee.query.get(int(user_id))


#customer section
class Customer(UserMixin,db.Model):
    """"
    Create a Customer table
    """

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), index=True, unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))

    def is_customer(self):
        return True

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Customer: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    user = Employee.query.get(int(user_id))
    if not user:
        user = Customer.query.get(int(user_id))
    return user

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
    

class Task(db.Model):

    "Create a Task table"

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(260), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('employees.id'))
    completed = db.Column(db.Boolean, default=False)
    in_progress = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)
    employee = db.relationship('Employee', backref='tasks', foreign_keys=[assigned_to])
    #employees = db.relationship('Employee', secondary=task_assignments, lazy='subquery', backref=db.backref('tasks', lazy=True))


    def __repr__(self):
        return '<Task: {}>'.format(self.name)
    

class Leave(db.Model):

    "Create a Leave Table"

    __tablename__ = "leaves"

    id = db.Column(db.Integer,primary_key=True)
    reason = db.Column(db.String(260), nullable=False)
    leave_date = db.Column(db.DateTime,nullable=False)
    leave_duration = db.Column(db.Integer,nullable=False)
    leave_assigned_to = db.Column(db.Integer,db.ForeignKey('employees.id'))
    approved = db.Column(db.Boolean, default=False)
    submitted = db.Column(db.Boolean,default=False)
    disproved = db.Column(db.Boolean,default=False)
    leave_employee = db.relationship('Employee',backref='leaves',foreign_keys=[leave_assigned_to])

    def __repr__(self):
        return '<Leave: {} - {}>'.format(self.leave_date,self.reason)
    
class Product(db.Model):

    "create a product table"

    __tablename__ = 'products'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    image_path = db.Column(db.String(260),nullable=True)
    count = db.Column(db.Integer,nullable=False, default = 0)
    cost_usd = db.Column(db.Integer,nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'))
    tea_id = db.Column(db.Integer, db.ForeignKey('teas.id'))

    db.CheckConstraint('count>=0',name='check_count_positive')
    db.CheckConstraint('cost_usd>=0', name='check_cost_usd_positive')

    def __repr__(self):
        return '<Product: {}>'.format(self.name)

    
class Package(db.Model):

    "Create a package table"

    __tablename__ ='packages'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.String(260),nullable=False)
    image = db.Column(db.String(260),nullable=True)
    products = db.relationship('Product',backref='package',lazy='dynamic')
    
class Tea(db.Model):

    "Create a Tea table"

    __tablename__ = "teas"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.String(260),nullable=False)
    products = db.relationship('Product',backref='tea',lazy='dynamic')

    def __repr__(self):
        return '<Tea : {}>'.format(self.name)
    
class Order(db.Model):

    "Create an order table"

    __tablename__ = "orders"

    id = db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'))
    count = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime,default=datetime.now)
    total_cost = db.Column(db.Integer)
    customer = db.relationship('Customer',backref='orders')
    product = db.relationship('Product',backref='orders')

    def __repr__(self):
        return '<Order: {}>'.format(self.id)
    
    