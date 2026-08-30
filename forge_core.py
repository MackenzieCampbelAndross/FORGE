import os
import time
import google.generativeai as genai
from typing import TypedDict
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API Key not found in .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.6-flash') 

# --- ROBUST API CALLER (Fixes 429 Errors) ---
def call_gemini(prompt: str, retries=3):
    for attempt in range(retries):
        try:
            # 1. Be polite to the API (Wait 2s between calls)
            time.sleep(2) 
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = 15 * (attempt + 1) # Wait 15s, then 30s, then 45s
                print(f"   [!] Speed Limit Hit. Cooling down for {wait_time}s...")
                time.sleep(wait_time)
            else:
                return f"Error: {e}"
    
    return "Failed to generate content after multiple retries."

# --- STATE ---
class ForgeState(TypedDict):
    objective: str
    strategy_doc: str
    architecture_doc: str
    security_policy: str
    final_report: str
    step: str

# --- AGENTS ---

def strategy_agent(state: ForgeState):
    print("\n[1/4] 🧠 STRATEGY AGENT: Analyzing market fit...")
    prompt = f"Role: Chief Strategy Officer. Objective: {state['objective']}. Output: 3 bullet strategic brief."
    output = call_gemini(prompt)
    return {"strategy_doc": output, "step": "strategy_done"}

def architect_agent(state: ForgeState):
    print("[2/4] 🏗️  SYSTEM ARCHITECT: Designing stack...")
    prompt = f"Role: System Architect. Strategy: {state['strategy_doc']}. Output: Tech Stack (Frontend, Backend, DB, Cloud)."
    output = call_gemini(prompt)
    return {"architecture_doc": output, "step": "architect_done"}

def security_agent(state: ForgeState):
    print("[3/4] 🛡️  SECURITY ARCHITECT: Threat modeling...")
    prompt = f"Role: CISO. Stack: {state['architecture_doc']}. Output: 3 security risks & fixes."
    output = call_gemini(prompt)
    return {"security_policy": output, "step": "security_done"}

def supervisor_agent(state: ForgeState):
    print("[4/4] 👁️  SUPERVISOR: Compiling report...")
    final_output = f"""
    ==================================================
    🔥 FORGE SYSTEM BLUEPRINT (v0.5 Stable)
    ==================================================
    🎯 OBJECTIVE: {state['objective']}
    
    --- 🧠 STRATEGY ---
    {state['strategy_doc']}
    
    --- 🏗️ ARCHITECTURE ---
    {state['architecture_doc']}
    
    --- 🛡️ SECURITY ---
    {state['security_policy']}
    
    [STATUS: COMPLETE]
    """
    return {"final_report": final_output, "step": "finished"}

# --- GRAPH ---
workflow = StateGraph(ForgeState)
workflow.add_node("strategy", strategy_agent)
workflow.add_node("architect", architect_agent)
workflow.add_node("security", security_agent)
workflow.add_node("supervisor", supervisor_agent)

workflow.set_entry_point("strategy")
workflow.add_edge("strategy", "architect")
workflow.add_edge("architect", "security")
workflow.add_edge("security", "supervisor")
workflow.add_edge("supervisor", END)

app = workflow.compile()

if __name__ == "__main__":
    print("="*60)
    print("FORGE v0.5 | AUTO-RETRY MODE ENABLED")
    print("="*60)
    user_input = input(">> ENTER SYSTEM OBJECTIVE: ")
    res = app.invoke({"objective": user_input, "step": "start"})
    print(res['final_report'])