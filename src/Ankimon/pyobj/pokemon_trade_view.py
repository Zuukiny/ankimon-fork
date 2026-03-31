import json
import string
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtGui import QPixmap, QFont, QIcon, QColor, QMovie, QImage
from PyQt6.QtCore import QSize, Qt

from aqt import mw
from aqt import QBoxLayout

from ..functions.sprite_functions import get_sprite_path

if TYPE_CHECKING: 
    from ..pyobj.pokemon_trade import PokemonTrade

class PokemonTradeView():
    PKMN_SPRITE_SIZE = QSize(64, 64)

    def __init__(self, controller: 'PokemonTrade', pokemon: dict, moves_file_path, parent_window=None):
        self.controller = controller
        self.pokemon_to_trade = pokemon # temporary
        self.moves_file_path = moves_file_path # temporary
        self.parent_window = parent_window
    
    def open_trade_window(self):

        # Window Details
        parent = self.parent_window if self.parent_window is not None else mw
        window = QDialog(parent)
        window.setWindowTitle(f"Trade Pokémon: {string.capwords(self.pokemon_to_trade['name'])}")
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        window.setMinimumSize(380, 400)

        main_layout = QVBoxLayout(window)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Trade Caption
        title_label = QLabel(f"Trading Away: {string.capwords(self.pokemon_to_trade['name'])}")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Trade Window Contents
        sprite_layout = self._setup_trade_pokemon_layout()
        main_layout.addLayout(sprite_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        code_layout = self._setup_trade_code_layout(window)
        main_layout.addLayout(code_layout)

        window.exec()

    def _setup_trade_pokemon_layout(self) -> QBoxLayout:
        # TODO: Rename your --> my and other --> their

        """ 
        Returns Sprite Layout
        """
        
        sprites_layout = QHBoxLayout()
        sprites_layout.setSpacing(20)

        # Pokemon To Trade
        
        my_pokemon_sprite_layout = QVBoxLayout()
        my_pokemon_sprite_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        my_pokemon_sprite_label = QLabel()
        my_pokemon_sprite_label.setMaximumSize(self.PKMN_SPRITE_SIZE)
        my_pokemon_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        my_pokemon_gif_path = get_sprite_path(side="front", sprite_type="gif", id=self.pokemon_to_trade['id'], shiny=self.pokemon_to_trade['shiny'], gender=self.pokemon_to_trade['gender'])
        my_pokemon_movie = QMovie(my_pokemon_gif_path)
        my_pokemon_sprite_label.setMovie(my_pokemon_movie)
        my_pokemon_movie.start()
        my_pokemon_name_label = QLabel(f"{string.capwords(self.pokemon_to_trade['name'])}")
        my_pokemon_name_label.setFont(QFont("Arial", 12))

        my_pokemon_sprite_layout.addWidget(my_pokemon_sprite_label)
        my_pokemon_sprite_layout.addWidget(my_pokemon_name_label)
        sprites_layout.addLayout(my_pokemon_sprite_layout)

        # Arrow Indicator
        trade_icon_label = QLabel("⟶")
        trade_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trade_icon_label.setFont(QFont("", 30))
        sprites_layout.addWidget(trade_icon_label)

        # Pokemon To Receive
        their_pokemon_layout = QVBoxLayout()
        their_pokemon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        their_pokemon_sprite_label = QLabel()
        their_pokemon_sprite_label.setMaximumSize(self.PKMN_SPRITE_SIZE)
        their_pokemon_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        their_pokemon_sprite_label.setPixmap(QPixmap(":/icons/pokeball.png").scaled(self.PKMN_SPRITE_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        their_pokemon_name_label = QLabel("")
        their_pokemon_name_label.setFont(QFont("Arial", 12))
        
        their_pokemon_layout.addWidget(their_pokemon_sprite_label)
        their_pokemon_layout.addWidget(their_pokemon_name_label)
        sprites_layout.addLayout(their_pokemon_layout)

        return sprites_layout

    def _setup_trade_code_layout(self, window) -> QBoxLayout:
        # TODO: Button Only pressable after the input is deemed valid 
        # TODO: Remove window parameter

        """
        Returns Trade Layout

        Args:
            window: TEMPORARY - Contains reference to this window instance
        """

        trade_code_layout = QVBoxLayout() # Contains QObjects layouts from both trade sides
        trade_code_layout.setSpacing(15)

        # MyCode
        my_trade_code_layout = QVBoxLayout() # Contains QObjects regarding my trade code
        my_trade_code_layout.setSpacing(5)

        my_code_label = QLabel("Your Trade Code:")
        my_code_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))

        my_code_display_layout = QHBoxLayout() # Contains TextField (Code) and Button (Copy)

        my_code_text = QLineEdit(self.controller.get_clipboard_info())
        my_code_text.setReadOnly(True)
        my_code_text.setFont(QFont("Courier New", 10))

        my_code_copy_button = QPushButton("Copy")
        my_code_copy_button.setToolTip("Copy the trade code to your clipboard")
        my_code_copy_button.clicked.connect(lambda: self.controller.copy_to_clipboard(my_code_text.text))

        my_code_display_layout.addWidget(my_code_text)
        my_code_display_layout.addWidget(my_code_copy_button)
        
        my_trade_code_layout.addWidget(my_code_label)
        my_trade_code_layout.addLayout(my_code_display_layout)


        # TheirCode
        their_trade_code_layout = QVBoxLayout() # Contains QObjects regarding their trade code
        their_trade_code_layout.setSpacing(5)

        their_code_label = QLabel("Enter Their Trade Code:")
        their_code_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))

        their_code_text = QLineEdit()
        their_code_text.setPlaceholderText("Paste trade code here")
        their_code_text.textChanged.connect(lambda text: self._update_pokemon_sprite(text, 1))
        # TODO: Have a look at the editingFinished() signal that QLineEdit throws – might be better in this case?

        their_trade_code_layout.addWidget(their_code_label)
        their_trade_code_layout.addWidget(their_code_text)

        button_trade_with_password = QPushButton("Generate Trade Password")
        button_trade_with_password.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        button_trade_with_password.setStyleSheet("padding: 10px;")
        button_trade_with_password.clicked.connect(lambda: self.controller.generate_and_show_passwords(window))

        trade_code_layout.addLayout(my_trade_code_layout)
        trade_code_layout.addLayout(their_trade_code_layout)
        trade_code_layout.addWidget(button_trade_with_password)

        return trade_code_layout

    def _update_pokemon_sprite(self, code, pokemon_index: int):
        print("Called: _update_pokemon_sprite")
        """
        Args:
            pokemon_index: Is the pokemon index to select when updating the sprite - index 0 being my Pokémon, index 1 being their Pokémon
        """
        pass
    

    def update_other_pokemon_sprite(self, code):
        from PyQt6.QtGui import QMovie
        try:
            parts = code.split(',')
            self.other_pokemon_sprite_label.clear()
            self.other_pokemon_sprite_label.setPixmap(QPixmap())
            self.other_pokemon_name_label.setText("")
            if len(parts) > 0 and parts[0].isdigit():
                pokemon_id = int(parts[0])
                other_gender = "M"
                other_shiny = False
                if len(parts) > 2:
                    gender_map = {"0": "M", "1": "F", "2": "N"}
                    other_gender = gender_map.get(parts[2], "M")
                
                sprite_path = get_sprite_path(side="front", sprite_type="gif", id=pokemon_id, shiny=other_shiny, gender=other_gender)
                
                if hasattr(self, '_other_pokemon_movie') and self._other_pokemon_movie is not None:
                    self._other_pokemon_movie.stop()
                    self._other_pokemon_movie.deleteLater()
                    self._other_pokemon_movie = None
                other_pokemon_movie = QMovie(sprite_path)
                self._other_pokemon_movie = other_pokemon_movie
                
                def set_other_frame():
                    frame = other_pokemon_movie.currentImage()
                    if not frame.isNull():
                        scaled = QPixmap.fromImage(frame).scaled(self.PKMN_SPRITE_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        self.other_pokemon_sprite_label.setPixmap(scaled)
                other_pokemon_movie.frameChanged.connect(lambda _: set_other_frame())
                self.other_pokemon_sprite_label.setMovie(other_pokemon_movie)
                other_pokemon_movie.start()
                set_other_frame()
                name = self.get_pokemon_name_by_id(pokemon_id)
                self.other_pokemon_name_label.setText(name if name else "Unknown Pokémon")
            else:
                self.other_pokemon_sprite_label.setPixmap(QPixmap(":/icons/pokeball.png").scaled(QSize(64, 64), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.other_pokemon_name_label.setText("")
        except Exception:
            self.other_pokemon_sprite_label.setPixmap(QPixmap(":/icons/pokeball.png").scaled(QSize(64, 64), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.other_pokemon_name_label.setText("")

    def get_pokemon_name_by_id(self, pokemon_id):
        try:
            with open(self.pokedex_path, 'r', encoding='utf-8') as file:
                pokedex = json.load(file)
                for details in pokedex.values():
                    if details.get('num') == pokemon_id:
                        return details.get('name', str(pokemon_id))
        except Exception as e:
            show_warning_with_traceback(parent=self.parent_window, exception=e, message=f"An error occurred while getting the Pokémon name for ID {pokemon_id}.")
        return str(pokemon_id)
    
    def format_gender(self):
        gender_map = {"M": 0, "F": 1, "N": 2}
        return gender_map.get(self.pokemon_to_trade['gender'], 3)
    
    def format_shiny(self):
        return 1 if self.pokemon_to_trade['shiny'] else 0

    def ev_string(self):
        return ','.join(str(value) for value in self.pokemon_to_trade['ev'].values())

    def iv_string(self):
        return ','.join(str(value) for value in self.pokemon_to_trade['iv'].values())

    def attack_ids(self):
        return ','.join([str(self.find_move_by_name(attack)) for attack in self.pokemon_to_trade['attacks']])

    def find_move_by_name(self, move_name):
        with open(self.moves_file_path, 'r', encoding='utf-8') as file:
            moves_data = json.load(file)
            move = next((move for move in moves_data.values() if move.get('name').lower() == move_name.lower()), None)
            if move:
                return move['num']
            else:
                return int(33)