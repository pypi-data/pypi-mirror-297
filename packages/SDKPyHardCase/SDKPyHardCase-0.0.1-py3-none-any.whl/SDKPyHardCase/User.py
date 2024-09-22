from typing import Optional
from Access import Access

class User():
    def __init__(self):
        self.Id: Optional[int] = None
        self.Login: Optional[str] = None
        self.Password: Optional[str] = None
        self.Email: Optional[str] = None
        self.Access: Access

