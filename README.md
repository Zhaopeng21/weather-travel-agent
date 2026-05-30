这里为你整理好了完美的 Markdown 格式。我帮你加上了正确的标题层级、列表排版，并且**修复了代码块未闭合的问题**。

你只需要点击代码框右上角的 **“复制 (Copy)”** 按钮，然后直接粘贴到你的 `README.md` 文件里就可以了：

```markdown
# 🌍 SkyGuide: Interactive AI Travel Concierge

An Elite, Multi-Turn Interactive Travel Agent powered by Large Language Models and Live Meteorological Radar.

## 🚀 Overview

SkyGuide is not just a standard Q&A chatbot. It is a State-Aware Interactive Agent that acts as a professional travel concierge. Instead of passively waiting for a massive prompt, SkyGuide takes the initiative to interview users step-by-step, gathers crucial trip parameters, and dynamically fuses them with real-time weather data to generate a highly customized, weather-optimized travel blueprint.

## ✨ Key Features

* **🧠 Proactive Step-by-Step Interviewing:** The Agent utilizes a "Priority Queue" logic to ask exactly one question per turn (Companions -> Duration -> Budget), creating a natural, human-like consultation experience without overwhelming the user.
* **📡 Real-Time Meteorological Fusion:** Integrates with live weather APIs to ensure the itinerary is strictly bounded by today's climate conditions (e.g., locking indoor routes for heavy rain, or adjusting pacing for high wind speeds).
* **🛡️ State Machine Memory:** Leverages Streamlit's Session State to remember previous constraints across multiple dialogue turns.
* **🎨 Dynamic UI/UX:** A clean, modern Streamlit interface featuring live weather metrics cards that only reveal themselves at the climactic moment of generating the final report.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM Engine:** Llama 3.3 70B (via Groq API)
* **SDK/Routing:** `openai` (Python SDK for LLM interactions)
* **External API:** OpenWeather API (via `requests`)
* **Environment Management:** `python-dotenv`

## 📂 Project Structure

```text
├── app.py              # Streamlit frontend & UI layout
├── agent.py            # Core Agent logic, Prompt Engineering & Multi-turn reasoning
├── tools.py            # Tool calling functions (Live Weather API integration)
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (API Keys)
└── README.md           # Project documentation

```

## ⚙️ Installation & Setup

**1. Clone the Repository**
Navigate into your project directory or extract the source folder:

```bash
cd your-project-folder

```

**2. Install Dependencies**
Install all required Python packages using pip:

```bash
pip install -r requirements.txt

```

**3. Configure Environment Variables**
Create a file named `.env` in the root directory of the project.

> ⚠️ **CRITICAL SECURITY NOTE:** The `.env` file contains your private API credentials. Keep it strictly on your local machine and NEVER commit or push it to GitHub.

Add your personal API tokens using the following template:

```env
GROQ_API_KEY="your_groq_api_key_here"
OPENWEATHER_API_KEY="your_openweather_api_key_here"

```

*(Note: You can obtain your credentials from the Groq Console and OpenWeather Map Portal.)*

**4. Run the Application**
Launch the local Streamlit web server:

```bash
streamlit run app.py

```

## 💡 Usage Example

* **Initialize the Session:** Open the local Streamlit web URL provided in your terminal (typically `http://localhost:8501`).
* **State Your Destination:** Enter a straightforward prompt in the chat input, for example: *"I want to visit Tokyo."*
* **Interactive Multi-Turn Interview:** The Concierge will NOT generate the itinerary immediately. Driven by a state-aware priority queue protocol, it will gracefully interview you step-by-step over the next few turns, asking about your Companions, Trip Duration, and Budget Level one question at a time.
* **Live Meteorological Blueprint:** Once all 4 core dimensions are successfully gathered, the system triggers the live weather tool. The interface will instantly reveal current weather metric cards and output a personalized, multi-day travel blueprint optimized for today's weather conditions!

---

*Developed by Zhaopeng Wen • 2026*

```

```
