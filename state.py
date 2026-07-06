from typing import TypedDict, Any


class RecruitmentState(TypedDict):
    cv_text: str
    job_text: str

    cv_data: dict
    job_data: dict

    match: dict
    skills: dict
    interview: dict
    placement: dict