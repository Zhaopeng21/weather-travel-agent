import streamlit as st
from agent import handle_agent_reasoning

# 1. 前端高级配置（Wide模式大盘）
st.set_page_config(
    page_title="SkyGuide Personal Concierge", 
    page_icon="🌍", 
    layout="wide"
)

# 2. 侧边栏设计 (Sidebar)
with st.sidebar:
    st.markdown("## 🌍 SkyGuide Concierge")
    st.markdown("### *Interactive Luxury Travel Agent*")
    
    # 💡 【完美去报错改动】：直接调用最安全的 HTML 渲染图片法，100% 撑满且彻底消灭未来的 Deprecation 警告！
    st.markdown(
        '<img src="https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=500&auto=format&fit=crop" style="width:100%; border-radius:10px; margin-bottom:15px;">', 
        unsafe_allow_html=True
    )
    
    st.write("---")
    st.markdown("#### ⚙️ Engine Matrix")
    st.success("● Mode: Interactive Interview")
    st.info("● LLM: Llama 3.3 70B")
    st.warning("● Persona: Travel Concierge")
    st.write("---")
    st.caption("Developed by Zhaopeng Wen • 2026")

# 3. 主界面核心呈现（增加视觉层次感）
st.title("🌍 SkyGuide: Interactive AI Travel Concierge")
st.markdown("##### 🚀 *An intelligent consultant that interviews you to build weather-optimized, ultra-personalized journeys.*")

# 💡 增加一个优雅的欢迎提示卡片，让用户一进来不觉得空旷
st.info("👋 **Welcome to SkyGuide!** Tell me where you'd like to visit, and I will guide you through a personalized planning session.")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 建立一个动态卡片卡槽
metrics_container = st.container()

# 渲染对话历史
for message in st.session_state.messages:
    if isinstance(message, dict) and message.get("role") in ["user", "assistant"] and message.get("content"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 用户输入交互
if user_input := st.chat_input("Type your response here... (e.g., I want to plan a trip to Tokyo!)"):
    
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("⏳ Concierge is reviewing your profile..."):
            
            # 把对话丢给大脑
            reply, weather_analytics = handle_agent_reasoning(st.session_state.messages)
            
            # 💡 只有最后信息收齐、API被触发了，才会帅气地亮出实时数据大盘
            if weather_analytics:
                with metrics_container:
                    st.markdown("### 📊 Live Climate Analytics for Your Destination")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(label="🌡️ Temperature", value=f"{weather_analytics.get('temp')} °C")
                    with col2:
                        st.metric(label="🧠 Feels Like", value=f"{weather_analytics.get('feels_like')} °C")
                    with col3:
                        st.metric(label="💨 Wind Speed", value=f"{weather_analytics.get('wind_speed')} m/s")
                    with col4:
                        st.metric(label="☁️ Cloud Cover", value=f"{weather_analytics.get('clouds_all')} %")
                    st.write("---")
            
            # 显示文本（可能是追问，也可能是最后的行程报告）
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})