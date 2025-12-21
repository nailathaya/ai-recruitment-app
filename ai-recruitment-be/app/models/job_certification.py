from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class JobCertification(Base):
    __tablename__ = "job_certifications"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("job_postings.id"))
    certification_name = Column(String(150), nullable=False)

    job = relationship("JobPosting", back_populates="certifications")

