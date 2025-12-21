from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("job_postings.id"))
    skill_name = Column(String(100), nullable=False)

    job = relationship("JobPosting", back_populates="skills")
