from flask import render_template, request, flash,redirect,url_for
from flask_login import login_required, current_user
from .. import db
from ..models import Employee, Task, Leave,Customer
from .forms import EmployeeProfileForm, LeaveForm
from . import employees
from datetime import date

@employees.route('/profile', methods=['GET', 'POST'])
@login_required
def employee_profile():
    employee = Employee.query.filter_by(id=current_user.id).first()
    form = EmployeeProfileForm(obj=employee)
    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        flash('Your profile has been updated.')
    else:
        for field,errors in form.errors.items():
            for error in errors:
                flash(error)
    return render_template('employee/employee_profile.html', employee=employee, form=form, title="Profile",Customer=Customer)

@employees.route('/view_tasks', methods=['GET'])
@login_required
def employee_tasks():
    employee = Employee.query.filter_by(id=current_user.id).first()
    tasks = Task.query.filter_by(assigned_to=employee.id,in_progress=False).all()

    return render_template('employee/employee_task.html', tasks=tasks,Customer=Customer)

@employees.route('/view_tasks/submit/<int:id>',methods=['POST'])
@login_required
def employee_tasksSubmit(id):
    task=Task.query.get(id)
    if task:
        task.completed = True
        db.session.commit()
        flash('Task has been succesfuly submitted')
    else:
        flash('Task was not found')
    return redirect(url_for('employees.employee_tasks'))

@employees.route('/view_tasks/complete/<int:id>',methods=['POST'])
@login_required
def employee_tasksComplete(id):
    
    task= Task.query.get(id)
    if task:
        task.in_progress = True
        db.session.commit()
        flash('Task has been successfully completed')
    else:
        flash('Task was not found')
    return redirect(url_for('employees.employee_tasks'))

@employees.route('/task_complete',methods=['GET'])
@login_required
def list_completeTasks():

    employee = Employee.query.filter_by(id=current_user.id).first()
    tasks = Task.query.filter_by(assigned_to=employee.id,in_progress=True).all()

    return render_template('employee/employee_taskComplete.html',tasks=tasks,Customer=Customer)

@employees.route('/list_leave',methods=['GET'])
@login_required
def list_employee_leaves():

    employee = Employee.query.filter_by(id=current_user.id).first()
    leaves = Leave.query.filter_by(leave_assigned_to=employee.id,approved=False).all()

    return render_template('employee/employee_listLeave.html',leaves=leaves,Customer=Customer)
@employees.route('/request_leave',methods=['GET','POST'])
@login_required
def request_leave():
    employee = Employee.query.filter_by(id=current_user.id).first()
    form = LeaveForm()
    if form.validate_on_submit():
        leave_date = form.start_date.data
        if leave_date < date.today():
            flash('Error: You cannot select a past date for leave')
            return redirect(url_for('employees.list_employee_leaves'))
        #check if employees have already requested that leave date
        existing_leave = Leave.query.filter_by(leave_assigned_to=current_user.id,leave_date=leave_date).first()
        if existing_leave:
            flash('Error: You have already submitted a leave request for selected date')
            return redirect(url_for('employees.list_employee_leaves'))
        #code when leave is not same
        leave = Leave(reason=form.reason.data,
                      leave_date=form.start_date.data,
                      leave_duration = form.duration.data,
                      leave_assigned_to = current_user.id,
                      submitted = True)
        try:
            db.session.add(leave)
            db.session.commit()
            flash('Your leave request has been submitted for approval')
        except:
            flash('Error: You have already submitted for selected leave date ')
        return redirect(url_for('employees.list_employee_leaves'))
    return render_template('employee/request_leave.html',form=form,employee=employee,Customer=Customer)

@employees.route('/accept_leave',methods=['GET'])
@login_required
def accept_leave():

    employee = Employee.query.filter_by(id=current_user.id).first()
    leaves = Leave.query.filter_by(leave_assigned_to=employee.id,approved=True).all()

    return render_template('employee/accept_leave.html',leaves=leaves,Customer=Customer)

@employees.route('/delete_leave/<int:id>',methods=['GET','POST'])
@login_required
def delete_leave(id):

    leaves = Leave.query.get_or_404(id)
    db.session.delete(leaves)
    db.session.commit()
    flash('You have successfully deleted the leave.')

    # redirect to the leavess page
    return redirect(url_for('employees.list_employee_leaves'))
    


