from typing import Optional

class Question():
    def __init__(self):
        self.Id: Optional[int] = None
        self.Description: Optional[str] = None
        self.IsOneAnswer: Optional[bool] = None
        self.IdSurvey: Optional[int] = None
