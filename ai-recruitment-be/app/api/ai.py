from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.application import Application
from app.schemas.request import AIMatchRequest
from app.schemas.response import AIMatchResponse

router = APIRouter(prefix="/ai", tags=["AI Matching"])


@router.post(
    "/match",
    response_model=List[AIMatchResponse]
)
def ai_match(
    payload: AIMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 🔐 HRD only
    if current_user.role != "hrd":
        raise HTTPException(status_code=403, detail="Forbidden")

    # ✅ Ambil kandidat yang APPLY ke job ini
    applications = (
        db.query(Application)
        .filter(Application.job_id == payload.job_id)
        .all()
    )

    results = []

    for app in applications:
        user = app.user

        results.append({
            "candidate": {
                "id": user.id,
                "user": {
                    "id": user.id,
                    "name": user.full_name,
                    "email": user.email,
                    "avatarUrl": user.avatar_url,
                }
            },
            # 🔧 DUMMY SCORE (NANTI DIGANTI AI)
            "fitScore": 75,
            "summary": "Kandidat memenuhi kriteria dasar untuk posisi ini.",
            "matchingAspects": [
                "Pengalaman relevan",
                "Skill sesuai kebutuhan"
            ],
            "aiReasons": [
                "Data kandidat akan dianalisis oleh AI",
                "Scoring berbasis LLM belum diaktifkan"
            ]
        })

    return results
