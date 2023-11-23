from dataclasses import dataclass


@dataclass
class WebsiteUrlResult:
    websiteUrl: str
    error: str