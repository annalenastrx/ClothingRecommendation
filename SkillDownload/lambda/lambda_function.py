# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import random
import requests
import json
import database as db
import userDB as df

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value

from ask_sdk_model import Response, DialogState

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#generating colors which are typical to the season
top_spring = ["khaki", "black", "beige", "antique pink" "light blue", "amber" ]
top_summer = ["red", "yellow", "white", "coral", "pink", "turquoise", "violet"]
top_fall = ["light grey", "brown", "burgundry", "black", "champagne", "apricot"]
top_winter = ["dark grey", "black", "brown", "orange", "white"]

bottom_spring = ["black", "blue"]
bottom_summer = ["white", "light blue"]
bottom_fall = ["beige", "white", "light blue"]
bottom_winter = ["black", "dark blue", "metallic"]

dress_spring =["burgundry", "grey", "amber" ]
dress_summer = ["white", "orange", "baby blue", "blush", "lemon yellow", "apricot"]
dress_fall = ["khaki", "beige", "light brown"]

jacket_spring = ["black", "grey", "jeans", "beige"]
jacket_fall = ["champagne", "burgundry" ]
jacket_winter = ["black", "dark grey", "monochrome"]

username = ""
isNewUser = False
favClothes = ""
favColor = ""
hateColor = ""

randWeight = ""

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to your one and only alexa wardrobe! What is your name?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class WelcomeIntentHandler(AbstractRequestHandler):
    """Handler for WelcomeIntent."""
    def can_handle(self, handler_input):

        return ask_utils.is_intent_name("WelcomeIntent")(handler_input)

    def handle(self, handler_input):
        
        username = handler_input.request_envelope.request.intent.slots['name'].value
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["name"] = username
        isUser = df.get_username(username)
        text = ''
        
        if isUser == False :
            isNewUser = True
            text = f"It's a pleasure to meet you {username}. Tell me a bit about yourself. What is your favourite color and what are your favourite clothes?"
        else :
            isNewUser = False
            favClothes = df.get_fav_cloth(username)
            favColor = df.get_fav_color(username)
            hateColor = df.get_hate_color(username)
            session_attr["favClothes"] = favClothes
            session_attr["favColor"] = favColor
            session_attr["hateColor"] = hateColor
            text = f"It's great to see you again {username}. What can I help you with today?"

        session_attr["newUser"] = isNewUser
        speak_output = text

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class NewUserIntent(AbstractRequestHandler):
    """Handler for NewUser Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("NewUserIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        favColor = handler_input.request_envelope.request.intent.slots['color'].value
        favClothes = handler_input.request_envelope.request.intent.slots['clothes'].value
        hateColor = handler_input.request_envelope.request.intent.slots['hatecolor'].value
        hateClothes = handler_input.request_envelope.request.intent.slots['hateclothes'].value
        
        username = handler_input.attributes_manager.session_attributes["name"]
        text = ''
        
        if handler_input.attributes_manager.session_attributes['newUser'] == True:
            session_attr["favColor"] = favColor
            session_attr["favClothes"] = favClothes
            session_attr["hateColor"] = hateColor
            session_attr["hateClothes"] = hateClothes
            text = f"Thank you for telling me what to look out for when recommending clothing to you! Anytime you want to change your preferences again just say change my preferences or tell me your favourite color again."
        else:
            text = f"All right {username}, I updated your preferences. To change your favourites just say change my preferences or tell me your favourite color again!"
        
        speak_output = text

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class OccasionRecIntentHandler(AbstractRequestHandler):
    """Handler for OccasionRec Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("OccasionRecIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        event = handler_input.request_envelope.request.intent.slots['occasion'].value
        adjective = handler_input.request_envelope.request.intent.slots['adjective'].value
        favColor = handler_input.attributes_manager.session_attributes['favColor']
        favClothes = handler_input.attributes_manager.session_attributes['favClothes']
        hateColor = handler_input.attributes_manager.session_attributes['hateColor']
        randWeight = random.randint(0,100)
        
        top_color =  top_spring[random.randint(0,len(top_spring)-1)]
        bottom_color = bottom_spring[random.randint(0,len(bottom_spring)-1)]
        dress_color = dress_spring[random.randint(0,len(dress_spring)-1)]
        jacket_color = jacket_spring[random.randint(0,len(jacket_spring)-1)]
        
        article = "a "
        
        if adjective:
            item = db.get_adj_event(event, adjective, "")
            
            if item == "dress":
                jacket = db.get_adj_event(event, adjective, "Jackets")
                jacket_color = jacket_fall[random.randint(0,len(jacket_fall)-1)]
                dress_color = dress_summer[random.randint(0,len(dress_summer)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (dress_color == hateColor):
                    dress_color = favColor
                speak_output = f"To look {adjective} for {event} you could wear a {dress_color} {item}. I would also recommend you to take a {jacket} with you, maybe a {jacket} in {jacket_color}."
            else:
                bottom = db.get_adj_event(event, adjective, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_adj_event(event, adjective, "Tops")
                top_color =  top_spring[random.randint(0,len(top_spring)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_winter[random.randint(0,len(bottom_winter)-1)]
                speak_output = f"For {event} I would recommend you to wear a {top_color} {top} in combination to {article} {bottom_color} {bottom}. This will definetly be {adjective}."
        else:
            item = db.get_event(event, "")
            if item == "dress":
                jacket = db.get_event(event, "Jackets")
                dress_color = dress_summer[random.randint(0,len(dress_summer)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (dress_color == hateColor):
                    dress_color = favColor
                jacket_color = jacket_fall[random.randint(0,len(jacket_fall)-1)]
                speak_output = f"You could try out a {dress_color} {item} for a {event}. A {jacket_color} {jacket} on top would complete the outfit."
            else:
                bottom = db.get_event(event, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_event(event, "Tops")
                top_color =  top_spring[random.randint(0,len(top_spring)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_winter[random.randint(0,len(bottom_winter)-1)]
                speak_output = f"Why dont you try to wear a {top_color} {top} combined with {article} {bottom_color} {bottom} for this {event}?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class SeasonsIntentHandler(AbstractRequestHandler):
    """Handler for Season Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SeasonsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        season = handler_input.request_envelope.request.intent.slots['season'].value
        adjective = handler_input.request_envelope.request.intent.slots['adjective'].value
        favColor = handler_input.attributes_manager.session_attributes['favColor']
        hateColor = handler_input.attributes_manager.session_attributes['hateColor']
        randWeight = random.randint(0,100)

        article = "a "
        
        print(season)
        print(adjective)
        
        if adjective:
            if season == "spring":
                bottom = db.get_adj_season(season, adjective, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_adj_season(season, adjective, "Tops")
                dress = db.get_adj_season(season, adjective, "Dresses")
                jacket = db.get_adj_season(season, adjective, "Jackets")
                
                top_color =  top_spring[random.randint(0,len(top_spring)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_spring[random.randint(0,len(bottom_spring)-1)]
                dress_color = dress_spring[random.randint(0,len(dress_spring)-1)]
                jacket_color = jacket_spring[random.randint(0,len(jacket_spring)-1)]
                
                speak_output = f"For {season} days you could wear a {top_color} {top} combined with {bottom_color} {bottom}. Also a {dress_color} {dress} would be suitable but don't forget your {jacket} then. Both will look very {adjective}."
            if season == "summer":
                bottom = db.get_adj_season(season, adjective, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_adj_season(season, adjective, "Tops")
                dress = db.get_adj_season(season, adjective, "Dresses")
                
                top_color =  top_summer[random.randint(0,len(top_summer)-1)]
                bottom_color = bottom_summer[random.randint(0,len(bottom_summer)-1)]
                dress_color = dress_summer[random.randint(0,len(dress_summer)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (dress_color == hateColor):
                    dress_color = favColor
                
                speak_output = f"For warm {season} days, I would recommend you to wear a {dress_color} {dress}. Otherwise a {top_color} {top} combined with {article} {bottom_color} {bottom} would be {adjective} too."
            if season == "fall":
                bottom = db.get_adj_season(season, adjective, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_adj_season(season, adjective, "Tops")
                dress = db.get_adj_season(season, adjective, "Dresses")
                jacket = db.get_adj_season(season, adjective, "Jackets")
                

                top_color =  top_fall[random.randint(0,len(top_fall)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_fall[random.randint(0,len(bottom_fall)-1)]
                dress_color = dress_fall[random.randint(0,len(dress_fall)-1)]
                jacket_color = jacket_fall[random.randint(0,len(jacket_fall)-1)]
                
                speak_output = f"For {season} days you could wear a {top_color} {top} combined with {article}{bottom_color} {bottom}. Also a {dress_color} {dress} would be suitable but don't forget your {jacket} then. Both will be very {adjective}."
            if season == "winter":
                bottom = db.get_adj_season(season, adjective, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_adj_season(season, adjective, "Tops")
                jacket = db.get_adj_season(season, adjective, "Jackets")
                
                top_color =  top_winter[random.randint(0,len(top_winter)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_winter[random.randint(0,len(bottom_winter)-1)]
                jacket_color = jacket_winter[random.randint(0,len(jacket_winter)-1)]
                
                speak_output = f"Make sure to be appropriate clothed for {season} days. You definitely will need a {jacket}, maybe a {jacket} in {jacket_color} would look good. Underneath you could wear a {top_color} {top} combined with {article} {bottom_color} {bottom}."
            
        else:
            if season == "spring":
                bottom = db.get_season(season, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_season(season, "Tops")
                dress = db.get_season(season, "Dresses")
                jacket = db.get_season(season, "Jackets")
                
                top_color =  top_spring[random.randint(0,len(top_spring)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_spring[random.randint(0,len(bottom_spring)-1)]
                dress_color = dress_spring[random.randint(0,len(dress_spring)-1)]
                jacket_color = jacket_spring[random.randint(0,len(jacket_spring)-1)]
                
                speak_output = f"For {season} days you could wear a {top_color} {top} combined with {article} {bottom_color} {bottom}. Also a {dress_color} {dress} would be suitable but don't forget your {jacket} then."
            if season == "summer":
                bottom = db.get_season(season, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_season(season, "Tops")
                dress = db.get_season(season, "Dresses")
                
                top_color =  top_summer[random.randint(0,len(top_summer)-1)]
                bottom_color = bottom_summer[random.randint(0,len(bottom_summer)-1)]
                dress_color = dress_summer[random.randint(0,len(dress_summer)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (dress_color == hateColor):
                    dress_color = favColor
                
                speak_output = f"For warm {season} days, I would recommend you to wear a {dress_color} {dress}. Otherwise a {top_color} {top} combined with {article} {bottom_color} {bottom} would be appropriate too." 
            if season == "fall":
                bottom = db.get_season(season, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_season(season, "Tops")
                dress = db.get_season(season, "Dresses")
                jacket = db.get_season(season, "Jackets")
                
                top_color =  top_spring[random.randint(0,len(top_spring)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_spring[random.randint(0,len(bottom_spring)-1)]
                dress_color = dress_spring[random.randint(0,len(dress_spring)-1)]
                jacket_color = jacket_spring[random.randint(0,len(jacket_spring)-1)]
                
                speak_output = f"For {season} days you could wear a {top_color} {top} combined with {article} {bottom_color} {bottom}. Also a {dress_color} {dress} would be suitable but don't forget your {jacket} then."
                
                
            if season == "winter":
                bottom = db.get_season(season, "Bottoms")
                if bottom[-1] == "s":
                    article = ""
                top = db.get_season(season, "Tops")
                jacket = db.get_season(season, "Jackets")
                
                top_color =  top_winter[random.randint(0,len(top_winter)-1)]
                # depending on user preference change color
                if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                    top_color = favColor
                bottom_color = bottom_winter[random.randint(0,len(bottom_winter)-1)]
                jacket_color = jacket_winter[random.randint(0,len(jacket_winter)-1)]
                
                speak_output = f"Make sure to be appropriate clothed for {season} days. You definitely will need a {jacket}, maybe a {jacket} in {jacket_color} would look good. Underneath you could wear a {top_color} {top} combined with {article} {bottom_color} {bottom}."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
            
    

class WeatherTestIntentHandler(AbstractRequestHandler):
    """Handler for Weather Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("WeatherTestIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        city = handler_input.request_envelope.request.intent.slots['cityslot'].value
        time = handler_input.request_envelope.request.intent.slots['timeslot'].value
        favColor = handler_input.attributes_manager.session_attributes['favColor']
        hateColor = handler_input.attributes_manager.session_attributes['hateColor']

        randWeight = random.randint(0,100)
        
        if time is "None":
            time = "today"
        
        if city is "None":
            city = "Munich"
        
        # key for openweathermap API
        api_key = "9492a54f5b49d1246b10e3d93d325dfd"
        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}"
        # api url with forecast for 5 days api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}
        json_data = requests.get(api_url).json()
        
        weather_json = json_data['weather'][0]['main']
        temp_json = round(json_data['main']['temp'] )
        city_json = json_data['name']
        celsius = round(temp_json - 273.15)
        
        article = "a "
        
        accessoire = ""
        
        if weather_json == "Snow":
            accessoire = ", so a hat would be nice"
        elif (weather_json == "Rain") | (weather_json == "Drizzle"):
            accessoire = ", so make sure to pack an umbrella"
        elif weather_json == "Sunny":
            accessoire = ", so make sure to pack sunglasses"
        
        if celsius <= 10:
            bottom = db.get_season("winter", "Bottoms")
            if bottom[-1] == "s":
                article = ""
            top = db.get_season("winter", "Tops")
            jacket = db.get_season("winter", "Jackets")
            
            top_color =  top_winter[random.randint(0,len(top_winter)-1)]
            # depending on user preference change color
            if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                top_color = favColor
            bottom_color = bottom_winter[random.randint(0,len(bottom_winter)-1)]
            jacket_color = jacket_winter[random.randint(0,len(jacket_winter)-1)]
            
            speak_output = f"The weather will be {weather_json} with {celsius} °C {time}{accessoire}. You definitely will need a {jacket}, maybe a {jacket_color} {jacket} would look good. Underneath you could wear a {top_color} {top} combined with {article} {bottom_color} {bottom}."
        
        if celsius >= 11 and celsius <= 20:
            bottom = db.get_season("spring", "Bottoms")
            if bottom[-1] == "s":
                article = ""
            top = db.get_season("spring", "Tops")
            jacket = db.get_season("spring", "Jackets")
            dress = db.get_season("spring", "Dresses")
            
            top_color =  top_spring[random.randint(0,len(top_spring)-1)]
            # depending on user preference change color
            if (randWeight >= 60 and favColor != "no") or (top_color == hateColor):
                top_color = favColor
            bottom_color = bottom_spring[random.randint(0,len(bottom_spring)-1)]
            dress_color = dress_spring[random.randint(0,len(dress_spring)-1)]
            jacket_color = jacket_spring[random.randint(0,len(jacket_spring)-1)]
            
            speak_output = f"You could wear a {top_color} {top} combined with {article} {bottom_color} {bottom}. It will be {weather_json} with {celsius} °C {time} {accessoire}. You could also wear a {dress_color} {dress} but don't forget to take a {jacket} with you."
            
        if celsius >= 21:
            bottom = db.get_season("summer", "Bottoms")
            if bottom[-1] == "s":
                article = ""
            top = db.get_season("summer", "Tops")
            dress = db.get_season("summer", "Dresses")
            
            top_color =  top_summer[random.randint(0,len(top_summer)-1)]
            bottom_color = bottom_summer[random.randint(0,len(bottom_summer)-1)]
            dress_color = dress_summer[random.randint(0,len(dress_summer)-1)]
            # depending on user preference change color
            if (randWeight >= 60 and favColor != "no") or (dress_color == hateColor):
                dress_color = favColor
            
            speak_output = f"The weather will be {weather_json} with {celsius} °C {time} {accessoire}. I would recommend you to wear a {dress_color} {dress}. Otherwise a {top_color} {top} combined with {article} {bottom_color} {bottom} would be appropriate too." 

        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(WelcomeIntentHandler())
sb.add_request_handler(NewUserIntent())
sb.add_request_handler(OccasionRecIntentHandler())
sb.add_request_handler(WeatherTestIntentHandler())
sb.add_request_handler(SeasonsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()