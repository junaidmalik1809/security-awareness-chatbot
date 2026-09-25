from src.chatbot import SecurityChatbot
from pathlib import Path

def main():
    knowledge_path = Path("data") / "knowledge_base.json"
    bot = SecurityChatbot(str(knowledge_path))

    print("=" * 60)
    print("Cybersecurity Awareness Chatbot")
    print("Type your questions about security topics.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot:", bot.get_response("bye"))
            break

        if not user_input:
            continue

        response = bot.get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()