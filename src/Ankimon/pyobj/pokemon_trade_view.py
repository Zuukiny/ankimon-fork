import json
import string

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtGui import QPixmap, QFont, QIcon, QColor, QMovie, QImage
from PyQt6.QtCore import QSize, Qt

from aqt import mw

from ..functions.sprite_functions import get_sprite_path

class PokemonTradeView():
    PKMN_SPRITE_SIZE = QSize(64, 64)

    def __init__(self, pokemonTradeObj, pokemon, moves_file_path, parent_window=None):
        self.pokemonTradeObj = pokemonTradeObj
        self.pokemon_to_trade = pokemon
        self.moves_file_path = moves_file_path # temporary
        self.parent_window = parent_window
    
    def open_trade_window(self):

        # Window Details
        parent = self.parent_window if self.parent_window is not None else mw
        window = QDialog(parent)
        window.setWindowTitle(f"Trade Pokémon: {string.capwords(self.pokemon_to_trade['name'])}")
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        window.setMinimumSize(380, 450)

        main_layout = QVBoxLayout(window)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Trade Infos
        title_label = QLabel(f"Trading Away: {string.capwords(self.pokemon_to_trade['name'])}")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        sprites_layout = QHBoxLayout()
        sprites_layout.setSpacing(20)
        
        # Pokemon To Trade
        
        your_pokemon_sprite_layout = QVBoxLayout()
        your_pokemon_sprite_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        your_pokemon_sprite_label = QLabel()
        your_pokemon_sprite_label.setMaximumSize(self.PKMN_SPRITE_SIZE)
        your_pokemon_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        your_pokemon_gif_path = get_sprite_path(side="front", sprite_type="gif", id=self.pokemon_to_trade['id'], shiny=self.pokemon_to_trade['shiny'], gender=self.pokemon_to_trade['gender'])
        your_pokemon_movie = QMovie(your_pokemon_gif_path)
        your_pokemon_sprite_label.setMovie(your_pokemon_movie)
        your_pokemon_movie.start()
        your_pokemon_name_label = QLabel(f"{string.capwords(self.pokemon_to_trade['name'])}")
        your_pokemon_name_label.setFont(QFont("Arial", 12))

        your_pokemon_sprite_layout.addWidget(your_pokemon_sprite_label)
        your_pokemon_sprite_layout.addWidget(your_pokemon_name_label)
        sprites_layout.addLayout(your_pokemon_sprite_layout)

        # Arrow Indicator
        trade_icon_label = QLabel("->")
        trade_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sprites_layout.addWidget(trade_icon_label)

        # Pokemon To Receive
        other_pokemon_layout = QVBoxLayout()
        other_pokemon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        their_pokemon_sprite_label = QLabel()
        their_pokemon_sprite_label.setMaximumSize(self.PKMN_SPRITE_SIZE)
        their_pokemon_sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        their_pokemon_sprite_label.setPixmap(QPixmap(":/icons/pokeball.png").scaled(self.PKMN_SPRITE_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        their_pokemon_name_label = QLabel("")
        their_pokemon_name_label.setFont(QFont("Arial", 12))
        
        other_pokemon_layout.addWidget(their_pokemon_sprite_label)
        other_pokemon_layout.addWidget(their_pokemon_name_label)
        sprites_layout.addLayout(other_pokemon_layout)

        main_layout.addLayout(sprites_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        # Trade Code

        # MyCode
        trade_code_layout = QVBoxLayout()
        trade_code_layout.setSpacing(5)

        my_trade_code_layout = QVBoxLayout()

        my_code_label = QLabel("Your Trade Code:")
        my_code_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))

        my_code_display_layout = QHBoxLayout()

        my_code_text = QLineEdit(self.pokemonTradeObj.get_clipboard_info())
        my_code_text.setReadOnly(True)
        my_code_text.setFont(QFont("Courier New", 10))

        my_code_copy_button = QPushButton("Copy")
        my_code_copy_button.setToolTip("Copy the trade code to your clipboard")
        my_code_copy_button.clicked.connect(lambda: self.pokemonTradeObj.copy_to_clipboard(my_code_text.text))

        # Add to HBox – MyCode
        my_code_display_layout.addWidget(my_code_text)
        my_code_display_layout.addWidget(my_code_copy_button)
        # Add to VBox – MyCode
        my_trade_code_layout.addWidget(my_code_label)
        my_trade_code_layout.addLayout(my_code_display_layout)

        trade_code_layout.addLayout(my_trade_code_layout) # Should happen later

        main_layout.addLayout(self.trade_code_layout) # Should happen at the end

        # TheirCode
        self.their_code_label = QLabel("Enter Their Trade Code:")
        self.their_code_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        main_layout.addWidget(self.their_code_label)

        self.trade_code_input = QLineEdit()
        self.trade_code_input.setPlaceholderText("Paste trade code here")
        self.trade_code_input.textChanged.connect(self.update_other_pokemon_sprite)
        main_layout.addWidget(self.trade_code_input)

        self.trade_button = QPushButton("Generate Trade Password")
        self.trade_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.trade_button.setStyleSheet("padding: 10px;")
        self.trade_button.clicked.connect(lambda: self.generate_and_show_passwords(window))
        main_layout.addWidget(self.trade_button)

        window.exec()
    
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