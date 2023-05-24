# app/auth/views.py

from flask import flash, redirect, render_template, url_for, current_app
from flask_login import login_required, login_user, logout_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db,mail
from ..models import Employee, Customer



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.user_type.data == 'employee':
            user = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        else:
            user = Customer(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add user to the database
        db.session.add(user)
        db.session.commit()

        # send email verification link if user is a customer
        if isinstance(user, Customer):
            # generate token
            ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = ts.dumps(user.email, salt='email-confirm-key')

            # generate verification link
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)

            # create email message
            subject = 'Please confirm your email'
            sender = current_app.config['MAIL_DEFAULT_SENDER']
            recipients = [user.email]
            body = f'Please click on the following link to verify your email: {confirm_url}'
            msg = Message(subject, sender=sender, recipients=recipients, body=body)

            # send email
            mail.send(msg)

        flash('You have successfully registered! Please check your email for a verification link.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/confirm-email/<token>')
def confirm_email(token):
    # create serializer
    ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    # load token
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=86400)
    except SignatureExpired:
        flash('The email verification link has expired.')
        return redirect(url_for('auth.login'))

    # verify email
    user = Customer.query.filter_by(email=email).first()
    if user is not None:
        user.email_verified = True
        db.session.commit()
        flash('Your email has been verified! You can now log in.')
    else:
        flash('Invalid email verification link.')

    # redirect to login page
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = Employee.query.filter_by(email=form.email.data).first() or Customer.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # Check if user is approved or email verified
            if isinstance(user, Customer) and not user.email_verified:
                flash('Please verify your email before logging in.')
            elif isinstance(user, Employee) and (not user.is_admin and not user.is_approved):
                flash('Your account has not been approved yet.')
            else:
                # log user in
                login_user(user)

                # redirect to the appropriate dashboard page after login
                if hasattr(user, 'is_admin') and user.is_admin:
                    return redirect(url_for('home.admin_dashboard'))
                elif isinstance(user, Customer):
                    return redirect(url_for('home.customer_dashboard'))
                else:
                    return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

    # load login template
   # return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))