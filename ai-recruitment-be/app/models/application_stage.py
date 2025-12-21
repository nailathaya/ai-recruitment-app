from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ApplicationStage(Base):
    __tablename__ = "application_stages"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id"),
        nullable=False,
    )

    name = Column(
        Enum(
            "Screening",
            "Psikotest",
            "Interview HR",
            "Interview User",
            "Penawaran",
            name="stage_name_enum",
        ),
        nullable=False,
    )

    status = Column(
        Enum(
            "Belum",
            "Pending",
            "Dalam Proses",
            "Lolos",
            "Tidak Lolos",
            name="stage_status_enum",
        ),
        default="Belum",
    )

    application = relationship("Application", back_populates="stages")
