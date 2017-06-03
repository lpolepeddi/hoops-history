import logging

from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement

import time


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def launch():
  return get_new_fact()

@ask.intent('GetNewFactIntent', mapping={'website': 'website'})
def get_new_fact():
  today = time.strftime('%B-%-d').lower()
  template = '{0}'.format(today)

  fact_text = render_template(template)
  return statement(fact_text).simple_card('Hoops History', fact_text)

@ask.intent('AMAZON.HelpIntent')
def help():
  speech_text = 'You can ask me about what happened today in basketball history.'
  return question(speech_text).reprompt(speech_text).simple_card('Livy', speech_text)

@ask.intent('AMAZON.StopIntent')
def stop():
  speech_text = 'Goodbye.'
  return statement(speech_text).simple_card('Hoops History', speech_text)  

@ask.intent('AMAZON.CancelIntent')
def cancel():
  speech_text = 'Goodbye.'
  return statement(speech_text).simple_card('Hoops History', speech_text)  

@ask.session_ended
def session_ended():
  return "", 200


if __name__ == '__main__':
  app.run(debug=True)