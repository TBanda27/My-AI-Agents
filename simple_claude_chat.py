"""
Simple Chat Interface with Claude
Type messages and see Claude's responses
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Claude
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def chat(message):
    """Send a message to Claude and get response"""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": message
            }]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {e}"


def main():
    print("=" * 60)
    print("Chat with Claude - Testing Interface")
    print("=" * 60)
    print("Type your messages and press Enter")
    print("Type 'quit' to exit\n")

    while True:
        # Get user input
        user_message = input("You: ").strip()

        # Exit command
        if user_message.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye! 👋")
            break

        # Skip empty messages
        if not user_message:
            continue

        # Get Claude's response
        print("\nClaude: ", end="", flush=True)
        response = chat(user_message)
        print(response + "\n")


if __name__ == "__main__":
    main()