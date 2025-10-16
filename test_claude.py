import os
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()

def test_claude_connection():
    """Test connection to the Claude API."""
    api_key = os.getenv("ANTHROPIC_API_KEY")


    # assert api_key is not None, "ANTHROPIC_API_KEY environment variable not set"
    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY not found in environment variables")
        print("\nTo fix this:")
        print("1. Get your API key from: https://console.anthropic.com/")
        print("2. Set it in your terminal:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        return False

    # Initialize Claude client
    client = Anthropic(api_key=api_key)


    print("Testing connection to Claude API...")
    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Can you respond with 'Connection successful!' if you receive this?"
                }
            ]
        )
        response = message.content[0].text
        print(f"✅ Response from Claude: {response}")
        return True

    except Exception as e:
        print(f"❌ ERROR: Failed to connect to Claude API: {e}")
        return False





test_claude_connection()

