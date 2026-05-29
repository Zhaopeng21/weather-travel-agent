import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from tools import get_current_weather

load_dotenv()

# Page configuration
st.set_page_config(page_title="Weather Travel Planner", page_icon="✈️", layout="centered")
st.title("✈️ Weather-Aware Travel Planner")
st.caption("⚡ Powered by Groq (Llama 3.3 70B) & OpenWeather API")

# Initialize client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather and temperature for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g., 'Auckland', 'London'"}
                },
                "required": ["city"]
            }
        }
    }
]

# Initialize session state for chat history (Streamlit persistence)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an AI travel assistant. Your goal is to customize itineraries based on destination weather.\n"
                "Core Logic:\n"
                "1. Always invoke the weather tool first when a user asks about a city.\n"
                "2. Conditional decision: If it is raining/storming, prioritize indoor spots.\n"
                "   If the weather is clear/sunny, prioritize outdoor activities.\n"
                "3. Explicitly state the weather condition in your final response and justify your choices based on it."
            )
        }
    ]

# Display visible chat messages (skipping system prompt)
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    if message["role"] in ["user", "assistant"] and "content" in message and message["content"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input box
if user_input := st.chat_input("Where do you want to go? (e.g., I want to visit Tokyo tomorrow)"):
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        with st.spinner("Agent is reasoning and fetching live data..."):
            # Step 1: LLM Reasoning
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto"
            )
            
            msg = response.choices[0].message
            st.session_state.messages.append(msg)

            # Step 2: Tool Execution (if needed)
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    city = args.get("city")
                    
                    st.info(f"🤖 [Agent Log]: Target city '{city}' detected. Querying OpenWeather API...")
                    
                    if func_name == "get_current_weather":
                        weather_data = get_current_weather(city=city)
                        st.success(f"📡 [Tool Output]: {weather_data}")
                        
                        st.session_state.messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": weather_data
                        })
                
                # Step 3: Final response with data integrated
                final_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                reply = final_response.choices[0].message.content
                response_placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                # Direct response
                reply = msg.content
                response_placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})