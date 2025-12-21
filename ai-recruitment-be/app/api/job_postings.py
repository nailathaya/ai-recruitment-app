from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.job_posting import JobPosting
from app.schemas.request import JobPostingCreateRequest
from app.schemas.response import JobPostingResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.models.job_skill import JobSkill
from app.models.job_certification import JobCertification

router = APIRouter(
    prefix="/job-postings",
    tags=["Job Postings"]
)

# =========================
# CREATE JOB (HRD)
# =========================
from app.models.job_skill import JobSkill
from app.models.job_certification import JobCertification

@router.post("/", response_model=JobPostingResponse)
def create_job(
    payload: JobPostingCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "hrd":
        raise HTTPException(status_code=403)

    payload_data = payload.dict(exclude={"skills", "certifications"})

    job = JobPosting(
        hrd_id=current_user.id,
        **payload_data,
        status="published"
    )

    for skill in payload.skills:
        job.skills.append(JobSkill(skill_name=skill))

    for cert in payload.certifications:
        job.certifications.append(JobCertification(certification_name=cert))

    db.add(job)
    db.commit()
    db.refresh(job)
    return job

# =========================
# LIST ALL JOBS (HRD)
# =========================
@router.get("/", response_model=List[JobPostingResponse])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "hrd":
        raise HTTPException(status_code=403, detail="Only HRD")

    return db.query(JobPosting).filter(
        JobPosting.hrd_id == current_user.id
    ).all()

@router.get("/public", response_model=List[JobPostingResponse])
def get_public_jobs(db: Session = Depends(get_db)):
    jobs = (
        db.query(JobPosting)
        .filter(JobPosting.status == "published")
        .order_by(JobPosting.created_at.desc())
        .all()
    )
    return jobs


