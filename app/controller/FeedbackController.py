from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.service.FeedbackService import FeedbackService
from app.service.UserService import UserService
from app.util.util import *


def get_feedback_router(feedbackService: FeedbackService):
    router = APIRouter()

    @router.patch('/update')
    async def update_feedback(request: Request):
        try:
            body = await request.json()
            query_id = body.get('queryId')
            content = body.get('content')

            feedback = feedbackService.get_feedback_by_query_id(query_id)
            if feedback:
                feedback_id = feedbackService.update_feedback(query_id, content)
                return JSONResponse(content={'feedbackId': feedback_id})
            else:
                feedback_id = feedbackService.create_feedback(query_id, content)
                return JSONResponse(content={'feedbackId': feedback_id})
        except Exception as e:
            print(str(e))
            return JSONResponse(content={"error": str(e)}, status_code=404)

    return router
