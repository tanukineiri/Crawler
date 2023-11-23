from dataclasses import dataclass


@dataclass
class CompanyDetails():
    name: str
    phone: str
    websiteUrl: str
    postalAddress: str
    emails = set()
    error: str

    def __init__(self):
        self.name = None
        self.phone = None
        self.websiteUrl = None
        self.postalAddress = None
        self.error = None
