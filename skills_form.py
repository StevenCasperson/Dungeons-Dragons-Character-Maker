from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class SkillsForm(FlaskForm):
    skills = SelectMultipleField(
        "Choose exactly 2 proficiencies",
        choices=[],  # overridden in __init__
        validators=[DataRequired(message="Pick two skills.")]
    )
    submit = SubmitField("Confirm Fighter Details")

    def __init__(self, allowed_skills, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Build choices from allowed_skills list
        self.skills.choices = [(s, s) for s in allowed_skills]

    def validate_skills(self, field):
        if len(field.data) != 2:
            raise ValidationError("You must pick exactly two skills.")
