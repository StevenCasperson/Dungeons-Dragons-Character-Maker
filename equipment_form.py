from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from dnd_builder.data.equipment import equipment_list
# dnd_builder/forms/equipment_form.py
from ..data.equipment import equipment_list

class EquipmentForm(FlaskForm):
    budget = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Next")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in equipment_list:
            key = item["key"]
            if item.get("options"):
                choices = [("", "-- none --")] + [
                    (o["key"], o["label"]) for o in item["options"]
                ]
                setattr(self, key, SelectField(item["label"], choices=choices))
            else:
                setattr(self, key, BooleanField(item["label"]))

    def validate(self):
        if not super().validate():
            return False

        total = 0.0
        for item in equipment_list:
            field = getattr(self, item["key"])
            if isinstance(field.data, bool) and field.data:
                total += item["cost"]
            elif isinstance(field.data, str) and field.data:
                opt = next(o for o in item["options"] if o["key"] == field.data)
                total += opt["cost"]

        budget = float(self.budget.data or 0)
        if total > budget:
            self.budget.errors.append(f"Spent {total} gp, only have {budget} gp")
            return False

        self.selected_items = {
            item["key"]: getattr(self, item["key"]).data
            for item in equipment_list
        }
        return True
