from pydantic import BaseModel

class ReportRequest(BaseModel):
    reason: str = "general"
