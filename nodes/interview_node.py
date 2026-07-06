from agents.interview_agent import interview_agent

def interview_node(state):
    state["interview"] = interview_agent(
        state["cv_data"],
        state["job_data"]
    )
    return state