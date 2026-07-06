from state import RecruitmentState

from nodes.cv_node import cv_node
from nodes.job_node import job_node
from nodes.match_node import match_node
from nodes.skills_node import skills_node
from nodes.interview_node import interview_node
from nodes.placement_node import placement_node


def run_graph(cv_text, job_text):

    state = RecruitmentState(
        cv_text=cv_text,
        job_text=job_text,
        cv_data={},
        job_data={},
        match={},
        skills={},
        interview={},
        placement={}
    )

    # FLOW CONTROL (LIKE LANGGRAPH)
    state = cv_node(state)
    state = job_node(state)

    state = match_node(state)
    state = skills_node(state)

    state = interview_node(state)
    state = placement_node(state)

    return state