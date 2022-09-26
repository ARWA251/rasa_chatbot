
from typing import Any, Text, Dict, List, Optional, Union
import os
import json
import arrow 
import requests
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import os
from rasa_sdk.types import DomainDict
def date(someDate):
    
    newDate = ""
    for i in someDate:
        if i == '.' or i == '-' or i== ' ':
            newDate += '/'
        else:
            newDate += i
    return newDate
    
username = ''
password = ''
api_url = "https://fnac-es-dev.oc-i.eu/opencell/api/rest/account/access/createOrUpdate"
todo ={
            "code" : ".....",
            "subscription" : ".....",
            "subscriptionValidityDate" : ".....",
            "startDate" : ".....",
            "endDate" : "....."
            }
headers =  {"Content-Type":"application/json"}



class ActionGetVersion(Action):
    
    def name(self) -> Text:
        return "action_get_version"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        username = ''
        password = ''
        f = requests.get('https://fnac-es-dev.oc-i.eu/opencell/api/rest/Communication/version',auth=(username,password))

        answer = f.json()
        answers = answer["message"]
        
        
        dispatcher.utter_message(text=answers)
        return [SlotSet("version", answers)]
        

class ActionSaveConversation(Action):
  
    def name(self) -> Text:
        return "action_conversation_saved"

    def required_slots(self,tracker) -> List[Text]:
      return ["email","phno"]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "email": [
                self.from_text(),
            ],
            "phno": [
                self.from_text(),
            ],
        } 
            
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:       

        dispatcher.utter_message(text="All chats saved.")
        return []
class ValidateSimpleAccountForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_simple_account_form"
    
    def validate_account_code(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `account_code` value."""

        todo.update({"code":slot_value})
        print(todo)
        
        return {"account_code": slot_value}
    def validate_account_subscriptionValidityDate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `account_subscriptionValidityDate` value."""

        todo.update({"subscriptionValidityDate":date(slot_value)})
        print(todo)
        return {"account_subscriptionValidityDate": slot_value}

    def validate_account_subscription(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `account_subscription` value."""

        todo.update({"subscription":slot_value})
        print(todo)
        return {"account_subscription": slot_value}

    def validate_account_startDate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `account_startDate` value."""

        todo.update({"startDate":date(slot_value)})
        print(slot_value)
        print(todo)
        return {"account_startDate": slot_value}
    

    def validate_account_endDate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `account_endDate` value."""
        
        todo.update({"endDate":date(slot_value)})
        print(todo)
        return {"account_endDate": slot_value}
        
class ActionGetStatus(Action):
    
    def name(self) -> Text:
        return "action_get_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        
        response = requests.post(api_url,data=json.dumps(todo) , headers=headers, auth=(username,password))
        
        answer = response.json()
        answers = answer["status"]
        
        if answers=="SUCCESS":

           dispatcher.utter_message(text="Your account will be updated with success")
        else :
           dispatcher.utter_message(text="your account isn't updating") 