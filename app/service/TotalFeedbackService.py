from app.domain.TotalFeedback import Total_Feedback


class TotalFeedbackService:
    def __init__(self, session):
        self.session = session

    def create_totalFeedback(self, user_id, content):
        total_feedback = Total_Feedback(user_id=user_id, content=content)
        self.session.add(total_feedback)
        self.session.commit()

        return total_feedback.total_feedback_id

    def get_totalFeedback_by_user_id(self, user_id):
        return self.session.query(Total_Feedback).filter_by(user_id=user_id).first()

    def get_totalFeedback_by_total_feedback_id(self, total_feedback_id):
        return self.session.query(Total_Feedback).filter_by(total_feedback_id=total_feedback_id).first()

    def get_all_totalFeedback(self):
        return self.session.query(Total_Feedback).all()

    def update_totalFeedback(self, total_feedback_id, content):
        total_feedback = self.get_totalFeedback_by_total_feedback_id(total_feedback_id)
        total_feedback.content = content
        self.session.commit()

        return total_feedback.total_feedback_id

    def delete_totalFeedback(self, user_id):
        total_feedback = self.get_totalFeedback_by_user_id(user_id)
        if total_feedback:
            self.session.delete(total_feedback)
            self.session.commit()
