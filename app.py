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
            "description": "Get current detailed weather, temperature, wind, and cloud analytics for a specific city.",
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

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an enterprise-grade AI Travel & Weather Risk Consultant. Your core capability is Multi-Variable Collaborative Decision Making based on live meteorological data.\n\n"
                "CRITICAL MATRIX & CONTROL FLOW:\n"
                "1. MANDATORY ACQUISITION: Always call 'get_current_weather' when a destination is mentioned. Extract these EXACT keys from the JSON tool response: 'temp', 'feels_like', 'wind_speed', 'clouds_all', and 'weather_main'.\n\n"
                "2. TEMPERATURE INTERSECTION:\n"
                "   - feels_like > 32°C: Issue extreme heat warning. SUSPEND mid-day outdoor activities. Route to air-conditioned indoor venues.\n"
                "   - feels_like < 5°C: Issue cold/frostbite warning. Recommend heavy winter gear, indoor heated venues, or hot springs.\n"
                "   - 15°C <= feels_like <= 25°C: Optimal. Prioritize walking tours and extensive outdoor exploration.\n\n"
                "3. WIND SPEED DYNAMIC ROUTING:\n"
                "   - wind_speed > 8 m/s: Trigger a Safety Fuse. Automatically CANCEL and explicitly warn against cable cars, boat cruises, ferries, and high-altitude activities. Re-route to low-altitude city walks or indoor activities.\n\n"
                "4. CLOUD COVER OVERRIDE:\n"
                "   - clouds_all > 80% or weather_main is 'Fog'/'Mist': Do NOT recommend panoramic viewpoints, skyscrapers, or mountain peaks. State that visibility is poor and pivot to cultural experiences, museums, or shopping.\n\n"
                "5. PRECIPITATION STRICT ROUTING:\n"
                "   - weather_main contains 'Rain'/'Thunderstorm'/'Snow': Terminate all outdoor recommendations. Lock the itinerary to 100% indoor destinations.\n\n"
                "OUTPUT FORMAT REQUIREMENTS:\n"
                "- LANGUAGE: STRICTLY respond in fluent, professional English. Never use Chinese in your response.\n"
                "- STRUCTURE:\n"
                "  * Step 1: [Real-Time Meteorological Diagnostic] List precise metrics (Temp, Feels Like, Wind Speed, Cloud Cover) and translate them into a 'Travel Comfort Level'.\n"
                "  * Step 2: [Safety & Precaution Warnings] Issue specific warnings/fuses based on the metrics.\n"
                "  * Step 3: [Customized Itinerary] Provide an optimized itinerary strictly adhering to the routing rules above, explicitly justifying *why* each place was chosen based on the weather data."
            )
        }
    ]

# Display visible chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    if message["role"] in ["user", "assistant"] and "content" in message and message["content"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input box
if user_input := st.chat_input("Where do you want to go? (e.g., I want to visit Tokyo tomorrow)"):
    
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning and fetching live data..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto"
            )
            
            msg = response.choices[0].message
            st.session_state.messages.append(msg)

            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    city = args.get("city")
                    
                    # 💡 【修改点】删除了原先展示在前端的 st.info 日志提示
                    
                    if func_name == "get_current_weather":
                        weather_data = get_current_weather(city=city)
                        
                        # 💡 【修改点】删除了原先展示在前端的 st.success 数据提示
                        
                        st.session_state.messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": weather_data
                        })
                
                final_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                reply = final_response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                reply = msg.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})