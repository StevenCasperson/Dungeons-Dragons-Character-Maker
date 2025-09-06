import random

from flask import Blueprint, render_template, request, redirect, url_for, session

# ← Changed imports to relative paths within dnd_builder
from .forms.equipment_form import EquipmentForm
from .data.equipment       import equipment_list
from .data.spells          import level1_spells, cleric_cantrips, level1_cleric_spells
from .forms.skills_form import SkillsForm
from .data.class_skills      import CLASS_SKILLS
from .utils import calc_spell_save_dc, calc_spell_attack_bonus
#from .forms.race_form       import RaceForm
from .forms.class_form      import ClassForm

bp = Blueprint("characters", __name__, url_prefix="/characters")


# ————— Constants —————

ABILITY_LABELS = [
    "Strength", "Dexterity", "Constitution",
    "Intelligence", "Wisdom", "Charisma"
]

RACIAL_BONUSES = {
    "Elf":      {"dexterity": 2, "charisma": 1},
    "Dwarf":    {"constitution": 2, "strength": 1},
    "Halfling": {"dexterity": 2, "constitution": 1},
    "Human":    {}
}

CLASS_FEATURES = {
    "Cleric": ["Spellcasting", "Divine Order"],
    "Fighter": ["Fighting Style", "Second Wind", "Weapon Mastery"],
    "Rogue": ["Expertise", "Sneak Attack", "Thieves' Cant", "Weapon Mastery"],
    "Wizard": ["Spellcasting", "Ritual Adept", "Arcane Recovery"],
}

FIGHTING_STYLES = [
    "Archery",
    "Blind Fighting",
    "Defense",
    "Dueling",
    "Great Weapon Fighting",
    "Interception",
    "Protection",
    "Thrown Weapon Fighting",
    "Two-Weapon Fighting",
    "Unarmed Fighting",
]

# Map each skill to its governing ability (3-letter key)
SKILL_ABILITIES = {
    "Athletics":               "str",
    "Acrobatics":              "dex",
    "Sleight of Hand":         "dex",
    "Stealth":                 "dex",
    "Arcana":                  "int",
    "History":                 "int",
    "Investigation":           "int",
    "Nature":                  "int",
    "Religion":                "int",
    "Animal Handling":         "wis",
    "Insight":                 "wis",
    "Medicine":                "wis",
    "Perception":              "wis",
    "Survival":                "wis",
    "Deception":               "cha",
    "Intimidation":            "cha",
    "Performance":             "cha",
    "Persuasion":              "cha",
}

COIN_VALUES = {"pp": 500, "gp": 100, "sp": 10, "cp": 1}
PROFICIENCY_BONUS = 2


# ————— Helpers —————

def roll_stat():
    """Roll 4d6, drop the lowest."""
    rolls = sorted(random.randint(1, 6) for _ in range(4))
    return sum(rolls[1:])


def coins_to_cp(coins: dict) -> int:
    """Convert a coin-dict to total copper pieces."""
    return sum(COIN_VALUES[d] * count for d, count in coins.items())


def cp_to_coins(cp_total: int) -> dict:
    """Convert a copper total back into a coin-dict."""
    rem = cp_total
    result = {}
    for denom in ("pp", "gp", "sp", "cp"):
        result[denom], rem = divmod(rem, COIN_VALUES[denom])
    return result


# ————— Step 1: Roll Ability Scores —————

@bp.route("/step1", methods=["GET", "POST"])
def step1_abilities():
    if request.method == "POST":
        session.clear()
        session["stats"] = {
            lbl.lower(): roll_stat() for lbl in ABILITY_LABELS
        }
        session["coins_left"] = {"gp": 100}
        return redirect(url_for("characters.step1_abilities"))

    return render_template(
        "index.html",
        labels=ABILITY_LABELS,
        stats=session.get("stats", {})
    )


# ————— Step 2: Choose Race —————

@bp.route("/step2_race", methods=["GET", "POST"])
def step2_race():
    if request.method == "POST":
        race = request.form["race"]
        session["race"] = race

        base = session["stats"].copy()
        bonuses = RACIAL_BONUSES.get(race, {})
        session["adjusted_stats"] = {
            k: base[k] + bonuses.get(k, 0) for k in base
        }

        return redirect(url_for("characters.step2_race_summary"))

    return render_template(
        "race.html",
        races=list(RACIAL_BONUSES.keys())
    )


@bp.route("/step2_race_summary")
def step2_race_summary():
    return render_template(
        "race_summary.html",
        labels=ABILITY_LABELS,
        base_stats=session.get("stats", {}),
        adjusted_stats=session.get("adjusted_stats", {}),
        race=session.get("race")
    )


# ————— Step 3: Choose Class —————

@bp.route("/step3_class", methods=["GET", "POST"])
def step3_class():
    classes = ["Fighter", "Wizard", "Rogue", "Cleric"]
    form = ClassForm()
    if form.validate_on_submit():
        # This line is critical:
        session["class"] = form.class_choice.data  # or form.selected_class.data
        return redirect(url_for("characters.step4_skills"))
    return render_template("step3_class.html", form=form)
    if request.method == "POST":
        session["class"] = request.form["class"]
        return redirect(url_for("characters.step4_class"))
    return render_template("class.html", classes=classes)


# ————— Step 4: Class-Specific Details —————

@bp.route("/step4_class", methods=["GET", "POST"])
def step4_class():
    char_class = session.get("class")
    if not char_class:
        return redirect(url_for("characters.step3_class"))

    if char_class == "Fighter":
        if request.method == "POST":
            session["primary_ability"]     = request.form["primary_ability"]
            session["skill_proficiencies"] = request.form.getlist("skills")
            session["fighting_style"]      = request.form["fighting_style"]
            return redirect(url_for("characters.step5_equipment"))

        return render_template(
            "class_fighter.html",
            primary_abilities=ABILITY_LABELS,
            skills=list(SKILL_ABILITIES.keys()),
            fighting_styles=FIGHTING_STYLES
        )

    if char_class == "Wizard":
        spell_labels = [label for _, label in level1_spells]
        return render_template(
            "spells.html",
            char_class="Wizard",
            spells=spell_labels
        )

    if char_class == "Cleric":
        labels = [label for _, label, _ in cleric_cantrips]
        return render_template(
            "spells.html",
            char_class="Cleric",
            spells=labels
        )

    return redirect(url_for("characters.step5_equipment"))

@bp.route("/step4_skills", methods=["GET", "POST"])
def step4_skills():
    chosen_class = session.get("class")
    allowed = CLASS_SKILLS.get(chosen_class, [])

    form = SkillsForm(allowed_skills=allowed)
    if form.validate_on_submit():
        # Save exactly the two chosen skills
        session["skills"] = form.skills.data
        return redirect(url_for("characters.step5_equipment"))

    return render_template(
        "step4_skills.html",
        form=form,
        chosen_class=chosen_class
    )
    
# ————— Step 5: Buy Equipment —————
@bp.route("/step5_equipment", methods=["GET", "POST"])
def step5_equipment():
    form = EquipmentForm()

    # Handle form submission
    if form.validate_on_submit():
        # … your purchase logic here, e.g. update session…
        return redirect(url_for("characters.step5_equipment"))

    # Build a list of (label, field) for templating
    fields = [
        (item["label"], getattr(form, item["key"]))
        for item in EQUIPMENT_LIST
    ]

    # Render with every argument separated by commas
    return render_template(
        "step5_equipment.html",
        form=form,
        fields=fields,
        coins_left=session.get("coins_left", {})
    )

# ————— Step 6: Summary & “Begin Adventure” —————

@bp.route("/step6_summary")
def step6_summary():
    if "stats" not in session or "class" not in session:
        return redirect(url_for("characters.step1_abilities"))

    # Equipment details
    details = []
    for name, qty in session.get("equipment", {}).items():
        if qty:
            details.append({"name": name})

    # Core stats & modifiers
    stats      = session.get("adjusted_stats", session.get("stats"))
    int_mod    = (stats.get("intelligence", 0) - 10) // 2
    wis_mod    = (stats.get("wisdom",       0) - 10) // 2
    prof_bonus = PROFICIENCY_BONUS

    char_class = session.get("class")
    cast_mod   = int_mod if char_class == "Wizard" \
               else wis_mod if char_class == "Cleric" \
               else 0

    # Build ability mods & skill mods
    ability_mods = {
        abbr: (score - 10) // 2
        for abbr, score in stats.items()
    }

    profs = set(session.get("skill_proficiencies", []))
    skills_mods = []
    for skill, abbr in SKILL_ABILITIES.items():
        base_mod  = ability_mods[abbr]
        total_mod = base_mod + (prof_bonus if skill in profs else 0)
        skills_mods.append({
            "name":       skill,
            "abbr":       abbr,
            "mod":        total_mod,
            "proficient": skill in profs
        })

    return render_template(
        "summary.html",
        race               = session.get("race"),
        char_class         = char_class,
        class_features     = CLASS_FEATURES.get(char_class, []),
        primary_ability    = session.get("primary_ability"),
        skill_proficiencies = session.get("skill_proficiencies", []),
        fighting_style     = session.get("fighting_style"),
        stats              = stats,
        equipment_details  = details,
        coins_left         = session.get("coins_left", {}),
        prof_bonus         = prof_bonus,
        cast_mod           = cast_mod,
        skills_mods        = skills_mods
    )
