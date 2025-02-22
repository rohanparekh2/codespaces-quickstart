from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCheckAppointmentAvailability(Action):
    def name(self) -> Text:
        return "action_check_appointment_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        appointment_type = tracker.get_slot("appointment_type")
        preferred_date = tracker.get_slot("preferred_date")
        preferred_time = tracker.get_slot("preferred_time")

        is_available = self.check_availability(appointment_type, preferred_date, preferred_time)

        return [SlotSet("appointment_available", is_available)]

    def check_availability(self, appointment_type, date, time):
        # Implement your availability checking logic here
        return False  # Placeholder


class ActionCheckAlternativeAvailability(Action):
    def name(self) -> Text:
        return "action_check_alternative_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        alternative_date = tracker.get_slot("alternative_date")
        alternative_time = tracker.get_slot("alternative_time")
        current_attempts = tracker.get_slot("attempt_counter") or 0
        max_attempts = 3  # Set your desired maximum attempts

        is_available = self.check_availability(alternative_date, alternative_time)
        new_attempts = current_attempts + 1

        if is_available:
            return [
                SlotSet("appointment_available", True),
                SlotSet("attempt_counter", 0)  # Reset counter on success
            ]
        else:
            return [
                SlotSet("appointment_available", False),
                SlotSet("attempt_counter", new_attempts),
                SlotSet("max_attempts_reached", new_attempts >= max_attempts),
                SlotSet("alternative_date", None),
                SlotSet("alternative_time", None)
            ]

    def check_availability(self, date, time):
        # Implement your availability checking logic here
        return False  # Placeholder
