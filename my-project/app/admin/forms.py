from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,SelectMultipleField,HiddenField,DateField,IntegerField
from wtforms.validators import DataRequired, ValidationError,NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget
from flask_wtf.file import FileField, FileAllowed

from ..models import Department, Role, Employee,Package,Tea,Product


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

    def iter_choices(self):
        for value, label in self.choices:
            selected = self.data is not None and self.coerce(value) in self.data
            yield (value, label, selected)

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [self.coerce(value) for value in valuelist]
        else:
            self.data = []

    def pre_validate(self, form):
        if self.data:
            values = list(c[0] for c in self.choices)
            for d in self.data:
                if d not in values:
                    raise ValueError(self.gettext('Not a valid choice'))


""" class FlatpickrDatePickerField(StringField):
    
    Custom form field for a Flatpickr date picker.
    

    def __init__(self, label='', validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)

    def _value(self):
        
        Override the default value getter to return a formatted date string.
        
        if self.data:
            return self.data.strftime('%Y-%m-%d')
        else:
            return ''

    def process_formdata(self, valuelist):
        
        Override the default form data processing to parse the date string
        into a datetime object.
        
        super().process_formdata(valuelist)
        if self.data:
            self.data = datepicker.parse(self.data) """


class TaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired()])
    description = TextAreaField('Task Description', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    assigned_to = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Create Task')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        if self.start_date.data > self.end_date.data:
            self.end_date.errors.append('End date must be after or on start date')
            return False
        return True


class PackageForm(FlaskForm):
    """
    Form for admin to add or edit a package
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')



class TeaForm(FlaskForm):
    """
    Form for admin to add or edit a tea variety
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProductForm(FlaskForm):
    """
    Form for admin to add or edit a package
    """
    name = StringField('Name', validators=[DataRequired()])
    
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    package = QuerySelectField(query_factory=lambda: Package.query.all(),
                                  get_label="name")
    tea = QuerySelectField(query_factory=lambda: Tea.query.all(),
                            get_label="name")
    count = IntegerField('Count', validators=[NumberRange(min=0)])
    cost = IntegerField('Cost (USD)', validators=[NumberRange(min=0)])
    submit = SubmitField('Submit')

class OrderForm(FlaskForm):
    """
    Form for admin to add order
    """

    product = QuerySelectField(query_factory=lambda: Product.query.all(),get_label='name', validators=[DataRequired()])
    count = IntegerField('Count',validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_count(self,field):
        if field.data <=0:
            raise ValidationError('Count must be a positive value')
        product = Product.query.filter_by(name=self.product.data.name).first()
        if field.data>product.count:
            print(f"Validation error: count({field.data}) is greater than product count({product.count})")
            raise ValidationError('You cannot order this much.')
        
   