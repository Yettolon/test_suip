from pydantic import BaseModel


class SuipDataRead(BaseModel):
    id: int
    filename: str
    size: str
    modified_at: str
    accessed_at: str
    file_type: str
    mime_type: str

    class Config:
        from_attributes = True
        orm_mode = True
