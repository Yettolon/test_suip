from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SuipData(Base):
    __tablename__ = "suip_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String)
    size: Mapped[str] = mapped_column(String)
    modified_at: Mapped[str] = mapped_column(String)
    accessed_at: Mapped[str] = mapped_column(String)
    file_type: Mapped[str] = mapped_column(String, nullable=True)
    mime_type: Mapped[str] = mapped_column(String)
