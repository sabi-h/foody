from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class TagForm(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired(), Length(min=2, max=256)])
    product_category = StringField("Product Category", validators=[DataRequired()])
    serving_size = IntegerField("Serving Size (g)")
    # description = StringField('Description', validators=[Length(max=2047)])
    # source_location_name = StringField('Source Location Name', validators=[Length(max=20)])
    # source_location_address = StringField('Source Location Address', validators=[Length(max=511)])
    # farmed_date = DateField('Farmed Date')
    submit = SubmitField("Create")
