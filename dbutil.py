import constants
import sqlite3

from models.company_details import CompanyDetails

class DbUtil:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect(constants.db_name)
        self.cursor = self.connection.cursor()
        self.init_db()

    def init_db(self):
        if self.cursor is not None:
            self.cursor.execute(f'''
             CREATE TABLE IF NOT EXISTS {constants.db_table_name} (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             phone TEXT NOT NULL,
             site TEXT NOT NULL,
             emails TEXT NOT NULL,
             errors TEXT
             )
             ''')
        self.connection.commit()

    def close_db(self):
        if self.connection is not None:
            self.connection.close()

    def saveItem(self, name, phone, site, emails, errors):
        if (self.cursor is not None) and (self.connection is not None):
            self.cursor.execute(f'INSERT INTO {constants.db_table_name} (name, phone, site, emails, errors)', (name, phone, site, emails, errors))
            self.connection.commit()

    def save_company_details(self, company: CompanyDetails):
        if (self.cursor is not None) and (self.connection is not None):
            if self.checkIfCompanyNotExist(company):
                print(f"DbUtil: current company is {company}")
                emailString = ""
                if len(company.emails) > 0:
                    emailString = ';'.join(list(map(str, company.emails)))
                self.cursor.execute(f'INSERT INTO {constants.db_table_name} (name, phone, site, emails, errors) VALUES (?, ?, ?, ?, ?)',
                               (company.name, company.phone, company.websiteUrl, emailString, company.error))
                self.connection.commit()
            else:
                print(f"DbUtil: Company {company.name} already exist in database")

    def checkIfCompanyNotExist(self, company: CompanyDetails):
        if (self.cursor is not None) and (self.connection is not None):
            self.cursor.execute(f'SELECT * FROM {constants.db_table_name} WHERE name = ?', (company.name,))
            existing = self.cursor.fetchall()
            return len(existing) == 0
        else:
            return False