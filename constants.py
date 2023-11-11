import re

version = 0.5

db_name = "crawler2.db"
output_file_name = "outfile.csv"

regexEmail = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
regexValidation = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

possibleContactKeywords = ["контакт", "контакты", "связаться", "contact"]

headerString = "НАЗВАНИЕ,ТЕЛЕФОН,САЙТ,ПОЧТА,ПОЧТА"
primer_url = "https://www.houzz.ru/professionals/dizayn-interyera"
itemNumber = 40515
