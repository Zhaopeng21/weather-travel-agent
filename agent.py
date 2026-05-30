import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import get_current_weather

# 加载环境变量
load_dotenv()

# 初始化 Groq 客户端
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# 智能体专属：天气工具声明
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current detailed weather analytics (temp, feels_like, wind_speed, clouds_all, weather_main) for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g., 'London', 'Harbin'"}
                },
                "required": ["city"]
            }
        }
    }
]

# 🧠 强制步进版提示词：一次只问一个问题，循序渐进！
SYSTEM_PROMPT = (
    "You are an Elite Last-Minute Travel Planner. You plan immediate trips based on real-time weather data.\n\n"
    "CRITICAL CONVERSATION PROTOCOL:\n"
    "1. NEVER ASK FOR DATES, MONTHS, TIME, OR SEASONS. Assume the user is traveling RIGHT NOW, TODAY.\n\n"
    "2. USER PROFILE CHECKLIST (4 Dimensions):\n"
    "   - Destination (Target City)\n"
    "   - Companions & Travel Style (e.g., solo, family, fast-paced, relaxing)\n"
    "   - Duration (How many days starting from today)\n"
    "   - Budget Level (e.g., backpacker, moderate, luxury)\n\n"
    "3. THE STEP-BY-STEP INTERVIEW RULE (STRICTLY ENFORCED):\n"
    "   - DO NOT ask for all missing information at once. You MUST ask ONE dimension per turn.\n"
    "   - Priority 1: If Companions & Style is missing, ask ONLY about that. Stop and wait for the user.\n"
    "   - Priority 2: If Companions are known but Duration is missing, ask ONLY about how many days. Stop and wait.\n"
    "   - Priority 3: If Duration is known but Budget is missing, ask ONLY about their budget. Stop and wait.\n"
    "   - Keep your responses extremely short, warm, and natural (maximum 1 or 2 sentences per question).\n\n"
    "4. REAL-TIME RADAR EXECUTION:\n"
    "   - Once ALL 4 dimensions are collected across multiple turns, immediately invoke 'get_current_weather'.\n"
    "   - Generate a personalized multi-day itinerary in fluent English:\n"
    "     * Adapt locations to Budget Level.\n"
    "     * Adapt structure to Duration (e.g., Day 1, Day 2).\n"
    "     * Adapt activities STRICTLY to today's live weather (e.g., if temp < 5°C, focus on indoors; if wind > 8 m/s, cancel heights).\n\n"
    "OUTPUT FORMAT REQUIREMENTS:\n"
    "  - FINAL BLUEPRINT (Only output when all 4 dimensions are met and weather is fetched):\n"
    "    * Step 1: [Real-Time Meteorological Diagnostic]\n"
    "    * Step 2: [Profile & Budget Aware Safety Warnings]\n"
    "    * Step 3: [Weather-Aware Personalized Multi-Day Itinerary]"
)

def handle_agent_reasoning(session_messages):
    """
    Step-by-step interactive reasoning engine.
    """
    if not any(m["role"] == "system" for m in session_messages):
        session_messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=session_messages,
        tools=tools,
        tool_choice="auto"
    )
    
    msg = response.choices[0].message
    session_messages.append(msg)
    
    weather_analytics = None

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            city = args.get("city")
            
            if func_name == "get_current_weather":
                weather_data_str = get_current_weather(city=city)
                try:
                    weather_analytics = json.loads(weather_data_str)
                except:
                    weather_analytics = None
                
                session_messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": func_name,
                    "content": weather_data_str
                })
        
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=session_messages
        )
        reply = final_response.choices[0].message.content
        return reply, weather_analytics
        
    else:
        return msg.content, None