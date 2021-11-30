# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from logging import RootLogger
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FormValidation, SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.types import DomainDict
from rasa_sdk import FormValidationAction
import re


class ValidateSearchForm(FormValidationAction):
    validation_events = []

    def name(self) -> Text:
        return "validate_search_form"
    
    def invalid_input(self, slot_name: Any, slot_value: Any, dispatcher: CollectingDispatcher):
        dispatcher.utter_message(response="utter_wrong_input", wrong_input=slot_value)
        self.validation_events.append(SlotSet(slot_name, None))
    
    def validate_1_departure_location(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        location = slot_value.split(" ")
        if location[0] == "from" or location[0] == "departure" or location[0] == "depart":
            location = " ".join(location[1:])
        else:
            location = " ".join(location)
        if location.lower() in self.departure_db():
            self.validation_events.append(SlotSet("1_departure_location", location))
            return {"1_departure_location": location}
        else:
            self.invalid_input("1_departure_location", location, dispatcher)
            return {"1_departure_location": None}
    
    def validate_2_destination(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        location2 = slot_value.split(" ")
        if location2[0] == "destination" or location2[0] == "to" or location2[0] == "arrival":
            location2 = " ".join(location2[1:])
        else:
            location2 = " ".join(location2)
        if location2.lower() in self.destination_db():
            self.validation_events.append(SlotSet("2_destination", location2))
            return {"2_destination": location2}
        else:
            self.invalid_input("2_destination", location2, dispatcher)
            return {"2_destination": None}
    
    def validate_3_flight_date(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        #date_regex = '/(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.](19|20)\d\d/';
        #date_regex2 = '\d{4}-\d{2}-\d{2}'
        if (re.search(r"\d{2}-\d{2}-\d{4}", slot_value)) or (re.search(r"\d{2}/\d{2}/\d{4}", slot_value)):
            return {"3_flight_date": slot_value}
        else:
            self.invalid_input("3_flight_date", slot_value, dispatcher)
            return {"3_flight_date": None}
    
    def validate_4_stops_or_not(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() in self.stops_nonstops_dct():
            self.validation_events.append(SlotSet("4_stops_or_not", slot_value))
            return {"4_stops_or_not": slot_value}
        else:
            self.invalid_input("4_stops_or_not", slot_value, dispatcher)
            return {"4_stops_or_not": None}
    
    def validate_5_cabin_class(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() in self.cabin_class_dct():
            self.validation_events.append(SlotSet("5_cabin_class", slot_value))
            return {"5_cabin_class": slot_value}
        else:
            self.invalid_input("5_cabin_class", slot_value, dispatcher)
            return {"5_cabin_class": None}

    def validate_6_ticket_numbers(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        ticket_number = slot_value.split(" ")[0]
        if ticket_number.isnumeric():
            self.validation_events.append(SlotSet("6_ticket_numbers", ticket_number))
            return {"6_ticket_numbers": ticket_number}
        else:
            self.invalid_input("6_ticket_numbers", ticket_number, dispatcher)
            return {"6_ticket_numbers": None}
    
    def validate_7_names(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        temp = slot_value.split(" ")
        first_name = temp[-2]
        last_name = temp[-1]                       
        names = " ".join(temp[-2:])
        if first_name.isalpha() and last_name.isalpha():
            self.validation_events.append(SlotSet("7_names", names))
            return {"7_names": names}
        else:
            self.invalid_input("7_names", names, dispatcher)
            return {"7_names": None}
    
    def validate_8_contact_info(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                                      domain: DomainDict) -> Dict[Text, Any]:
        phone_numbers = re.findall(r"\d+", slot_value)[0]
        if phone_numbers and len(phone_numbers) == 10:
            self.validation_events.append(SlotSet("8_contact_info", phone_numbers))
            return {"8_contact_info": phone_numbers}
        else:
            self.invalid_input("8_contact_info", phone_numbers, dispatcher)
            return {"8_contact_info": None}

    @staticmethod
    def departure_db() -> List[Text]:
        return ["san jose", "san francisco", "los angeles", "sacramento", "san diego", "seattle", "phoenix", 
                "tahoe", "portland", "austin", "oakland", "dallas", "new york", "boston", "houston", "miami", 
                "atlanta", "orlando", "chicago", "philadelphia", "detroit", "washington dc", "denver", "columbus"]
    
    @staticmethod
    def destination_db() -> List[Text]:
        return ["beijing", "kunming", "vancouver", "tokyo", "seoul", "dubai", "berlin", "mexico city", "salt lake city",
                "hawaii", "london"]

    @staticmethod
    def stops_nonstops_dct() -> List[Text]:
        return ["stops", "stop", "nonstop", "nonstops"]

    @staticmethod
    def cabin_class_dct() -> List[Text]:
        return ["economy", "premium economy", "business", "first"]

class confirmation(Action):
    def name(self) -> Text:
        return "action_confirmation_msg"
    
    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        departure = tracker.get_slot("1_departure_location")
        departure = departure.split(" ")
        if departure[0] == "destination" or departure[0] == "to" or departure[0] == "arrival":
            departure = " ".join(departure[1:])
        else:
            departure = " ".join(departure)
        destination = tracker.get_slot("2_destination")
        destination = destination.split(" ")
        if destination[0] == "destination" or destination[0] == "to" or destination[0] == "arrival":
            destination = " ".join(destination[1:])
        else:
            destination = " ".join(destination)
        date = tracker.get_slot("3_flight_date")
        stops = tracker.get_slot("4_stops_or_not")
        if stops.lower() == "nonstops" or stops.lower() == "nonstop":
            nonstops = "Yes"
        else:
            nonstops = "No"
        cabin = tracker.get_slot("5_cabin_class")
        tickets = tracker.get_slot("6_ticket_numbers")
        tickets = tickets.split(" ")[0]
        name = tracker.get_slot("7_names")
        name = " ".join(name.split(" ")[-2:])
        contact = tracker.get_slot("8_contact_info")
        contact = re.findall(r"\d{10}", contact)[0]

        message = f"Departure: {departure}, Destination: {destination}, Date: {date}, Nonstops: {nonstops}, Cabin: {cabin}, Number of Tickets: {tickets}, Names: {name}, Phone Numbers: {contact}"
        dispatcher.utter_message(text = "Confirmation. " + message)


class ActionProcessRefresh(Action):

    def name(self) -> Text:
        return "action_process_refresh"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
'''
class ActionStartProcess(Action):

    def name(self) -> Text:
        return "action_start_process"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("begin_process", True)]
'''