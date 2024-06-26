from app.domain.Feedback import Feedback


class FeedbackService:
    def __init__(self, session):
        self.session = session

    def create_feedback(self, query_id, content):
        feedback = Feedback(query_id=query_id, content=content)

        self.session.add(feedback)
        self.session.commit()

        return feedback.feedback_id

    def get_feedback_by_query_id(self, query_id):
        feedback = self.session.query(Feedback).filter_by(query_id=query_id).first()
        if feedback:
            return feedback
        else:
            return None

    def get_all_feedback(self):
        return self.session.query(Feedback).all()

    def update_feedback(self, query_id, content):
        feedback = self.get_feedback_by_query_id(query_id)
        if feedback:
            feedback.content = content
            self.session.commit()
        return feedback.feedback_id

    def delete_feedback(self, query_id):
        feedback = self.get_feedback_by_query_id(query_id)
        if feedback:
            self.session.delete(feedback)
            self.session.commit()
