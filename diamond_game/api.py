# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from typing import Optional
# from .storage import manager
# from .game import Game

# app = FastAPI(title="Diamond Card Game API", version="1.0.0")

# # ---------- Schemas ----------
# class CreateGameReq(BaseModel):
#     human_name: str = Field(default="You", min_length=1)
#     bot_level: str = Field(default="medium")  # easy/medium/hard/expert

# class CreateGameResp(BaseModel):
#     game_id: str
#     status: dict

# class PlayReq(BaseModel):
#     human_value: int = Field(ge=1, le=13, description="Your bid card value (1..13)")

# class PlayResp(BaseModel):
#     round_no: int
#     diamond: str
#     human_play: str
#     bot_play: str
#     winner: str
#     points: int
#     scores: dict
#     remaining_human_cards: list
#     remaining_diamonds_count: int
#     active: bool

# # ---------- Endpoints ----------
# @app.post("/games", response_model=CreateGameResp)
# def create_game(req: CreateGameReq):
#     g = manager.create(human_name=req.human_name, bot_level=req.bot_level)
#     return CreateGameResp(game_id=g.id, status=g.status())

# @app.get("/games/{game_id}")
# def get_status(game_id: str):
#     try:
#         g = manager.get(game_id)
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Game not found")
#     return g.status()

# @app.post("/games/{game_id}/play", response_model=PlayResp)
# def play_round(game_id: str, req: PlayReq):
#     try:
#         g = manager.get(game_id)
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Game not found")

#     try:
#         result = g.play_round(req.human_value)
#     except (RuntimeError, ValueError) as e:
#         raise HTTPException(status_code=400, detail=str(e))

#     status = g.status()
#     return PlayResp(
#         round_no=result.round_no,
#         diamond=str(result.diamond),
#         human_play=str(result.human_play),
#         bot_play=str(result.bot_play),
#         winner=result.winner,
#         points=result.points,
#         scores=status["scores"],
#         remaining_human_cards=status["remaining_human_cards"],
#         remaining_diamonds_count=status["remaining_diamonds_count"],
#         active=status["active"],
#     )

# @app.get("/games/{game_id}/score")
# def show_score(game_id: str):
#     try:
#         g = manager.get(game_id)
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Game not found")
#     s = g.status()
#     return {"game_id": game_id, "scores": s["scores"], "round_no": s["round_no"], "active": s["active"]}

# @app.get("/games/{game_id}/summary")
# def get_summary(game_id: str):
#     try:
#         g = manager.get(game_id)
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Game not found")
#     return g.summary()

# @app.post("/games/{game_id}/abandon")
# def abandon_game(game_id: str):
#     try:
#         g = manager.abandon(game_id)
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Game not found")
#     return {"game_id": game_id, "active": g.active}
