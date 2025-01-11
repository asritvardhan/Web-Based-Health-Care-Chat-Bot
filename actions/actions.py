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
# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction
import requests

# actions.py

# bmi calculator
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCalculateBMI(Action):

    def name(self) -> Text:
        return "action_calculate_bmi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weight = None
        height = None

        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'weight':
                weight = float(entity['value'])
            elif entity['entity'] == 'height':
                height = float(entity['value'])

        if weight and height:
            bmi = weight / (height ** 2)
            if bmi < 18.5:
                interpretation = "underweight"
            elif 18.5 <= bmi < 25:
                interpretation = "normal weight"
            elif 25 <= bmi < 30:
                interpretation = "overweight"
            else:
                interpretation = "obese"
            response = f"Your BMI is {bmi:.2f}, which is considered as{interpretation}."
        else:
            response = "I couldn't find your weight and height. Could you please provide them again?"

        dispatcher.utter_message(text=response)
        return []

# health news function
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime, timedelta

class ActionFetchHealthNews(Action):

    def name(self) -> Text:
        return "action_fetch_health_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract health problem and location mentioned by the user
        health_problem = next(tracker.get_latest_entity_values('health_problem'), None)
        location = next(tracker.get_latest_entity_values('location'), None)

        if not health_problem:
            dispatcher.utter_message(text="Please specify a health topic you are interested in.")
            return []

        if not location:
            dispatcher.utter_message(text="Please specify a location in India you are interested in.")
            return []

        # Specify the time period (e.g., past week)
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        to_date = datetime.now().strftime('%Y-%m-%d')

        # GNews API parameters
        api_key = "32e63fdc336db877fece9bc967450db1"  # Replace with your actual GNews API key
        endpoint = "https://gnews.io/api/v4/search"
        query = f"{health_problem} {location}"
        params = {
            "token": api_key,
            "q": query,
            "topic": "health",
            "lang": "en",
            "country": "in",  # Specify India as the country
            "from": from_date,
            "to": to_date,
            "max": 3
        }

        # Fetch health news related to the user's input from GNews API
        response = requests.get(endpoint, params=params)
        news_data = response.json()

        # Check if articles are present in the response
        if "articles" in news_data:
            articles = news_data["articles"]
            if articles:
                response_text = f"Here are the latest news articles related to {health_problem} in {location} from the past week:\n"
                for article in articles:
                    title = article.get("title", "No title")
                    link = article.get("url", "No link")
                    description = article.get("description") or article.get("content") or "No description available."
                    response_text += f"- {title}: {link}\nDescription: {description}\n\n"
                dispatcher.utter_message(text=response_text)
                return []

        # If no articles found or API request failed
        dispatcher.utter_message(
            text=f"Sorry, I couldn't find any health news articles related to {health_problem} in {location} from the past week.")
        return []
