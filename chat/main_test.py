from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
        self.response('Hi I am DOST a specialised response model to help you out as friend',
                      ['can', 'you', 'tell', 'me', 'about', 'yourself'], required_words=True)
        
        # self.response('',[''])
        self.response('If you are facing this issue you can use the below scipt execution button which will help you out to correct this.'+'\n'+'Thanks',
                      ['I', 'am', 'facing', 'sailor', 'seeing', 'another', 'sailor'], single_response=True)

        best_match = max(self.highest_prob_list, key=self.highest_prob_list.get)
        # return best_match

    def get_responses(self, user_input):
        split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
        response = self.check_all_messages(split_message)
        return response

dost_bot = DOST()

@app.post("/ask")
async def ask_question(question: str):
    response = dost_bot.get_responses(question)
    return {"response": response}
