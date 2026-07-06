from agents.skills_agent import skills_agent

def skills_node(state):
    state["skills"] = skills_agent(
        state["cv_data"],
        state["job_data"]
    )
    return state