from datetime import datetime

from pydantic import BaseModel, validator


class CreateLogRequest(BaseModel):
    app_id: str
    time: str
    auth_token: str
    text: str = "clubpravinvest: купил Т по 100 RUB (11.11.2011)"

    @validator("time")
    def validate_time_format(cls, value):
        try:
            datetime.strptime(value, "%d:%m:%Y.%H:%M:%S")
            return value
        except ValueError:
            raise ValueError("Invalid time format. Use DD:MM:YYYY.hh:mm:ss")


class APIResponse(BaseModel):
    status: str
