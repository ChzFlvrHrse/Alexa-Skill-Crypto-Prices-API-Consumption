import os
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import AskForPermissionsConsentCard
import requests
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = 'Hi! I heard you were curious about the top crypto prices today.'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
  """Handler for Hello World Intent."""
  def can_handle(self, handler_input):
    print('checking if we can handle')
    return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

  def handle(self, handler_input):
    speak_output = "Hello World!"

    return (
      handler_input.response_builder
          .speak(speak_output)
          .response
    )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "This intent handler is not finished yet!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
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
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


#_______________________________________________________________________

permissions = ["read::alexa:device:all:address"]

#_______________________________________________________________

class GetCryptoPricesIntentHandler(AbstractRequestHandler):
  """Handler for the get blog intent"""
  def can_handle(self, handler_input):
    return ask_utils.is_intent_name("GetCryptoPricesIntent")(handler_input)

  def handle(slf, handler_input):
    # api_key = '97a8863e-ba94-4740-bfc0-cfe9f1cdf0de'
    api_key = os.environ['key']
    base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    parameters = {'start': 1, 'limit': 5, 'convert':'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}

    session = Session()
    session.headers.update(headers)

    coin_prices = [] 

    try:
      response = session.get(base_url, params=parameters)
      data = json.loads(response.text)
      for i in range(0, 5):
        coin_prices.append(str(data['data'][i]['name']))
        coin_prices.append(str(round(data['data'][i]['quote']['USD']['price'], 3)))
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return(e)
  
    speak_output = 'The number one ranked coin today is ' + coin_prices[0] + ', priced at ' + coin_prices[1] + ' dollars. The second ranked coin today is ' + coin_prices[2] + ', priced at ' + coin_prices[3] + ' dollars. The third ranked coin today is ' + coin_prices[4] + ', priced at ' + coin_prices[5] + ' dollars. The fourth ranked coin today is ' + coin_prices[6] + ', priced at ' + coin_prices[7] + ' dollars. The fifth ranked coin today is ' + coin_prices[8] + ', priced at ' + coin_prices[9] + ' dollars.'
  
    return (
      handler_input.response_builder
          .speak(speak_output)
          .response)

