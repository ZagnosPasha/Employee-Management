# app/admin/views.py

import pdfkit
from flask import abort, flash, redirect, render_template, url_for, request,jsonify
from flask_login import current_user, login_required
from datetime import datetime,date
from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm, TaskForm,PackageForm,TeaForm,ProductForm,OrderForm
from .. import db
from ..models import Department, Role, Employee, Task, Leave,Package,Tea,Product,Customer,Order
from werkzeug.utils import secure_filename
import os
from flask import current_app
from werkzeug.datastructures import FileStorage
from sqlalchemy import and_
from flask import Flask, make_response
from xhtml2pdf import pisa
from io import BytesIO

#from flask_weasyprint import HTML, render_pdf

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

# Role Views

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.filter_by(is_approved=True).all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


#download employees

@admin.route('/download_tasks')
@login_required
def download_employees():
    # Get the employee and task data
    employees = Employee.query.filter_by(is_approved=True).all()

    # Render the HTML template with the employee data
    html = render_template('admin/employees/employee_pdf.html',  employees=employees)

    # Create a PDF file from the rendered HTML
    pdf_file = BytesIO()
    pisa.CreatePDF(html, dest=pdf_file)

    # Create a response with the generated PDF file
    response = make_response(pdf_file.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=employees.pdf'

    return response

@admin.route('/default_leave',methods=['POST'])
@login_required
def reset_leave():
    """Reset employee leave to default"""
    check_admin()

    default_leave_days=Employee.remaining_leave_days.default.arg
    employees=Employee.query.all()
    print('Number of employees:',len(employees))
    for employee in employees:
        try:
            employee.remaining_leave_days=default_leave_days
        except Exception as e:
            print('Error:',e)
            flash('An error ocurred whileupdating')
    try:
        db.session.commit()
        flash('All employees remaining leave days have been rest to {}.'.format(default_leave_days))
    except Exception as e:
        print('Error:',e)
        flash('An error ocurrec')
    return redirect(url_for('admin.list_employees'))



#search part

@admin.route('/employees/search')
@login_required
def search():

    check_admin()
    query = request.args.get('query')
    
    if not query:
        flash('Please enter a search query.')
        return redirect(url_for('admin.list_employees'))
    
    employees = Employee.query.filter(and_(Employee.email.contains(query),Employee.is_approved==True)).all()
    return render_template('admin/employees/employees.html', employees=employees)
       
@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

@admin.route('/employees/assign_task/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_task(id):
    """
    Assign a task to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from assigning a task to themselves
    if employee.is_admin:
        abort(403)

    form = TaskForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        if start_date < date.today():
            flash('Error: you cannot select a date that has passed')
            return redirect(url_for('admin.list_employees'))
        task = Task(name=form.name.data,
                    description=form.description.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    assigned_to=employee.id)
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('admin.list_employees'))

    # set the value of the assigned_to field to the employee's ID
    form.assigned_to.data = str(employee.id)

    return render_template('admin/employees/employee_assign_task.html',
                           employee=employee, form=form,
                           title='Assign Task')

@admin.route('/employees/profile/<int:id>',methods=['GET'])
@login_required
def employee_profile(id):
    """View employee from database"""
    check_admin()

    employee = Employee.query.get_or_404(id)

    return render_template('admin/employees/employee_profile.html',employee=employee,title='Employee Profile')

    

@admin.route('/employees/delete/<int:id>',methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """Delete employee from database"""
    check_admin()

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfuly deleted an employee.')

    #redirect to employees page
    return redirect(url_for("admin.list_employees"))


@admin.route('/employeesUnapproved')
@login_required
def list_employeesUnapproved():

    "List all unapproved employees"
    check_admin()

    employees = Employee.query.filter_by(is_approved=False).all()
    return render_template("admin/employees/employeesUnapproved.html",employees=employees)

@admin.route('/employeesUnapproved/approve/<int:id>')
@login_required
def approve_employee(id):

    employee = Employee.query.get(id)
    if employee:
        employee.is_approved = True
        db.session.commit()
        flash('Employee is approved')
    else:
        flash('Employee not found')
    return redirect(url_for("admin.list_employeesUnapproved"))

@admin.route('/employeesUnapproved/delete/<int:id>',methods=['GET', 'POST'])
@login_required
def delete_employeesUnapproved(id):
    "Delete employee from database"
    check_admin()

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfuly deleted an employee.')

    #redirect to employees page
    return redirect(url_for("admin.list_employeesUnapproved"))



#tasks

@admin.route('/tasks',methods=['GET'])
@login_required
def list_tasks():

    check_admin()

    tasks = Task.query.filter_by(approved=False).all()
    
    return render_template('admin/tasks/tasks.html', tasks=tasks)


    

@admin.route('/tasks/search')
@login_required
def search_tasks():

    check_admin()
    query = request.args.get('query')
    
    if not query:
        flash('Please enter a search query.')
        return redirect(url_for('admin.list_tasks'))
    
    tasks = Task.query.filter(Task.name.contains(query)).all()
    return render_template('admin/tasks/tasks.html', tasks=tasks)

@admin.route('tasks/accept/<int:id>',methods=['POST'])
@login_required
def accept_task(id):

    check_admin()
    task = Task.query.get(id)
    if task:
        task.approved =True
        db.session.commit()
        flash('Task has been accepted')
    else:
        flash('Task not found')
    return redirect(url_for('admin.list_tasks'))

@admin.route('tasks/reject/<int:id>',methods=['POST'])
@login_required
def reject_task(id):

    check_admin()
    task=Task.query.get(id)
    if task:
        task.completed = False
        db.session.commit()
        flash('Task has been rejected')
    else:
        flash('Task not found')
    return redirect(url_for('admin.list_tasks'))


#download





@admin.route('/download-tasks')
@login_required
def download_tasks():
    # Get the employee and task data
    tasks = Task.query.filter_by(approved=False).all()

    # Render the HTML template with the employee and task data
    html = render_template('admin/tasks/task_pdf.html',  tasks=tasks)

    # Create a PDF file from the rendered HTML
    pdf_file = BytesIO()
    pisa.CreatePDF(html, dest=pdf_file)

    # Create a response with the generated PDF file
    response = make_response(pdf_file.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=tasks.pdf'

    return response




@admin.route('/tasks_accepted',methods=['GET'])
@login_required
def list_completedTasks():

    check_admin()

    tasks = Task.query.filter_by(approved=True).all()
    return render_template('admin/tasks/taskCompleted.html',tasks=tasks)


#leave


@admin.route('/leave_request',methods=['GET'])
@login_required
def leave_request():

    check_admin()

    leaves = Leave.query.filter_by(approved=False).filter_by(disproved=False).all()

    return render_template('admin/leave/leave_requests.html',leaves=leaves)


@admin.route('/accept_leave/<int:id>',methods=['POST'])
@login_required
def accept_leave(id):

    check_admin()
    leave = Leave.query.get(id)
    if leave:
        leave.approved = True
        employee = Employee.query.get(leave.leave_assigned_to)

        employee.remaining_leave_days -= leave.leave_duration

        db.session.commit()
        flash('Leave was accepted')
    else:
        flash('No such leave')
    return redirect(url_for('admin.leave_request'))


@admin.route('/reject_leave/<int:id>',methods=['POST'])
@login_required
def reject_leave(id):

    check_admin()
    leave = Leave.query.get(id)
    if leave:
        leave.disproved = True
        db.session.commit()
        flash('Leave was rejected')
    else:
        flash('No such leave')
    return redirect(url_for('admin.leave_request'))


@admin.route('/list_accept_leave',methods=['GET'])
@login_required
def list_accept_leave():

    leaves = Leave.query.filter_by(approved=True).all()

    return render_template('admin/leave/leave_accept.html',leaves=leaves)



#packages



@admin.route('/packages', methods=['GET', 'POST'])
@login_required
def list_packages():
    """
    List all packages
    """
    check_admin()

    packages = Package.query.all()
    image_urls = {}
    for package in packages:
        if package.image:
            image_urls[package.id] = f'/static/img/{package.image}'

    print(image_urls)
    return render_template('admin/package/package_list.html',
                           packages=packages, title="Packages",image_urls=image_urls)

@admin.route('/packages/add', methods=['GET', 'POST'])
@login_required
def add_packages():
    """
    Add a packages to the database
    """
    check_admin()

    add_package = True

    form = PackageForm()
    if form.validate_on_submit():
        package = Package(name=form.name.data,
                                description=form.description.data)
        # handle the uploaded image file
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            package.image = filename
        try:
            # add package to the database
            db.session.add(package)
            db.session.commit()
            flash('You have successfully added a new package.')
        except:
            # in case package name already exists
            print("An exception occurred")
            flash('Error: package name already exists.')

        # redirect to packages page
        return redirect(url_for('admin.list_packages'))

    # load packages template
    return render_template('admin/package/package_add.html', action="Add",
                           add_package=add_package, form=form,
                           title="Add Package")

@admin.route('/packages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_package(id):
    """
    Edit a package
    """
    check_admin()

    add_package = False

    package = Package.query.get_or_404(id)
    form = PackageForm(obj=package)
    if form.validate_on_submit():
        print(f'form data: {form.data}')
        print(f'request.form: {request.form}')
        print(f'request.files: {request.files}')
        package.name = form.name.data
        package.description = form.description.data
         
        # handle the uploaded image file
        if form.image.data:
            print(f'form.image.data: {form.image.data}')
            image_file = form.image.data
            if isinstance(image_file, FileStorage):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                package.image = filename

        db.session.commit()
        flash('You have successfully edited the package.')

        # redirect to the packages page
        return redirect(url_for('admin.list_packages'))
    
    #generate image urls dictionary
    image_urls = {}
    if package.image:
        image_urls[package.id] = url_for('static',filename='img/'+package.image)

    print (image_urls)

    form.description.data = package.description
    form.name.data = package.name
    return render_template('admin/package/package_add.html', action="Edit",
                           add_package=add_package, form=form,
                           package=package, title="Edit Package")

@admin.route('/packages/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_package(id):
    """
    Delete a package from the database
    """
    check_admin()

    package = Package.query.get_or_404(id)
    db.session.delete(package)
    db.session.commit()
    flash('You have successfully deleted the package.')

    # redirect to the Packages page
    return redirect(url_for('admin.list_packages'))


# tea


@admin.route('/tea', methods=['GET', 'POST'])
@login_required
def list_teas():
    """
    List all teas
    """
    check_admin()

    teas = Tea.query.all()

    return render_template('admin/tea/tea_list.html',
                           teas=teas, title="Tea")

@admin.route('/tea/add', methods=['GET', 'POST'])
@login_required
def add_tea():
    """
    Add a tea to the database
    """
    check_admin()

    add_tea = True

    form = TeaForm()
    if form.validate_on_submit():
        tea = Tea(name=form.name.data,
                                description=form.description.data)
        try:
            # add tea to the database
            db.session.add(tea)
            db.session.commit()
            flash('You have successfully added a new tea variety.')
        except:
            # in case tea variety already exists
            flash('Error: tea variety already exists.')

        # redirect to teas page
        return redirect(url_for('admin.list_teas'))

    # load tea template
    return render_template('admin/tea/tea_add.html', action="Add",
                           add_tea=add_tea, form=form,
                           title="Add Tea")

@admin.route('/tea/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tea(id):
    """
    Edit a tea variety
    """
    check_admin()

    add_tea = False

    tea = Tea.query.get_or_404(id)
    form = TeaForm(obj=tea)
    if form.validate_on_submit():
        tea.name = form.name.data
        tea.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the tea variety.')

        # redirect to the tea page
        return redirect(url_for('admin.list_teas'))

    form.description.data = tea.description
    form.name.data = tea.name
    return render_template('admin/tea/tea_add.html', action="Edit",
                           add_tea=add_tea, form=form,
                           tea=tea, title="Edit Tea")

@admin.route('/tea/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_tea(id):
    """
    Delete a tea variety from the database
    """
    check_admin()

    tea = Tea.query.get_or_404(id)
    db.session.delete(tea)
    db.session.commit()
    flash('You have successfully deleted the tea variety.')

    # redirect to the tea page
    return redirect(url_for('admin.list_teas'))

    
    
#products

@admin.route('/products', methods=['GET', 'POST'])
@login_required
def list_products():
    """
    List all products
    """
    check_admin()

    products = Product.query.all()
    print(f'Products: {products}')
    image_urls = {}
    for product in products:
        if product.image_path:
            image_urls[product.id] = f'/static/img/{product.image_path}'

    print(image_urls)
    return render_template('admin/product/product_list.html',
                           products=products, title="Products",image_urls=image_urls)

@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_products():
    """
    Add a products to the database
    """
    check_admin()

    add_product = True

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
                          count=form.count.data,
                          cost_usd = form.cost.data,
                          package_id = form.package.data.id,
                          tea_id = form.tea.data.id)
        # handle the uploaded image file
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            product.image_path = filename
        # print product details
        print(f'Product details: {product.__dict__}')
        try:
            # add product to the database
            db.session.add(product)
            db.session.commit()
            flash('You have successfully added a new product.')
        except Exception as e:
            # in case product name already exists
            flash('Error: product name already exists.')
            # print error details
            print(f'Error details: {e}')

        # redirect to product page
        return redirect(url_for('admin.list_products'))

    # load product template
    return render_template('admin/product/product_add.html', action="Add",
                           add_product=add_product, form=form,
                           title="Add Product")

@admin.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_products(id):
    """
    Edit a products
    """
    check_admin()

    add_product = False

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.count = form.count.data
        product.cost_usd = form.cost.data
        product.package_id = form.package.data.id
        product.tea_id = form.tea.data.id
         # handle the uploaded image file
        if form.image.data:
            image_file = form.image.data
            if isinstance(image_file, FileStorage):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                product.image_path = filename
        db.session.commit()
        flash('You have successfully edited the product.')

        # redirect to the products page
        return redirect(url_for('admin.list_products'))
    
    #generate image urls dictionary
    image_urls = {}
    if product.image_path:
        image_urls[product.id] = url_for('static',filename='img/'+product.image_path)

    print (image_urls)

    form.name.data = product.name
    form.count.data = product.count
    form.cost.data = product.cost_usd
    form.package.data = product.package_id
    form.tea.data = product.tea_id
    return render_template('admin/product/product_add.html', action="Edit",
                           add_product=add_product, form=form,
                           product=product, title="Edit Product")

@admin.route('/products/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    """
    Delete a product from the database
    """
    check_admin()

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('You have successfully deleted the product.')

    # redirect to the products page
    return redirect(url_for('admin.list_products'))

@admin.route('/customers',methods=['GET'])
@login_required
def list_customers():
    """
    List customers
    """
    check_admin()

    customers = Customer.query.filter_by(email_verified=True).all()
    return render_template('admin/customer/customer_list.html',customers=customers,Title="Customer")

@admin.route('/customers/add_orders/<int:id>',methods=['GET','POST'])
@login_required
def new_order(id):

    print(f"request method:{request.method}")
    print(f"form data:{request.form}")

    """add orders"""
    print("new order function called")
    customer = Customer.query.get_or_404(id)

    form = OrderForm()
    print(f"Form data:{form.data}")
    if form.validate_on_submit():
        print("form validated and submitted")
        product = Product.query.filter_by(name=form.product.data.name).first()
        print(f"Selcted product:{product}")
        total_cost = product.cost_usd * form.count.data
        order = Order(customer=customer,
                      product=product,
                      count=form.count.data,
                      total_cost=total_cost)
        db.session.add(order)
        print(f"{order}")
        db.session.commit()
        product.count -= form.count.data
        db.session.commit()
        flash('Order sucessfully created')
        return redirect(url_for('admin.list_customers'))
    else:
        print(f"form errors:{form.errors}")
    return render_template('admin/customer/customer_orders.html',customer=customer,form=form)


@admin.route('/customer/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_customer(id):
    """
    Delete a product from the database
    """
    check_admin()

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('You have successfully deleted the customer.')

    # redirect to the customers page
    return redirect(url_for('admin.list_customers'))

@admin.route('/order',methods=['GET'])
@login_required
def list_orders():
    """
    orders list
    """
    orders = Order.query.all()
    return render_template('admin/order/order_list.html',orders=orders,Title="Order")