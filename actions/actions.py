from typing import Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionMeteo(Action):
    def name(self) -> str:
        return "action_meteo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        città = tracker.get_slot("città")

        meteo_finto = {
            "Roma": "sole e 27°C",
            "Milano": "pioggia leggera e 22°C",
            "Napoli": "nuvoloso e 25°C"
        }

        if città in meteo_finto:
            risposta = f"A {città} oggi c'è {meteo_finto[città]}."
        else:
            risposta = f"Mi dispiace, non ho informazioni sul meteo per {città}."

        dispatcher.utter_message(text=risposta)
        return []
