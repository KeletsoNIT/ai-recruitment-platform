from agents.placement_agent import placement_agent

def placement_node(state):
    state["placement"] = placement_agent(
        state["cv_data"]
    )
    return state