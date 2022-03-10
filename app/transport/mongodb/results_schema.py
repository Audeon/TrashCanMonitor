from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, StrictBool
from pydantic.typing import Optional


class ResultsSchema(BaseModel):
    """
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    container_id: str
    gateway_check: StrictBool
    radio_raw_data: Optional[dict] = None
    interface_data_raw: Optional[dict] = None
    lan_status_raw: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True
        title = "transcan_results"
        extra = "allow"
        json_encoders = {
            ObjectId: str
        }