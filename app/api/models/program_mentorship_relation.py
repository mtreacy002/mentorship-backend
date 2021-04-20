from flask_restx import fields, Model

from app.utils.enum_utils import MentorshipRelationState
from .task import create_task_request_body, list_tasks_response_body
from .task_comment import task_comment_model, task_comments_model


def add_models_to_namespace(api_namespace):
    api_namespace.models[
        send_program_mentorship_request_body.name
    ] = send_program_mentorship_request_body



send_program_mentorship_request_body = Model(
    "Send mentorship relation request model",
    {
        "mentor_id": fields.Integer(
            description="Mentorship relation mentor ID"
        ),
        "mentee_id": fields.Integer(
            description="Mentorship relation mentee ID"
        ),
        "org_rep_id": fields.Integer(
            required=True, description="Organization Representative's ID"
        ),
        "relation_id": fields.Integer(
            description="Mentorship Relation ID"
        ),
        "start_date": fields.Float(
            description="Program start date in UNIX timestamp format",
        ),
        "end_date": fields.Float(
            description="Program end date in UNIX timestamp format",
        ),
        "notes": fields.String(required=True, description="Mentorship relation notes"),
    },
)


