from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.auth.authenticate import authenticate
from app.service.RiddleService import RiddleService
from app.service.UserService import UserService
from app.util.util import *


def get_riddle_router(userService: UserService, riddleService: RiddleService):
    router = APIRouter()

    # 모든 riddle 보여주기
    @router.get('/list')
    async def show_all_riddle(request: Request):
        token = get_token_from_header(request)
        await authenticate(token)
        riddles = riddleService.get_all_riddle()
        all_riddles = [{'riddleId': riddle.riddle_id, 'riddleTitle': riddle.title} for riddle in riddles]
        return JSONResponse(content=all_riddles)

    # 새로운 riddle 생성
    @router.post('/new')
    async def create_riddle(request: Request):
        try:
            token = get_token_from_header(request)
            user_email = await authenticate(token)
            user = userService.get_user_email(user_email)
            body = await request.json()
            riddleTitle = body.get('riddleTitle')
            problem = body.get('problem')
            situations = body.get('situations')
            answers = body.get('answers')

            if userService.create_riddle(user.user_id) is True:
                problem_embedding, situation_embeddings, answer_embedding = get_embeddings(problem, situations, answers)
                riddle_id = riddleService.create_riddle(user_email, riddleTitle, problem, situations, answers,
                                                        problem_embedding, situation_embeddings, answer_embedding)
                return JSONResponse(content={'riddleId': riddle_id})
            else:
                return JSONResponse(content={'error': "Failed to create game"}, status_code=400)
        except Exception as e:
            print(str(e))
            return JSONResponse(content={"error": str(e)}, status_code=404)

    # riddle 점수 매기기
    @router.patch('/point')
    async def update_riddle(request: Request):
        try:
            body = await request.json()
            riddle_id = body.get('riddleId')
            point = body.get('point')

            riddleService.set_point(riddle_id, point)
            return JSONResponse(content={'riddleId': riddle_id})
        except Exception as e:
            print(str(e))
            return JSONResponse(content={"error": str(e)}, status_code=404)

    return router
