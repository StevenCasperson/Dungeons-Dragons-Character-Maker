from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, ValidationError
from wtforms.validators import DataRequired
# dnd_builder/forms/spell_form.py
from ..data.spells import level1_spells, cleric_cantrips, level1_cleric_spells

class SpellForm(FlaskForm):
    cantrips = SelectMultipleField(
        "Choose 3 Known Cantrips",
        choices=cantrips,
        validators=[DataRequired()]
    )
    spellbook = SelectMultipleField(
        "Add 6 Spells to Your Spellbook",
        choices=level1_spells,
        validators=[DataRequired()]
    )
    submit = SubmitField("Next")

    def validate_cantrips(self, field):
        if len(field.data) != 3:
            raise ValidationError("You must select exactly 3 cantrips.")

    def validate_spellbook(self, field):
        if len(field.data) != 6:
            raise ValidationError("You must add exactly 6 spells.")
