import socket

import certifi
import time
import requests
import json
import urllib3
import urllib
import ssl
from bs4 import BeautifulSoup
from urllib3.exceptions import NameResolutionError, MaxRetryError, HTTPError
from urllib import parse
from urllib import request
from urllib import error
from dataclasses import dataclass, astuple
import processingEmail
import constants
import dbutil
from models.company_details import CompanyDetails
from models.soup_result import SoupResult
from models.website_url_result import WebsiteUrlResult
from net_error import Net_Error
from dbutil import DbUtil
import test_block


currentPageNumber = 0
currentItemNumber = 0
db: DbUtil

def fetchSiteSoupByRequests(siteUrl):
    try:
        html = requests.get(siteUrl, verify=False)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.MissingSchema,
            requests.exceptions.ReadTimeout,
            NameResolutionError,
            MaxRetryError) as error:
        print(f"Error {error} when requesting {siteUrl}")
        return SoupResult(None, error)
    htmlText = html.text
    soup = BeautifulSoup(htmlText, 'html.parser')
    return SoupResult(soup, None)

def openSiteWithFailedVerify(req: urllib.request.Request):
    print(f"Tryin' to open {req.full_url} without sertificate check")
    result = ssl.get_default_verify_paths()
    cafile = certifi.where()
    print(f'{result=}')
    print(f'{cafile=}')
    context = ssl.create_default_context(cafile=certifi.where())

    # Bypass the certificate verification.
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        html = urllib.request.urlopen(req, context=context).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        return SoupResult(soup, None)
    except urllib.error.URLError as e:
        err_str = "Unknown error"
        if hasattr(e, 'reason'):
            print(e.reason)
            err_str = str(e.reason)
            print(f"{err_str} Error when requesting {req.full_url}")
        return SoupResult(None, f"{err_str} Error when requesting {req.full_url}")


def fetchSiteSoup(siteUrl):
    print(f"Fetching Soup for Url: {siteUrl}")
    url_parced = urllib.parse.urlparse(siteUrl)
    url = url_parced.scheme + "://" + url_parced.netloc + urllib.parse.quote(url_parced.path)
    req = urllib.request.Request(url, unverifiable=False)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
    req.add_header('Accept',
                   'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    try:
        opened = urllib.request.urlopen(req, timeout=40).read()
        try:
            html = opened.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return SoupResult(soup, None)
        except UnicodeDecodeError as e:
            print(f"{e.reason} Error when decoding {siteUrl}")
            try:
                html = opened.decode('latin-1')
                soup = BeautifulSoup(html, 'html.parser')
                return SoupResult(soup, None)
            except UnicodeDecodeError as e:
                print(f"{e.reason} Second Error when decoding {siteUrl}")
                return SoupResult(None, e.reason)
    except urllib.error.HTTPError as e:
        if e.code >= 400:
            print(f"{e.code} Error when requesting {siteUrl}")
            return SoupResult(None, f"{siteUrl} returns {e.code} error")
    except urllib.error.URLError as e:
        err_str = "Unknown error"
        if hasattr(e, 'reason'):
            print(e.reason)
            err_str = str(e.reason)
            print(f"{err_str} Error when requesting {siteUrl}")
        if (Net_Error.COMMON_URLOPEN_ERROR.value in str(err_str).lower() or
                Net_Error.UNRECOGNIZED_NAME.value in str(err_str).lower() or
                Net_Error.OPERATION_TIMED_OUT.value in str(err_str).lower() or
                Net_Error.INTERNAL_ERROR.value in str(err_str).lower()):
            return SoupResult(None, f"Error: {err_str}")
        return openSiteWithFailedVerify(req)
        # fetchSiteSoupByRequests(siteUrl)
    except ssl.SSLCertVerificationError:
        return openSiteWithFailedVerify(req)
    except socket.timeout as e:
        err_str = f"Timeout error when requesting {siteUrl}"
        print(err_str)
        return SoupResult(None, err_str)

def saveResult(company: CompanyDetails):
    if company.error is None:
        outputString = f"\n{company.name},{company.phone},{company.websiteUrl},"
        if len(company.emails) > 0:
            emailString = ';'.join(list(map(str, company.emails)))
            outputString = outputString + emailString
    else:
        outputString = f"\n{company.name},{company.phone},,{company.error},"
    db.save_company_details(company)
    with open(constants.output_file_name, 'a') as file:
        file.write(outputString)

def processPage(pageUrl):
    soupResult = fetchSiteSoup(pageUrl)
    if soupResult.soup is None:
        return
    directory = soupResult.soup.find("ul", class_="hz-pro-search-results mb0")

    if directory is None:
        print("Root element is empty")
        return

    result_items = directory.find_all("li", class_="hz-pro-search-results__item")

    # nextPageLinkContainer = soup.find("a", class_="hz-pagination-link hz-pagination-link--next")
    for item in result_items:
        company = CompanyDetails()
        itemJson = item.find(type="application/ld+json")
        itemHyperlink = item.find("a")
        websiteUrlResult = processingInternalLink(itemHyperlink["href"])
        itemList = json.loads(itemJson.text)
        company.name = itemList["name"]
        company.phone = itemList["telephone"]
        itemAddressList = itemList["address"]
        company.postalAddress = itemAddressList["streetAddress"]
        print(company.name)
        if websiteUrlResult.error is None:
            company.websiteUrl = websiteUrlResult.websiteUrl
            emailResult = processingEmail.processingEmail(company.websiteUrl)
            if len(emailResult.emails) > 0:
                company.emails = emailResult.emails
            elif emailResult.error is not None:
                company.error = emailResult.error
        else:
            company.websiteUrl = ""
            company.error = websiteUrlResult.error
        saveResult(company)


def processingInternalLink(internal_url):
    soupResult = fetchSiteSoup(internal_url)
    if soupResult.soup is None:
        if soupResult.error != None:
            return WebsiteUrlResult(None, soupResult.error)
        return
    websiteInfo = soupResult.soup.find("div", class_="sc-183mtny-0 sc-1uw6j8i-0 BusinessDetails__StyledCell-sc-1iscszt-0 dYJOPh ecpWHO gRCcss hz-track-me hui-cell")
    if websiteInfo is None:
        return WebsiteUrlResult(None, "Error: No Site")
    websiteLink = websiteInfo.find("a")
    websiteNameContainer = websiteLink.find("span", class_="sc-mwxddt-0 Website__EllipsisText-sc-19fzbgj-0 ctdszu dRuQKg")
    websiteUrl = "https://" + websiteNameContainer.text
    return WebsiteUrlResult(websiteUrl, None)

def appExit():
    db.close_db()
    exit()

def start():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    global currentItemNumber
    global currentPageNumber

    with open (constants.output_file_name, 'w') as file:
        file.write(constants.headerString)

    while currentItemNumber < 44: #itemNumber:
        currentItemNumber = currentPageNumber * 15
        page_url = constants.primer_url + f"/p/{currentItemNumber}"
        print(page_url)
        processPage(page_url)
        currentPageNumber += 1

if __name__ == '__main__':
    startTime = time.time()
    # test_block.test_block()
    # test_block.test_block2()

    db = DbUtil()
    start()
    print("--- %s seconds ---" % (time.time() - startTime))
    appExit()

    # TODO add DB support
    # TODO filter results