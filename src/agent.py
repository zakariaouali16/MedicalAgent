import operator
from typing import Annotated, TypedDict, List, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_google_vertexai import ChatVertexAI
from safety import detect_emergency 

# --- 1. SETUP THE BRAIN ---
llm = ChatVertexAI(
    model_name="gemini-2.5-flash",
    temperature=0, 
    location="us-central1"
)

# --- 2. DEFINE MEMORY ----
class AgentState(TypedDict):
    # We use 'add' so we don't overwrite history, we append to it
    messages: Annotated[List[BaseMessage], operator.add]
    is_emergency: bool
    next_step: str # specific flag to control flow

# --- 3. DEFINE THE NODES ---

def safety_node(state: AgentState):
    """Checks the LAST user message for hard-coded emergencies."""
    last_message = state['messages'][-1]
    if isinstance(last_message, HumanMessage):
        if detect_emergency(last_message.content):
            # Overwrite the flow to stop immediately
            return {"is_emergency": True, "messages": [AIMessage(content="🚨 SYSTEM ALERT: Call 911.")]}
    return {"is_emergency": False}

def chatbot_node(state: AgentState):
    """
    The Investigator. It gathers Onset, Severity, and Duration.
    """
    sys_msg = SystemMessage(content="""
    You are CareNavigator, a medical triage assistant.
    Your goal is to gather these 3 specific pieces of info:
    1. Onset (When did it start?)
    2. Severity (1-10 scale)
    3. Duration (Constant or intermittent?)
    
    Current State of conversation: Check the history.
    - If you are missing any of the 3, ask for the missing one.
    - Ask ONE question at a time.
    - If you have ALL 3, output EXACTLY: "DATA_COLLECTED"
    """)
    
    response = llm.invoke([sys_msg] + state['messages'])
    return {"messages": [response]}

def triage_node(state: AgentState):
    """
    The Decision Maker. Runs ONLY when data is collected.
    """
    sys_msg = SystemMessage(content="""
    You are a Triage Nurse. Review the conversation history.
    Based strictly on the Onset, Severity, and Duration provided:
    1. Classify Urgency: (Low, Medium, High, Critical)
    2. Recommend Care: (Home Care, Urgent Care, ER)
    3. Summarize the symptoms.
    """)
    
    response = llm.invoke([sys_msg] + state['messages'])
    return {"messages": [response]}

# --- 4. DEFINE THE LOGIC (EDGES) ---

def route_step(state: AgentState) -> Literal["emergency_stop", "finalize_triage", "continue_interview"]:
    # 1. Did we hit a hard safety stop?
    if state.get("is_emergency"):
        return "emergency_stop"
    
    # 2. Did the chatbot say it has all the data?
    last_msg = state["messages"][-1].content
    if "DATA_COLLECTED" in last_msg:
        return "finalize_triage"
    
    # 3. Otherwise, stop here and wait for user input (Standard chat loop)
    return "continue_interview"

# --- 5. BUILD THE GRAPH ---
workflow = StateGraph(AgentState)

workflow.add_node("safety_check", safety_node)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("triage", triage_node)

# Start at Safety
workflow.set_entry_point("safety_check")

# Logic: Safety -> Chatbot (if safe)
workflow.add_edge("safety_check", "chatbot")

# Logic: After Chatbot speaks, decide what to do
workflow.add_conditional_edges(
    "chatbot",
    route_step,
    {
        "emergency_stop": END,      # Hard stop
        "finalize_triage": "triage", # Go to summary
        "continue_interview": END   # Stop graph, wait for user input
    }
)

# After Triage speaks, we are done
workflow.add_edge("triage", END)

agent_app = workflow.compile()