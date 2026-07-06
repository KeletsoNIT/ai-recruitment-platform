from agents.job_agent import job_agent

def job_node(state):
    state["job_data"] = job_agent(state["job_text"])
    return state