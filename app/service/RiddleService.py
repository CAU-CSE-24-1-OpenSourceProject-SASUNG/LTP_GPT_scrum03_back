import json

from app.domain.Game import Game
from app.domain.Game_Query import Game_Query
from app.domain.Ranking import Ranking
from app.domain.Riddle import Riddle
from app.domain.User_Game import User_Game


class RiddleService:
    def __init__(self, session):
        self.session = session

    def create_riddle(self, creator, title, problem, situation, answer, problem_embedding, situation_embedding,
                      answer_embedding):
        answer = '$'.join(answer)
        situation = '$'.join(situation)
        problem_embedding_str = json.dumps(problem_embedding)
        situation_embedding_str = json.dumps(situation_embedding)  # 다차원 리스트도 JSON 문자열로 변환
        answer_embedding_str = json.dumps(answer_embedding)
        riddle = Riddle(creator=creator, title=title, problem=problem, situation=situation, answer=answer,
                        hit_ratio=0, point_1=0, point_2=0, point_3=0, point_4=0, point_5=0,
                        problem_embedding_str=problem_embedding_str,
                        situation_embedding_str=situation_embedding_str, answer_embedding_str=answer_embedding_str)
        self.session.add(riddle)
        self.session.commit()
        return riddle.riddle_id

    def get_riddle_by_riddle_id(self, riddle_id):
        return self.session.query(Riddle).filter_by(riddle_id=riddle_id).first()

    def get_all_riddle(self):
        return self.session.query(Riddle).all()

    def set_point(self, riddle_id, point):
        riddle = self.get_riddle_by_riddle_id(riddle_id)
        if riddle:
            if point == "1":
                riddle.point_1 += 1
            elif point == "2":
                riddle.point_2 += 1
            elif point == "3":
                riddle.point_3 += 1
            elif point == "4":
                riddle.point_4 += 1
            elif point == "5":
                riddle.point_5 += 1

        self.session.commit()

    def update_hit_ratio(self, riddle_id):
        games = self.session.query(Game).filter_by(riddle_id=riddle_id).all()
        riddle = self.get_riddle_by_riddle_id(riddle_id)
        game_count = len(games)
        hit_game_count = 0

        for game in games:
            if game.hit is True:
                hit_game_count += 1

        if game_count > 0:  # 게임이 있는 경우에만 계산
            riddle.hit_ratio = round((hit_game_count / game_count) * 100, 1)
        else:
            riddle.hit_ratio = 0.0  # 게임이 없는 경우 hit_ratio를 0으로 설정

        self.session.commit()


    def delete_riddle(self, riddle_id):
        riddle = self.get_riddle_by_riddle_id(riddle_id)
        if riddle:
            games = self.session.query(Game).filter_by(riddle_id=riddle.riddle_id).all()
            rankings = self.session.query(Ranking).filter_by(riddle_id=riddle.riddle_id).all()
            if games:
                for game in games:
                    user_game = self.session.query(User_Game).filter_by(game_id=game.game_id).first()
                    game_queries = self.session.query(Game_Query).filter_by(game_id=game.game_id).all()
                    if user_game:
                        self.session.delete(user_game)
                    if game_queries:
                        for game_query in game_queries:
                            self.session.delete(game_query)
                    self.session.delete(game)
            if rankings:
                for ranking in rankings:
                    self.session.delete(ranking)

            self.session.delete(riddle)
            self.session.commit()
