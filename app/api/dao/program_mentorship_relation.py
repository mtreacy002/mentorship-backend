from datetime import datetime, timedelta
from typing import Dict
from http import HTTPStatus
from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.utils.decorator_utils import email_verification_required
from app.utils.enum_utils import MentorshipRelationState


class ProgramMentorshipRelationDAO:
    """Data Access Object for program mentorship relation functionalities.

    Provides various functions pertaining to program mentorship.
    """

    def create_program_mentorship_relation_initial_program_mentor(self, user_id: int, data: Dict[str, str]):
        '''
            Create Initial Program Mentorship Relationship between a Program and a Mentor or viceversa
            
            Args:
                user_id: ID of the user initiating this request. Has to be either the mentor or the mentee or the org_rep_id.
            
            data: List containing the mentor_id, org_rep_id ,start_date_timestamp,end_date_timestamp  and notes.


        '''
        action_user_id = user_id
        mentor_id = data["mentor_id"]
        org_rep_id = data["org_rep_id"]
        end_date_timestamp = data["end_date"]
        start_date_timestamp = data["start_date"]
        notes = data["notes"]

        # user_id has to match either org_representative id or mentor_id
        is_valid_user_ids = action_user_id == mentor_id or action_user_id == org_rep_id
        if not is_valid_user_ids:
            return messages.MATCH_EITHER_MENTOR_OR_ORG_REP, HTTPStatus.BAD_REQUEST
                        
        # mentor_id has to be different from org_representative id
        if mentor_id == org_rep_id:
            return messages.MENTOR_ID_OR_MENTEE_ID_SAME_AS_ORG_REP_ID, HTTPStatus.BAD_REQUEST                
            
        try:
            end_date_datetime = datetime.fromtimestamp(end_date_timestamp)
        except ValueError:
            return messages.INVALID_END_DATE, HTTPStatus.BAD_REQUEST

        now_datetime = datetime.now()
        if end_date_datetime < now_datetime:
            return messages.END_TIME_BEFORE_PRESENT, HTTPStatus.BAD_REQUEST

        # validate if mentor user exists 
        mentor_user = UserModel.find_by_id(mentor_id)
        if mentor_user is None:
            return messages.MENTOR_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        # validate if mentor is available to mentor
        if not mentor_user.available_to_mentor:
            return messages.MENTOR_NOT_AVAILABLE_TO_MENTOR, HTTPStatus.BAD_REQUEST

        # validate if org_rep_user exists    
        org_rep_user = UserModel.find_by_id(org_rep_id)
        if org_rep_user is None:
            return messages.ORG_REP_DOES_NOT_EXIST, HTTPStatus.BAD_REQUEST
        
        # TODO add tests for this portion
                
        all_mentor_relations = (
            mentor_user.mentor_relations + mentor_user.mentee_relations
        )
        for relation in all_mentor_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                return messages.MENTOR_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST
                
        # All validations were checked
        tasks_list = TasksListModel()
        tasks_list.save_to_db()
            
        if action_user_id == org_rep_id:
            mentorship_relation = MentorshipRelationModel(
                action_user_id=action_user_id,
                mentor_user=mentor_user,
                mentee_user=None,
                creation_date=datetime.now().timestamp(),
                end_date=end_date_timestamp,
                state=MentorshipRelationState.PENDING,
                notes=notes,
                tasks_list=tasks_list,
            )
            mentorship_relation.start_date = start_date_timestamp
                
        else:
            mentorship_relation = MentorshipRelationModel(
                action_user_id=action_user_id,
                mentor_user=mentor_user,
                mentee_user=org_rep_user,
                creation_date=datetime.now().timestamp(),
                end_date=end_date_timestamp,
                state=MentorshipRelationState.PENDING,
                notes=notes,
                tasks_list=tasks_list,
            )
            mentorship_relation.start_date = start_date_timestamp
        
        mentorship_relation.save_to_db()
        return messages.PROGRAM_MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, HTTPStatus.CREATED

    def create_program_mentorship_relation_initial_program_mentee(self, user_id: int, data: Dict[str, str]):
        '''
            Create Initial Program Mentorship Relationship between a Program and a Mentee or viceversa
            
            Args:
                user_id: ID of the user initiating this request. Has to be either the mentor or the mentee or the org_rep_id.
            
            data: List containing the mentee_id, org_rep_id ,start_date_timestamp,end_date_timestamp  and notes.
        '''

        action_user_id = user_id
        mentee_id = data["mentee_id"]
        org_rep_id = data["org_rep_id"]
        end_date_timestamp = data["end_date"]
        start_date_timestamp = data["start_date"]
        notes = data["notes"]

        # user_id has to match either org_representative id or mentee_id
        is_valid_user_ids = action_user_id == mentee_id or action_user_id == org_rep_id
        if not is_valid_user_ids:
            return messages.MATCH_EITHER_MENTEE_OR_ORG_REP, HTTPStatus.BAD_REQUEST
                        
        # mentee_id has to be different from org_representative id
        if mentee_id == org_rep_id:
            return messages.MENTOR_ID_OR_MENTEE_ID_SAME_AS_ORG_REP_ID, HTTPStatus.BAD_REQUEST                
            
        try:
            end_date_datetime = datetime.fromtimestamp(end_date_timestamp)
        except ValueError:
            return messages.INVALID_END_DATE, HTTPStatus.BAD_REQUEST

        now_datetime = datetime.now()
        if end_date_datetime < now_datetime:
            return messages.END_TIME_BEFORE_PRESENT, HTTPStatus.BAD_REQUEST

        # validate if mentee user exists 
        mentee_user = UserModel.find_by_id(mentee_id)
        if mentee_user is None:
            return messages.MENTEE_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        # validate if mentee is needs mentoring
        if not mentee_user.need_mentoring:
            return messages.MENTEE_NOT_AVAIL_TO_BE_MENTORED, HTTPStatus.BAD_REQUEST

        # validate if org_rep_user exists    
        org_rep_user = UserModel.find_by_id(org_rep_id)
        if org_rep_user is None:
            return messages.ORG_REP_DOES_NOT_EXIST, HTTPStatus.BAD_REQUEST
        
        # TODO add tests for this portion
                
        all_mentee_relations = (
            mentee_user.mentor_relations + mentee_user.mentee_relations
        )
        for relation in all_mentee_relations:
            if relation.state == menteeshipRelationState.ACCEPTED:
                return messages.MENTEE_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST
                
        # All validations were checked
        tasks_list = TasksListModel()
        tasks_list.save_to_db()
            
        if action_user_id == org_rep_id:
            mentorship_relation = MentorshipRelationModel(
                action_user_id=action_user_id,
                mentee_user=mentee_user,
                mentor_user=None,
                creation_date=datetime.now().timestamp(),
                end_date=end_date_timestamp,
                state=MentorshipRelationState.PENDING,
                notes=notes,
                tasks_list=tasks_list,
            )
            mentorship_relation.start_date = start_date_timestamp
                
        else:
            mentorship_relation = MentorshipRelationModel(
                action_user_id=action_user_id,
                mentee_user=mentee_user,
                mentor_user=org_rep_user,
                creation_date=datetime.now().timestamp(),
                end_date=end_date_timestamp,
                state=MentorshipRelationState.PENDING,
                notes=notes,
                tasks_list=tasks_list,
            )
            mentorship_relation.start_date = start_date_timestamp
        
        mentorship_relation.save_to_db()
        return messages.PROGRAM_MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, HTTPStatus.CREATED
    
    def create_program_mentorship_relation_final_program_mentor(self, user_id: int, relation_id:int, data: Dict[str, str]):
        '''
            Create Final Program Mentorship Relationship between a Program and a Mentor or viceversa
            
            Args:
                user_id: ID of the user initiating this request. Has to be either the mentor or the mentee or the org_rep_id.
                relation_id : ID of the mentorship_relation request is being sent            
            
            data: List containing the mentor_id, org_rep_id ,start_date_timestamp,end_date_timestamp  and notes.            
        '''
        action_user_id = user_id
        mentor_id = data["mentor_id"]
        org_rep_id = data["org_rep_id"]
        notes = data["notes"]

        request = MentorshipRelationModel.find_by_id(relation_id)
        if request is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        request_action_user_id = request.action_user_id
        request_mentor_id = request.mentor_id 
        request_mentee_id = request.mentee_id 
        request_accept_date = request.accept_date

        if request_accept_date is None:
            return messages.MENTORSHIP_RELATION_NOT_IN_ACCEPT_STATE, HTTPStatus.BAD_REQUEST

        mentor_user = UserModel.find_by_id(mentor_id)
        if mentor_user is None:
            return messages.MENTOR_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        # validate if mentor is available to mentor
        if not mentor_user.available_to_mentor:
            return messages.MENTOR_NOT_AVAILABLE_TO_MENTOR, HTTPStatus.BAD_REQUEST

        is_valid_user_ids = action_user_id == mentor_id or action_user_id == org_rep_id
        if not is_valid_user_ids:
            return messages.MATCH_EITHER_MENTOR_OR_ORG_REP, HTTPStatus.BAD_REQUEST
 
        if mentor_id == org_rep_id:
            return messages.MENTOR_ID_OR_MENTEE_ID_SAME_AS_ORG_REP_ID, HTTPStatus.BAD_REQUEST
                
        # TODO add tests for this portion

        all_mentor_relations = (
            mentor_user.mentor_relations + mentor_user.mentee_relations
        )
        for relation in all_mentor_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                return messages.MENTOR_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST

        # All validations were checked
        if action_user_id == org_rep_id:
            request.action_user_id = org_rep_id

        else:
            request.action_user_id = mentor_id
                
        request.mentor_id = mentor_id
        request.notes = notes
        request.save_to_db()
        return messages.PROGRAM_MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, HTTPStatus.CREATED
    
    def create_program_mentorship_relation_final_program_mentee(self, user_id: int, relation_id:int, data: Dict[str, str]):
        '''
            Create Final Program Mentorship Relationship between a Program and a Mentee or viceversa
            
            Args:
                user_id: ID of the user initiating this request. Has to be either the mentor or the mentee or the org_rep_id.
                relation_id : ID of the mentorship_relation request is being sent   

            data: List containing the mentee_id, org_rep_id ,start_date_timestamp,end_date_timestamp  and notes.
        '''
        action_user_id = user_id
        mentee_id = data["mentee_id"]
        org_rep_id = data["org_rep_id"]
        notes = data["notes"]

        request = MentorshipRelationModel.find_by_id(relation_id)
        if request is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        request_action_user_id = request.action_user_id
        request_mentor_id = request.mentor_id 
        request_mentee_id = request.mentee_id 
        request_accept_date = request.accept_date

        if request_accept_date is None:
            return messages.MENTORSHIP_RELATION_NOT_IN_ACCEPT_STATE, HTTPStatus.BAD_REQUEST

        mentee_user = UserModel.find_by_id(mentee_id)
        if mentee_user is None:
            return messages.MENTEE_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
        
        # validate if mentee is needs mentoring
        if not mentee_user.need_mentoring:
            return messages.MENTEE_NOT_AVAIL_TO_BE_MENTORED, HTTPStatus.BAD_REQUEST
        
        is_valid_user_ids = action_user_id == mentee_id or action_user_id == org_rep_id
        if not is_valid_user_ids:
            return messages.MATCH_EITHER_MENTEE_OR_ORG_REP, HTTPStatus.BAD_REQUEST
                
        if mentee_id == org_rep_id:
            return messages.MENTOR_ID_OR_MENTEE_ID_SAME_AS_ORG_REP_ID, HTTPStatus.BAD_REQUEST
                
        # TODO add tests for this portion

        all_mentee_relations = (
            mentee_user.mentor_relations + mentee_user.mentee_relations
        )
        for relation in all_mentee_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                return messages.MENTEE_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST

        # All validations were checked
        if action_user_id == org_rep_id:
            request.action_user_id = org_rep_id

        else:
            request.action_user_id = mentee_id
                
        request.mentee_id = mentee_id
        request.notes = notes
        request.save_to_db()
        return messages.PROGRAM_MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, HTTPStatus.CREATED
    
    @staticmethod
    @email_verification_required
    def accept_request(user_id: int, org_rep_id:int, request_id: int, notes:str):
        """Allows a mentorship request.

        Args:
            user_id: ID of the user accepting the request.
            request_id: ID of the request to be accepted.

        Returns:
            message: A message corresponding to the completed action; success if mentorship relation request is accepted, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        request = MentorshipRelationModel.find_by_id(request_id)

        # verify if request exists
        if request is None:
            return (
                messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST,
                HTTPStatus.NOT_FOUND,
            )

        # verify if request is in pending state
        if request.state != MentorshipRelationState.PENDING:
            return messages.NOT_PENDING_STATE_RELATION, HTTPStatus.FORBIDDEN

        # verify if I'm the receiver of the request
        if request.action_user_id == user_id:
            return messages.CANT_ACCEPT_MENTOR_REQ_SENT_BY_USER, HTTPStatus.FORBIDDEN

        # verify if I'm involved in this relation
        if not (request.mentee_id == user_id or request.mentor_id == user_id or user_id == org_rep_id):
            return messages.CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION, HTTPStatus.FORBIDDEN
                
        my_requests = user.mentee_relations + user.mentor_relations

        # verify if I'm on a current relation
        for my_request in my_requests:
            if my_request.state == MentorshipRelationState.ACCEPTED:
                return (
                    messages.USER_IS_INVOLVED_IN_A_MENTORSHIP_RELATION,
                    HTTPStatus.FORBIDDEN,
                )

        mentee = request.mentee
        mentor = request.mentor
        action_user_id = request.action_user_id
        
        if mentor and mentee:
            # If I am mentor : Check if the mentee isn't in any other relation already
            if user_id == mentor.id:
                mentee_requests = mentee.mentee_relations + mentee.mentor_relations

                for mentee_request in mentee_requests:
                    if mentee_request.state == MentorshipRelationState.ACCEPTED:
                        return messages.MENTEE_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST
            # If I am mentee : Check if the mentor isn't in any other relation already
            elif user_id == mentee.id:
                mentor_requests = mentor.mentee_relations + mentor.mentor_relations

                for mentor_request in mentor_requests:
                    if mentor_request.state == MentorshipRelationState.ACCEPTED:
                        return messages.MENTOR_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST

            if ((action_user_id == mentee.id and user_id == mentor.id) or (action_user_id == mentor.id and user_id == mentee.id)) and (user_id != org_rep_id):
                return messages.CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION, HTTPStatus.FORBIDDEN            

        if action_user_id == org_rep_id:
            request.action_user_id = user.id
            request.notes = notes
            if request.accept_date is not None:
                request.state = MentorshipRelationState.ACCEPTED    
            request.accept_date = datetime.now().timestamp()
            request.save_to_db()
        
        else:
            request.action_user_id = org_rep_id
            request.notes = notes
            if request.accept_date is not None:
                request.state = MentorshipRelationState.ACCEPTED 
            request.accept_date = datetime.now().timestamp()
            request.save_to_db()
        
        return messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY, HTTPStatus.OK
