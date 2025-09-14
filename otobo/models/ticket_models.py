from dataclasses import dataclass
from typing import Optional, List, Union


@dataclass
class ArticleDetail:
    Body: Optional[str] = ""
    Subject: Optional[str] = ""


@dataclass
class TicketBase:
    TicketID: Optional[int] = None
    Title: Optional[str] = ""
    QueueID: Optional[int] = None
    Queue: Optional[str] = ""
    PriorityID: Optional[int] = None
    Priority: Optional[str] = ""
    Article: Optional[Union[ArticleDetail, List[ArticleDetail]]] = None
