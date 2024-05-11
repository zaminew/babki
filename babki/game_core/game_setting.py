from enum import Enum
import json

class EnumStr(Enum):
    def __str__(self):
        return self.value
    
class Difficulty(EnumStr):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class Speed(EnumStr):
    SLOW = 'slow'
    NORMAL = 'normal'
    FAST = 'fast'

class GameType(EnumStr):
    ONE_FOR_ALL = 'one_for_all'
    ONE_FOR_ONE = 'one_for_one'

class GameMode(EnumStr):
    STABLE_EVENTS = 'stable_events'
    RANDOM_EVENTS = 'random_events'

class GameSetting:
    def __init__(self, num_players = 1, speed : Speed = Speed.NORMAL, difficulty : Difficulty = Difficulty.MEDIUM, 
                 game_type : GameType = GameType.ONE_FOR_ALL, game_mode : GameMode = GameMode.RANDOM_EVENTS, 
                 hide_stats : bool = True):
        self.num_players = num_players
        self.speed : Speed = speed
        self.difficulty : Difficulty = difficulty
        self.game_type : GameType = game_type
        self.game_mode : GameMode = game_mode
        self.hide_stats : bool = hide_stats

    @classmethod
    def from_json(cls, json_str):
        json_data = json.loads(json_str)
        return cls(**json_data)        
    
    def to_json(self):
        return {
            "num_players": self.num_players,
            "speed": str(self.speed),
            "difficulty": str(self.difficulty),
            "game_type": str(self.game_type),
            "game_mode": str(self.game_mode),
            "show_stats": self.hide_stats
        }
    
    def __str__(self):
        return json.dumps(self.to_json())
    


    
if __name__ == "__main__":
    import jsonschema
    import json

    # схема запроса создания игры
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "num_players": { "type": "integer", "minimum": 1, "maximum": 6 },
            "speed": { "type": "string", "enum": ["slow", "normal", "fast"] },
            "difficulty": { "type": "string", "enum": ["low", "medium", "high"] },
            "game_type": { "type": "string", "enum": ["one_for_all", "one_for_one"] },
            "game_mode": { "type": "string", "enum": ["stable_events", "random_events"] },
            "show_stats": { "type": "boolean" }
        },
        "required": ["num_players", "speed", "difficulty", "game_type", "game_mode", "hide_stats"]
    }

    json_data_example = '''
    { 
        "num_players": 4,
        "speed": "normal",
        "difficulty": "medium",
        "game_type": "one_for_all",
        "game_mode": "stable_events",
        "hide_stats": true
    }
    '''

    try:
        instance = json.loads(json_data_example)
        jsonschema.validate(instance=instance, schema=schema)
        print('JSON данные валидны')
    except jsonschema.exceptions.ValidationError as e:
        print('Ошибка валидации JSON данных:', e)
