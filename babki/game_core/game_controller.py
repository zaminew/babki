from game import Game
from game_setting import *
from player import Player
from typing import List, Dict
import uuid

class GameController:
    def __init__(self):
        self.games : Dict[str, Game] = {}

    def create_game(self, settings: GameSetting, players: List[str] = List[str]) -> str:
        game_id = str(uuid.uuid4())
        self.games[game_id] = Game(settings, players)
        return game_id

    def get_game(self, game_id: str) -> Game:
        return self.games.get(game_id)

    def remove_game(self, game_id: str):
        if game_id in self.games:
            del self.games[game_id]

    def get_games_count(self) -> int:
        return len(self.games)

    def get_all_games(self) -> Dict[str, Game]:
        return self.games
    
    def get_games_info(self) -> List[tuple]:
        lines = []
        for key, value in self.games.items():
            string = f'p:{value.settings.num_players}, dif:{value.settings.difficulty}, '\
                        f' game maker: {value.players.get(value.game_maker_id).name}'
            names = []
            for player_key, player in value.players.items():
                names.append(player.name)
            
            lines.append((key, string, names))
        return lines
        