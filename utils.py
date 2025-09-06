# dnd_builder/utils.py

def calc_spell_save_dc(cast_mod: int, prof_bonus: int) -> int:
    """
    Spell Save DC = 8 + proficiency bonus + casting ability modifier
    """
    return 8 + prof_bonus + cast_mod


def calc_spell_attack_bonus(cast_mod: int, prof_bonus: int) -> int:
    """
    Spell Attack Bonus = proficiency bonus + casting ability modifier
    """
    return prof_bonus + cast_mod
