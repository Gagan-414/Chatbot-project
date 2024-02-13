import csv
import re
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted,ActionExecuted
from CSV_SQL_CONNECTION import Get_from_CSV  # Assuming CSV_SQL_CONNECTION.py contains the required function

# Action to start a new session and reset all slots
class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # List of events to return after this action runs
        events = [SessionStarted()]

        # Reset slots
        for slot in tracker.slots:
            events.append(SlotSet(slot, None))

        events.append(ActionExecuted("action_listen"))

        return events




# For Storing data into sql database
class ActionStoreParamsInCSV(Action):

    def name(self) -> str:
        return "action_store_params_in_csv"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> list:
        # Define your parameters
        params = ["name", "email", "contact", "query"]

        # Create a dictionary to store the parameter values
        param_values = {}

        # Fetch the parameter values from the tracker
        for param in params:
            value = tracker.get_slot(param)
            if value is not None:
                param_values[param] = value

        # Create a CSV file if it doesn't exist
        if not os.path.exists("parameter_values.csv"):
            with open("parameter_values.csv", "w") as file:
                writer = csv.DictWriter(file, fieldnames=params)
                writer.writeheader()

        # Append the parameter values to the CSV file
        with open("parameter_values.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=params)
            writer.writerow(param_values)
        Get_from_CSV("parameter_values.csv")
        name = tracker.get_slot("name")
        dispatcher.utter_message(text=f"Thank You {name} for your response. Our Team Representative will get back to you soon.")

        return []

# for validation of user details
class ActionHandleUserDetails(Action):
    def name(self) -> Text:
        return "action_handle_user_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not tracker.get_slot("name_filled"):
            return self.handle_name(dispatcher, tracker,domain)
        elif not tracker.get_slot("email_filled"):
            return self.handle_email(dispatcher, tracker,domain)
        elif not tracker.get_slot("contact_filled"):
            return self.handle_contact(dispatcher, tracker,domain)
        elif tracker.get_slot("contact_filled"):
            return self.handle_query(dispatcher, tracker,domain)
        else:
            return []

    def handle_name(self, dispatcher, tracker,domain):
        user_name = next(tracker.get_latest_entity_values("name"), None)
        if user_name and re.compile(r'^[a-zA-Z\s]+$').match(user_name):
            dispatcher.utter_message("Please enter your email.")
            return [SlotSet("name", user_name), SlotSet("name_filled", True)]
        else:
            dispatcher.utter_message("Please enter a valid name with only alphabets.")
            return []

    def handle_email(self, dispatcher, tracker,domain):
        user_email = next(tracker.get_latest_entity_values("email"), None)
        if user_email and re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user_email):
            dispatcher.utter_message("Please enter your contact.")
            return [SlotSet("email", user_email), SlotSet("email_filled", True)]
        else:
            dispatcher.utter_message("Please enter a valid email address.")
            return []

    def handle_contact(self, dispatcher, tracker,domain):
        # user_contact = next(tracker.get_latest_entity_values("contact"), None)
        # if user_contact and re.match(r"^[6-9]\d{9}$", user_contact):
        #     # Call the ValidateContact action here
        validate_action = ValidateContact()
        return validate_action.run(dispatcher, tracker, domain)

    def handle_query(self, dispatcher, tracker,domain):
        validate_query = ActionStoreUserQuery()
        return validate_query.run(dispatcher , tracker, domain)
        # user_query = next(tracker.get_latest_entity_values("query"), None)
        # if user_query:
        #     # dispatcher.utter_message("Thank you for your query. We will get back to you soon.")
        #     return [SlotSet("query", user_query)]
        # else:
        #     dispatcher.utter_message("Please enter your query.")
        #     return []

# Validate Contact Action
class ValidateContact(Action):

    def name(self) -> str:
        return "Contact_Validate_form"

    def run(self, dispatcher, tracker, domain):
        contact = tracker.get_slot("contact")

        if contact:
            country = self.check_country(contact)
            if country:
                # dispatcher.utter_message(text=f"Country: {country}")
                dispatcher.utter_message("Please tell me your query.")
                return [SlotSet("country", country),SlotSet("contact_filled", True)]
            else:
                dispatcher.utter_message(text="Unknown country.")
        else:
            dispatcher.utter_message(text="Please provide a contact number.")
        return []

    def check_country(self, contact: str) -> str:
        # Normalize the contact by removing spaces, dashes, and parentheses
        normalized_contact = re.sub(r'\s|-|\(|\)', '', contact)

        # Regular expression patterns for different country formats
        patterns = {
            "India": r'^(91|\+91|0)?[6789]\d{9}$',
            "United States": r'^(1|\+1)?\d{10}$',
            "United Kingdom": r'^(44|\+44)?\d{10}$',
            "United Arab Emirates": r'^(971|\+971)?\d{9}$',
            "Hong Kong": r'^(852|\+852)?\d{8}$',
            "Singapore": r'^(65|\+65)?\d{8}$',
            "Australia": r'^(61|\+61)?(02|03|07|08)?4\d{8}$'
        }

        for country, pattern in patterns.items():
            if re.compile(pattern).match(normalized_contact):
                return country

        return None


class ActionStoreUserQuery(Action):
    def name(self) -> str:
        return "action_store_user_query"

    def run(self, dispatcher, tracker, domain):
        user_query = tracker.latest_message.get('text')
        return [SlotSet("query", user_query)]
