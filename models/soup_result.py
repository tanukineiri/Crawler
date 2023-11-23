from dataclasses import dataclass
from bs4 import BeautifulSoup

@dataclass
class SoupResult:
    soup: BeautifulSoup
    error: str
