import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import get_current_weather

load_dotenv()

# Initialize Groq client via OpenAI SDK
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# Tool definition schema for LLM function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather and temperature for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g., 'Auckland', 'London'"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

def run_agent():
    print("⚡ Groq Agent: Weather-Aware Travel Planner initialized.")
    print("Type 'quit' to exit.\n")
    
    # Core context memory setup
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI travel assistant. Your goal is to customize itineraries based on destination weather.\n"
                "Core Logic:\n"
                "1. Always invoke the weather tool first when a user asks about a city.\n"
                "2. Conditional decision: If it is raining/storming, prioritize indoor spots (museums, galleries, indoor dining).\n"
                "   If the weather is clear/sunny, prioritize outdoor activities (parks, beaches, walking tours).\n"
                "3. Explicitly state the weather condition in your final response and justify your choices based on it."
            )
        }
    ]

    while True:
        user_input = input("🧑 User: ")
        if user_input.lower() == 'quit':
            print("Agent stopped. Bye!")
            break
            
        if not user_input.strip():
            continue
            
        messages.append({"role": "user", "content": user_input})

        # Step 1: Perceive input & decide on tool execution
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        msg = response.choices[0].message
        messages.append(msg)

        # Step 2: Handle conditional action execution
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                city = args.get("city")
                
                print(f"🤖 [Agent Log]: Target city '{city}' detected. Executing action -> Calling Weather API...")
                
                if func_name == "get_current_weather":
                    weather_data = get_current_weather(city=city)
                    print(f"📡 [Tool Output]: {weather_data}")
                    
                    # Feed tool results back into context memory
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": weather_data
                    })
            
            # Step 3: Generate customized itinerary based on live weather
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            reply = final_response.choices[0].message.content
            print(f"\n✈️ Travel Planner:\n{reply}\n")
            messages.append({"role": "assistant", "content": reply})
        else:
            # Fallback handling for standard conversations
            print(f"\n✈️ Travel Planner:\n{msg.content}\n")

        # Save session logs locally to demonstrate persistence
        with open("chat_history.json", "w") as f:
            json.dump([m if isinstance(m, dict) else m.model_dump() for m in messages], f, indent=4)

if __name__ == "__main__":
    run_agent()