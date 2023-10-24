import file_a
from file_a import get_responses
# Import the Bot class from your bot_file (replace 'bot_file' with the actual filename).
import file_class
from file_class import DOST

# Create an instance of the Bot class
bot = DOST()

# Define a loop to interact with the bot
while True:
    user_input = input('YOU: ')
    response = bot.get_responses(user_input)
    print('DOST: ' + response)


# print('DOST: HI')
# while True:
#     print('DOST: ' + get_responses(input('YOU: ')))