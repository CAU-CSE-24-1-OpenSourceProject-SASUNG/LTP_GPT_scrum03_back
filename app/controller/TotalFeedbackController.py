from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.auth.authenticate import authenticate
from app.service.UserService import UserService
from app.service.TotalFeedbackService import TotalFeedbackService
from app.util.util import *


def get_totalFeedback_router(userService: UserService, totalFeedbackService: TotalFeedbackService):
    router = APIRouter()

    @router.patch('/update')
    async def update_totalFeedback(request: Request):
        try:
            token = get_token_from_header(request)
            user_email = await authenticate(token)
            user = userService.get_user_by_email(user_email)
            body = await request.json()
            content = body.get('content')

            totalFeedback = totalFeedbackService.get_totalFeedback_by_user_id(user.user_id)
            if totalFeedback:
                total_feedback_id = totalFeedbackService.update_totalFeedback(totalFeedback.total_feedback_id, content)
                return JSONResponse(content={'totalFeedbackId': total_feedback_id})
            else:
                total_feedback_id = totalFeedbackService.create_totalFeedback(user.user_id, content)
                return JSONResponse(content={'totalFeedbackId': total_feedback_id})
        except Exception as e:
            print(str(e))
            return JSONResponse(content={"error": str(e)}, status_code=404)

    return router
