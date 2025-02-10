# __author__ = 'marble_xu'

# import pygame as pg
# from . import tool
# from . import constants as c
# from .state import level

# def main():
#     game = tool.Control()
#     state_dict = {c.LEVEL: level.Level()}
#     game.setup_states(state_dict, c.LEVEL)
#     game.main()


#__author__ = 'marble_xu'

import joblib  # Make sure joblib (or scikit-learn) is installed
import pygame as pg

from . import constants as c
from . import tool
from .state import level


def main():
    """
    Main entry point for the Angry Birds game.
    Loads an ML model, sets the difficulty multiplier,
    then starts the main game loop.
    """

    # 1) Optionally load your ML model
    try:
        model = joblib.load("game_difficulty_model_decision_tree.pkl")
        print("Loaded ML model: game_difficulty_model_decision_tree.pkl")
    except Exception as e:
        print("Could not load 'game_difficulty_model_decision_tree.pkl'. Using default multiplier.")
        print(f"Error detail: {e}")
        model = None

    # 2) Predict initial difficulty (example only)
    #    In a real scenario, you'd gather actual in-game stats or player data.
    if model:
        try:
            # Example feature array: [shots_fired, time_spent, retries, level_number, ...]
            example_features = [10, 60, 1, 1]  # Placeholder
            predicted_value = model.predict([example_features])[0]
            
            # Clamp or transform predicted_value into a sensible range
            # e.g., between 0.5 and 2.0
            c.DIFFICULTY_MULTIPLIER = max(0.5, min(2.0, predicted_value))
            print(f"Difficulty multiplier set to {c.DIFFICULTY_MULTIPLIER:.2f}")
        except Exception as e:
            print("Prediction failed. Using default multiplier of 1.0")
            print(f"Error detail: {e}")
            c.DIFFICULTY_MULTIPLIER = 1.0
    else:
        # If model isn't loaded, default to neutral multiplier
        c.DIFFICULTY_MULTIPLIER = 1.0

    # 3) Initialize and run the game
    game = tool.Control()
    # Create a dictionary of states; here, we just have LEVEL,
    # but you may have other states like MAIN_MENU, GAME_OVER, etc.
    state_dict = {c.LEVEL: level.Level()}
    game.setup_states(state_dict, c.LEVEL)
    game.main()
