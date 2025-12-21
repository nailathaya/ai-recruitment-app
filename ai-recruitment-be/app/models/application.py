from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    # 🔑 FOREIGN KEYS (INI WAJIB ADA)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)

    status = Column(
        Enum(
            "Pending",
            "Dalam Proses",
            "Interview",
            "Diterima",
            "Ditolak",
            name="application_status_enum",
        ),
        default="Pending",
    )

    applied_at = Column(DateTime, default=datetime.utcnow)

    # ✅ RELATIONSHIPS
    user = relationship("User", back_populates="applications")
    job = relationship("JobPosting", back_populates="applications")
    stages = relationship(
        "ApplicationStage",
        back_populates="application",
        cascade="all, delete-orphan",
    )
