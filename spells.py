# app/data/spells.py

# ————— Wizard Cantrips —————
cantrips = [
    ("acid_splash",     "Acid Splash"),
    ("blade_ward",      "Blade Ward (Concentration)"),
    ("chill_touch",     "Chill Touch"),
    ("dancing_lights",  "Dancing Lights (Concentration)"),
    ("elementalism",    "Elementalism"),
    ("fire_bolt",       "Fire Bolt"),
    ("friends",         "Friends (Concentration)"),
    ("light",           "Light"),
    ("mage_hand",       "Mage Hand"),
    ("mending",         "Mending"),
    ("message",         "Message"),
    ("mind_sliver",     "Mind Sliver"),
    ("minor_illusion",  "Minor Illusion"),
    ("poison_spray",    "Poison Spray"),
    ("prestidigitation","Prestidigitation"),
    ("ray_of_frost",    "Ray of Frost"),
    ("shocking_grasp",  "Shocking Grasp"),
    ("thunderclap",     "Thunderclap"),
    ("toll_the_dead",   "Toll the Dead"),
    ("true_strike",     "True Strike"),
]

# ————— 1st-Level Wizard Spells —————
level1_spells = [
    ("alarm",                          "Alarm"),
    ("burning_hands",                  "Burning Hands"),
    ("charm_person",                   "Charm Person"),
    ("chromatic_orb",                  "Chromatic Orb"),
    ("color_spray",                    "Color Spray"),
    ("comprehend_languages",           "Comprehend Languages"),
    ("detect_magic",                   "Detect Magic"),
    ("disguise_self",                  "Disguise Self"),
    ("expeditious_retreat",            "Expeditious Retreat"),
    ("false_life",                     "False Life"),
    ("feather_fall",                   "Feather Fall"),
    ("find_familiar",                  "Find Familiar"),
    ("fog_cloud",                      "Fog Cloud"),
    ("grease",                         "Grease"),
    ("ice_knife",                      "Ice Knife"),
    ("identify",                       "Identify"),
    ("illusory_script",                "Illusory Script"),
    ("jump",                           "Jump"),
    ("longstrider",                    "Longstrider"),
    ("mage_armor",                     "Mage Armor"),
    ("magic_missile",                  "Magic Missile"),
    ("protection_from_evil_and_good",  "Protection from Evil and Good"),
    ("ray_of_sickness",                "Ray of Sickness"),
    ("shield",                         "Shield"),
    ("silent_image",                   "Silent Image"),
    ("sleep",                          "Sleep"),
    ("tashas_hideous_laughter",        "Tasha's Hideous Laughter"),
    ("tensers_floating_disk",          "Tenser's Floating Disk"),
    ("thunderwave",                    "Thunderwave"),
    ("unseen_servant",                 "Unseen Servant"),
    ("witch_bolt",                     "Witch Bolt"),
]

# ————— Cleric Cantrips —————
# (key, label, requires_concentration)
cleric_cantrips = [
    ("guidance",          "Guidance",          True),
    ("light",             "Light",             False),
    ("mending",           "Mending",           False),
    ("resistance",        "Resistance",        True),
    ("sacred_flame",      "Sacred Flame",      False),
    ("spare_the_dying",   "Spare the Dying",   False),
    ("thaumaturgy",       "Thaumaturgy",       False),
    ("toll_the_dead",     "Toll the Dead",     False),
    ("word_of_radiance",  "Word of Radiance",  False),
]

# ————— 1st-Level Cleric Spells —————
level1_cleric_spells = [
    ("bane",                          "Bane"),
    ("bless",                         "Bless"),
    ("command",                       "Command"),
    ("create_or_destroy_water",       "Create or Destroy Water"),
    ("cure_wounds",                   "Cure Wounds"),
    ("detect_evil_and_good",          "Detect Evil and Good"),
    ("detect_magic",                  "Detect Magic"),
    ("detect_poison_and_disease",     "Detect Poison and Disease"),
    ("guiding_bolt",                  "Guiding Bolt"),
    ("healing_word",                  "Healing Word"),
    ("inflict_wounds",                "Inflict Wounds"),
    ("protection_from_evil_and_good", "Protection from Evil and Good"),
    ("purify_food_and_drink",         "Purify Food and Drink"),
    ("sanctuary",                     "Sanctuary"),
    ("shield_of_faith",               "Shield of Faith"),
]
