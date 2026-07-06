from agents.cv_agent import cv_agent

def cv_node(state):
    state["cv_data"] = cv_agent(state["cv_text"])
    return state