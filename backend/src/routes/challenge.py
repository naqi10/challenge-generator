# from fastapi import APIRouter, Depends, HTTPException, Request
# from pydantic import BaseModel
# from sqlalchemy.orm import Session

# from ..ai_generator import generate_challenge_with_ai
# from ..database.db import (
#     get_challenge_quota,
#     create_challenge,
#     create_challenge_quota,
#     reset_quota_if_needed,
#     get_user_challenges
# )
# from ..utils import authenticate_and_get_user_details
# from ..database.models import get_db
# import json
# from datetime import datetime

# router = APIRouter()


# class ChallengeRequest(BaseModel):
#     difficulty: str

#     class Config:
#         json_schema_extra = {"example": {"difficulty": "easy"}}


# @router.post("/generate-challenge")
# async def generate_challenge(request: ChallengeRequest, request_obj: Request, db: Session = Depends(get_db)):
#     try:
#         user_details = authenticate_and_get_user_details(request_obj)
#         user_id = user_details.get("user_id")

#         quota = get_challenge_quota(db, user_id)
#         if not quota:
#             quota = create_challenge_quota(db, user_id)

#         quota = reset_quota_if_needed(db, quota)

#         if quota.quota_remaining <= 0:
#             raise HTTPException(status_code=429, detail="Quota exhausted")

#         challenge_data = generate_challenge_with_ai(request.difficulty)

#         new_challenge = create_challenge(
#             db=db,
#             difficulty=request.difficulty,
#             created_by=user_id,
#             title=challenge_data["title"],
#             options=json.dumps(challenge_data["options"]),
#             correct_answer_id=challenge_data["correct_answer_id"],
#             explanation=challenge_data["explanation"]
#         )

#         quota.quota_remaining -= 1
#         db.commit()

#         return {
#             "id": new_challenge.id,
#             "difficulty": request.difficulty,
#             "title": new_challenge.title,
#             "options": json.loads(new_challenge.options),
#             "correct_answer_id": new_challenge.correct_answer_id,
#             "explanation": new_challenge.explanation,
#             "timestamp": new_challenge.date_created.isoformat()
#         }

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.get("/my-history")
# async def my_history(request: Request, db: Session = Depends(get_db)):
#     user_details = authenticate_and_get_user_details(request)
#     user_id = user_details.get("user_id")

#     challenges = get_user_challenges(db, user_id)
#     return {"challenges": challenges}


# @router.get("/quota")
# async def get_quota(request: Request, db: Session = Depends(get_db)):
#     user_details = authenticate_and_get_user_details(request)
#     user_id = user_details.get("user_id")

#     quota = get_challenge_quota(db, user_id)
#     if not quota:
#         return {
#             "user_id": user_id,
#             "quota_remaining": 0,
#             "last_reset_date": datetime.now()
#         }

#     quota = reset_quota_if_needed(db, quota)
#     return quota
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..ai_generator import generate_challenge_with_ai
from ..database.db import (
    get_challenge_quota,
    create_challenge,
    create_challenge_quota,
    reset_quota_if_needed,
    get_user_challenges
)
from ..utils import authenticate_and_get_user_details
from ..database.models import get_db
import json
from datetime import datetime
import traceback

router = APIRouter()


class ChallengeRequest(BaseModel):
    difficulty: str

    class Config:
        json_schema_extra = {"example": {"difficulty": "easy"}}


@router.post("/generate-challenge")
async def generate_challenge(request: ChallengeRequest, request_obj: Request, db: Session = Depends(get_db)):
    try:
        user_details = authenticate_and_get_user_details(request_obj)
        user_id = user_details.get("user_id")

        # ✅ Quota logic
        quota = get_challenge_quota(db, user_id)
        if not quota:
            quota = create_challenge_quota(db, user_id)

        quota = reset_quota_if_needed(db, quota)

        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota exhausted")

        # ✅ Generate challenge
        challenge_data = generate_challenge_with_ai(request.difficulty)
        print("🚀 Generated challenge data:", challenge_data)

        title = challenge_data.get("title", "Untitled Challenge")
        options = challenge_data.get("options", [])
        correct_answer_id = int(challenge_data.get("correct_answer_id", 0))
        explanation = challenge_data.get("explanation", "No explanation provided.")

        if not isinstance(options, list) or len(options) != 4:
            raise ValueError("Invalid options array returned from AI")

        # ✅ Save to DB
        new_challenge = create_challenge(
            db=db,
            difficulty=request.difficulty,
            created_by=user_id,
            title=title,
            options=json.dumps(options),
            correct_answer_id=correct_answer_id,
            explanation=explanation
        )

        # ✅ Update quota
        quota.quota_remaining -= 1
        db.commit()

        print("✅ Challenge saved to DB:", new_challenge.title)

        return {
            "id": new_challenge.id,
            "difficulty": request.difficulty,
            "title": title,
            "options": options,
            "correct_answer_id": correct_answer_id,
            "explanation": explanation,
            "timestamp": new_challenge.date_created.isoformat()
        }

    except Exception as e:
        print("❌ Error in /generate-challenge route:")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    try:
        user_details = authenticate_and_get_user_details(request)
        user_id = user_details.get("user_id")
        challenges = get_user_challenges(db, user_id)
        return {"challenges": challenges}
    except Exception as e:
        print("❌ Error in /my-history:", e)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    try:
        user_details = authenticate_and_get_user_details(request)
        user_id = user_details.get("user_id")

        quota = get_challenge_quota(db, user_id)
        if not quota:
            return {
                "user_id": user_id,
                "quota_remaining": 0,
                "last_reset_date": datetime.now()
            }

        quota = reset_quota_if_needed(db, quota)
        return quota
    except Exception as e:
        print("❌ Error in /quota:", e)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
