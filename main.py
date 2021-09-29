from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
import intents

sb = SkillBuilder()
sb.add_request_handler(intents.LaunchRequestHandler())
sb.add_request_handler(intents.HelpIntentHandler())
sb.add_request_handler(intents.CancelOrStopIntentHandler())
sb.add_request_handler(intents.HelloWorldIntentHandler())
sb.add_request_handler(intents.SessionEndedRequestHandler())
sb.add_request_handler(intents.GetCryptoPricesIntentHandler())
sb.add_request_handler(intents.IntentReflectorHandler()) 

app = Flask(__name__)
skill_id = 'amzn1.ask.skill.172383ce-082b-4e74-a96e-158e12ea41e0'

skill_adapter = SkillAdapter(
  skill=sb.create(), 
  skill_id=skill_id, app=app
  )

@app.route("/", methods=["GET", "POST"])
def invoke_skill():
    return skill_adapter.dispatch_request()

app.run('0.0.0.0', port=443)
