from agents.matching_agent import matching_agent

def match_node(state):
    state["match"] = matching_agent(
        state["cv_data"],
        state["job_data"]
    )
    return state