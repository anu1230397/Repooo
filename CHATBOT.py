import random
from datetime import datetime

def chatbot():
    print("🤖 ChatBot: Hello! I am your Python chatbot.")
    print("Type 'bye' to exit.\n")

    responses = {
        "hello": ["Hello!", "Hi there!", "Hey! How can I help you?"],
        "hi": ["Hi!", "Hello!", "Nice to meet you!"],
        "how are you": ["I'm doing great!", "I'm fine, thanks!"],
        "what is your name": ["I am PyBot.", "You can call me PyBot!"],
        "thank you": ["You're welcome!", "Happy to help!"]
    }

    while True:
        user = input("You: ").lower().strip()

        if user == "bye":
            print("🤖 ChatBot: Goodbye! Have a great day!")
            break

        elif "time" in user:
            current_time = datetime.now().strftime("%H:%M:%S")
            print("🤖 ChatBot:", current_time)

        elif user in responses:
            print("🤖 ChatBot:", random.choice(responses[user]))

        else:
            print("🤖 ChatBot: Sorry, I don't understand that yet.")

chatbot()