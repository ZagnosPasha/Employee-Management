from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField, IntegerField
from wtforms.validators import DataRequired, ValidationError,NumberRange,Length,Regexp

class EmployeeProfileForm(FlaskForm):

    "Forms for employees to submit phone_number and adress and update them"

    phone_number = StringField('Phone Number',validators =[DataRequired(),Length(max=10),Regexp('^[0-9]*$',message='Phone number must only contain digits')])
    address = StringField('Address',validators = [DataRequired()])
    submit = SubmitField('Update')

class LeaveForm(FlaskForm):

    "Forms for employees to submit leave"

    reason = StringField('Reason',validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    duration = IntegerField('Duration',validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Submit')

    def validate_duration(self, field):
        # Get current user from Flask
        employee = current_user

        # Print the value of employee
        print(f"employee: {employee}")

        # Get employee remaining leave days
        remaining_days = employee.remaining_leave_days

        # Print the value of employee.remaining_leave_days and remaining_days
        print(f"employee.remaining_leave_days: {employee.remaining_leave_days}")
        print(f"remaining_days: {remaining_days}")

        # Check for duration
        if field.data > 3:
            raise ValidationError('Duration cannot exceed 3 days')
    
        if field.data > remaining_days:
            raise ValidationError('Duration cannot exceed remaining leave days')


