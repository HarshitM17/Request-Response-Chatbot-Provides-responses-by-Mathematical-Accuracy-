import re


# Import long_responses as lr if needed

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
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

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'sup', 'hey', 'heya'], single_response=True)
    response('I\'m doing fine and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('Great!!:), what is your name?', ['good','happy','well'], single_response=True)
    response('Ohh!! it is a good name, my name is DOST', ['my', 'name', 'is'], required_words=['harshit'])
    response('Hi I am DOST a specialised response model to help you out as friend',['can','you','tell','me','about','yourself'],single_response=True)
    # response('')
    response('If you are facing this issue you can use the below scipt execution button which will help you out to correct this.'+'\n'+'Thanks',['I', 'am', 'facing', 'sailor', 'seeing', 'another', 'sailor'],single_response=True)

    

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    return best_match

def get_responses(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

# while True:
#     print('DOST: ' + get_responses(input('YOU: ')))
