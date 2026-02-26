# from Ankimon import settings_obj
# from abcdf import module1 

from PyQt5 import QtWebEngineWidgets
import pytest
from pytest_anki import AnkiSession

@pytest.mark.forked
def test_my_addon(anki_session: AnkiSession):
    with anki_session.profile_loaded():
        assert anki_session.collection


"""
import os
os.environ["TESTING"] = "1"

# conftest.py
from unittest.mock import MagicMock
import sys

# Block aqt and anki modules entirely before any addon code is imported
sys.modules['aqt.qt'] = MagicMock()
sys.modules['aqt.utils'] = MagicMock()
sys.modules['anki.hooks'] = MagicMock()

from unittest.mock import Mock
import aqt

from PyQt6.QtWidgets import QApplication
print(QApplication.instance())

aqt.mw = Mock()
aqt.mw.pm = Mock()
aqt.mw.pm.name = "TestProfile"

# Runs __init__ file in package Ankimon
# pyobj is treated as a namespace package
# Finally Pokemon Obj is pulled from module namespace
from Ankimon.pyobj.pokemon_obj import PokemonObject 

#def test_some_stuff():
#   print(module1.add(5, 15))    # Output: 20
#   module1.odd_even(6)          # Output: Even

def test_pkmn_single_evolution_by_lvl():

    pokemon: PokemonObject = PokemonObject()

    pokemon_data = {
        'name': "grookey",
        'id': 810,
        'level': 20,
        'ability': "Overgrow",
        'type':  ["Grass"],
        'base_stats': {
            "hp": 50,
            "atk": 65,
            "def": 50,
            "spa": 40,
            "spd": 40,
            "spe": 65
        },
        'attacks': ["razorleaf", "branchpoke"],
        'base_experience': 62,
        'growth_rate': "medium-slow",
        'ev': {
            "hp": 2,
            "atk": 2,
            "def": 0,
            "spa": 0,
            "spd": 2,
            "spe": 1
        },
        'iv': {
            "hp": 29,
            "atk": 9,
            "def": 26,
            "spa": 9,
            "spd": 20,
            "spe": 25
        },
        'gender': "F",
        # 'battle_status': battle_status,
        # 'battle_stats': battle_stats,
        'stat_stages': {'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0, 'accuracy': 0, 'evasion': 0},
        'tier': "Normal",
        # 'ev_yield': ev_yield,
        'shiny': False
    }

    pokemon.update_stats(**pokemon_data)

    print(pokemon)

"""
"""

update_stats()

{
    "nickname": "Grookey",

    "stats": {
      "hp": 58,
      "atk": 34,
      "def": 31,
      "spa": 23,
      "spd": 26,
      "spe": 37
    },

    
    "everstone": false,

    "captured_date": "2026-02-12 12:00:00",
    "individual_id": "defb9044-ebcb-4b05-ad8e-63f483eed207",
    "mega": false,
    "special_form": null,
    "xp": 152,
    "hp": 58,
    "friendship": 34,
    "pokemon_defeated": 5,
    "is_favorite": false,
    "current_hp": 1,
    "held_item": null
  },

"""