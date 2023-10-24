from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # Import Pydantic's BaseModel for defining request body structures

import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DOST:
    def __init__(self):
        self.highest_prob_list = {}
        self.message = ""

    def message_probability(self, user_message, recognised_words, single_response=False, required_words=[]):
        message_certainty = 0
        has_required_words = True

        for word in user_message:
            if word in recognised_words:
                message_certainty += 1

        percentage = float(message_certainty) / float(len(recognised_words))

        for word in required_words:
            if word not in user_message:
                has_required_words = False
                break

        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0

    def response(self, bot_response, list_of_words, single_response=False, required_words=[]):
        self.highest_prob_list[bot_response] = self.message_probability(
            self.message, list_of_words, single_response, required_words)

    def check_all_messages(self, message):
        self.message = message

        self.response('Hello!', ['hello', 'hi', 'sup', 'hey', 'heya'], single_response=True)
        self.response('I\'m doing fine and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
        self.response('Great!!:), what is your name?', ['good', 'happy', 'well'], single_response=True)
        self.response('Ohh!! it is a good name, my name is DOST', ['my', 'name', 'is'], required_words=['name'])
        self.response('Hi I am DOST a specialised response model to help you out as a friend',
              ['can', 'you', 'tell', 'me', 'about', 'yourself'], required_words=['about', 'yourself'])

        
        # self.response('Can you pleae provide a proper message',[''],required_words=[''])
        self.response('This can happen because of merging of two profiles by claiming your sailor-mate booking.'+'\n'+'Thanks',
                      ['sailor', 'seeing', 'another', 'sailor'], required_words=['sailor','seeing','another','sailor'])
        # self.response("I'm sorry, but I don't have knowledge about that.", [], single_response=True)
         

        #Fun Questions!!!!
        self.response('Sure, here is a joke for you: Why don’t scientists trust atoms? Because they make up everything.', 
                      ['can','you','tell','me','a','joke'], required_words=['joke'])
        self.response('The meaning of life is a philosophical question that has no definitive answer.', 
                      ['what', 'is', 'the', 'meaning', 'of', 'life'], required_words=['meaning','life'])
        self.response('I\'m just a chatbot, so I don\'t have personal preferences, but pizza is popular!', 
                      ['do', 'you', 'like', 'to', 'eat'], required_words=['eat'])
        self.response('I cannot provide real-time weather information, but you can check a weather website or app.', 
                      ['what', 'is', 'the', 'weather', 'like', 'today'], required_words=['weather'])
        self.response('Here\'s a fun fact: The shortest war in history was between Britain and Zanzibar on August 27, 1896. It lasted just 38 minutes!', 
                      ['Tell', 'me', 'a', 'fun', 'fact','funfact'], single_response=True)
        self.response('I don\'t have personal favorites, but there are many talented actors to choose from!', 
                      ['Who', 'is', 'your', 'favorite', 'actor'], required_words=['actor'])
        
        


        best_match = max(self.highest_prob_list, key=self.highest_prob_list.get)
        return best_match

    def get_responses(self, user_input):
        split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
        response = self.check_all_messages(split_message)
        return response

dost_bot = DOST()

class QuestionInput(BaseModel):
    # Define the structure of the request body
    question: str  

@app.post("/ask")
async def ask_question(question_input: QuestionInput):
    response = dost_bot.get_responses(question_input.question)
    return {"response": response}

