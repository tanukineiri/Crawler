from dataclasses import dataclass


@dataclass
class EmailResult:
    emails = set()
    error: str = None