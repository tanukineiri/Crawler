import time
from bs4 import Tag
import main
import constants
from urllib.parse import urlparse
import re

from models.email_result import EmailResult


def isValid(email):
    if re.fullmatch(constants.regexValidation, email):
        print(f"{email} Valid email")
        return True
    else:
        print(f"{email} Invalid email")
        return False

def getTextSearchResults(soup):
    txt = soup.get_text(separator=" ").strip()
    resultSet = set()
    textSearchResults = re.findall(constants.regexEmail, str(txt))
    for textResult in textSearchResults:
        if isValid(textResult):
            resultSet.update([str(textResult).lower()])
    return resultSet

def processingEmail(siteUrl):
    startTime = time.time()
    emailResult = EmailResult()
    primer_hostname = urlparse(siteUrl).netloc
    primer_scheme = urlparse(siteUrl).scheme
    results = set()
    possibleContactUrls = set()
    print(f"Processing email for: {siteUrl}")
    soupResult = main.fetchSiteSoup(siteUrl)
    if soupResult.soup is None:
        if soupResult.error is not None:
            # results.add(soupResult.error)
            emailResult.error = soupResult.error
        return emailResult
    soup = soupResult.soup
    linkContainers = soup.find_all("a")

    for link in linkContainers:
        tag: Tag = link
        if "href" in link.attrs.keys():
            linkUrl = link["href"]
            if linkUrl != None and "mailto" in linkUrl:
                emailAddress = linkUrl.replace("mailto:", "")
                if isValid(emailAddress):
                    results.add(emailAddress.lower())

            hostname = urlparse(linkUrl).netloc
            if hostname == primer_hostname or len(hostname) == 0:
                contactText = link.text.lower()
                for keyword in constants.possibleContactKeywords:
                    if keyword in contactText:
                        if len(hostname) == 0:
                            possibleContactUrl = primer_scheme + "://" + primer_hostname.rstrip("/") + "/" + link["href"].lstrip("/")
                            possibleContactUrls.add(possibleContactUrl)
                            print(f"Syntesized mail url: ${possibleContactUrl}")
                        else:
                            possibleContactUrls.add(link["href"])

    results.update(set(getTextSearchResults(soup)))

# # email в виде plain text'
#     for block in soup.find_all():
#         blockString = block.text
#         if len(blockString) > 0:
#             possibleEmails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', blockString)
#             if len(possibleEmails) > 0:
#                 for possibleEmail in possibleEmails:
#                     if isValid(possibleEmail):
#                         results.add(possibleEmail)
#
    if len(results) == 0 and len(possibleContactUrls) != 0:
        for possibleContactUrl in possibleContactUrls:
            print(f"Processing email for inner page: {possibleContactUrl}")
            soup = main.fetchSiteSoup(possibleContactUrl).soup
            if soup is None:
                if soupResult.error is not None:
                    results.add(soupResult.error)
                return results
            linkContainers = soup.find_all("a")
            for link in linkContainers:
                if "href" in link.attrs.keys():
                    linkUrl = link["href"]
                    if linkUrl != None and "mailto" in linkUrl:
                        emailAddress = linkUrl.replace("mailto:", "")
                        if isValid(emailAddress):
                            results.add(emailAddress.lower())
            results.update(set(getTextSearchResults(soup)))

    print(results)
    print("--- %s seconds ---" % (time.time() - startTime))
    emailResult.emails = results
    return emailResult
