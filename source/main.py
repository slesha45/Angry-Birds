import joblib
import pygame as pg

from . import constants as c
from . import tool
from .state import level


def main():
    """
    Main entry point for the Angry Birds game.
    Loads an ML model, sets the difficulty multiplier,
    and starts the main game loop.
    """

    # 1) Load ML model (Decision Tree)
    try:
        model = joblib.load("game_difficulty_model_decision_tree.pkl")
        print("Loaded ML model: game_difficulty_model_decision_tree.pkl")
    except Exception as e:
        print("Could not load 'game_difficulty_model_decision_tree.pkl'. Using default multiplier.")
        print(f"Error detail: {e}")
        model = None

    # 2) Predict initial difficulty (placeholder)
    if model:
        try:
            #[shots_fired, time_spent, retries, level_number]
            example_features = [10, 60, 1, 1]
            predicted_value = model.predict([example_features])[0]

            # Option A: Set DIFFICULTY_MULTIPLIER
            c.DIFFICULTY_MULTIPLIER = max(0.5, min(2.0, predicted_value))

            # Option B: Also store a difficulty label or raw numeric
            if predicted_value < 0.4:
                c.CURRENT_DIFFICULTY_LABEL = "LOW"
            elif predicted_value < 0.7:
                c.CURRENT_DIFFICULTY_LABEL = "MEDIUM"
            else:
                c.CURRENT_DIFFICULTY_LABEL = "HIGH"

            c.CURRENT_DIFFICULTY_VALUE = predicted_value

            print(f"Difficulty multiplier set to {c.DIFFICULTY_MULTIPLIER:.2f}")
            print(f"Difficulty level: {c.CURRENT_DIFFICULTY_LABEL} ({predicted_value:.2f})")

        except Exception as e:
            print("Prediction failed. Using default multiplier of 1.0")
            print(f"Error detail: {e}")
            c.DIFFICULTY_MULTIPLIER = 1.0
            c.CURRENT_DIFFICULTY_LABEL = "MEDIUM"
            c.CURRENT_DIFFICULTY_VALUE = 1.0
    else:
        # If model isn't loaded, default everything
        c.DIFFICULTY_MULTIPLIER = 1.0
        c.CURRENT_DIFFICULTY_LABEL = "MEDIUM"
        c.CURRENT_DIFFICULTY_VALUE = 1.0

    # 3) Initialize and run the game
    game = tool.Control()
    state_dict = {c.LEVEL: level.Level()}
    game.setup_states(state_dict, c.LEVEL)
    game.main()
