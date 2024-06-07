from datetime import time

from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.service.RankingService import RankingService
from app.util.util import *


def get_ranking_router(rankingService: RankingService):
    router = APIRouter()

    @router.get('')
    async def get_ranking(request: Request):
        try:
            body = await request.json()
            riddle_id = body.get('riddleId')
            top_rankings = rankingService.get_top_ranking(riddle_id)
            all_top_rankings = [{'rank': ranking.rank, 'userId': ranking.user_id, 'userName': ranking.user_name,
                                 'correctTime': ranking.correct_time.isoformat() if isinstance(ranking.correct_time, time) else ranking.correct_time}
                                for ranking in top_rankings]
            return JSONResponse(content=all_top_rankings)
        except Exception as e:
            print(str(e))
            return JSONResponse(content={"error": str(e)}, status_code=404)

    return router
