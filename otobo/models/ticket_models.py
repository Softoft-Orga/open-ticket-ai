from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ArticleDetail:
    Body: Optional[str] = ""
    Subject: Optional[str] = ""


@dataclass
class TicketBase:
    TicketID: Optional[int] = None
    Title: Optional[str] = None
    QueueID: Optional[int] = None
    Queue: Optional[str] = None
    PriorityID: Optional[int] = None
    Priority: Optional[str] = None
    Article: Optional[List[ArticleDetail]] = field(default_factory=list)
