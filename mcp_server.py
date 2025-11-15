from fastmcp import FastMCP
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------------- MODELS ----------------
class WeatherInput(BaseModel):
    city: str

class WebSearchInput(BaseModel):
    query: str

# ---------------- API CONFIGURATION ----------------
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")  # Optional, using free weather API

# ---------------- MCP SERVER ----------------
mcp = FastMCP("multi-tool-server")

@mcp.tool()
def get_weather(input: WeatherInput):
    """Get current weather for a city using WeatherAPI.com (free tier)"""
    try:
        # Using WeatherAPI.com free tier (no API key needed for basic usage)
        # Alternative: OpenWeatherMap if you have API key
        url = f"https://wttr.in/{input.city}?format=j1"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current_condition"][0]
            location = data["nearest_area"][0]
            
            weather_info = {
                "location": f"{location['areaName'][0]['value']}, {location['country'][0]['value']}",
                "temperature": f"{current['temp_C']}°C / {current['temp_F']}°F",
                "condition": current["weatherDesc"][0]["value"],
                "humidity": f"{current['humidity']}%",
                "wind": f"{current['windspeedKmph']} km/h",
                "feels_like": f"{current['FeelsLikeC']}°C"
            }
            return weather_info
        else:
            return {"error": f"Could not fetch weather for {input.city}"}
    except Exception as e:
        return {"error": f"Weather API error: {str(e)}"}

@mcp.tool()
def web_search(input: WebSearchInput):
    """Search the web using Serper API"""
    if not SERPER_API_KEY:
        return {"error": "SERPER_API_KEY not configured"}
    
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": input.query, "num": 5}
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            # Extract organic results
            for item in data.get("organic", [])[:5]:
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })
            
            # Include knowledge graph if available
            knowledge = data.get("knowledgeGraph", {})
            
            return {
                "query": input.query,
                "results": results,
                "knowledge_graph": knowledge.get("description", "") if knowledge else None
            }
        else:
            return {"error": f"Serper API error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Web search error: {str(e)}"}

if __name__ == "__main__":
    print("🔥 MCP server running...")
    mcp.run()
