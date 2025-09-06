from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class ClassForm(FlaskForm):
    class_choice = SelectField("Choose your class", choices=[])
    submit       = SubmitField("Confirm Fighter Details")

    def __init__(self, classes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_choice.choices = [(c, c) for c in classes]
