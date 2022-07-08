#!/usr/bin/env python3

from operator import is_
import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup



payload_xss = open("xss_payload.txt").read().strip().split('\n')
payload_sql = open("sql_payload.txt").read().strip().split('\n')
total_payload=len(payload_xss)
report_file=open("output.txt","w")


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links
        
    def extract_links_from(self, url):
        response = self.session.get(url)
        html = response.text
        return re.findall(r'(?:href=")(.*?)"', html)

    


    def check(self,html):
        sql_errors = {
            "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*", r"SQL syntax.*MariaDB server"),
            "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"Warning.*PostgreSQL"),
            "Microsoft SQL Server": (r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*odbc_.*", r"Warning.*mssql_", r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string", r"Microsoft OLE DB Provider for ODBC Drivers"),
            "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine", r".*Syntax error.*query expression"),
            "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Warning.*oci_.*", "Microsoft OLE DB Provider for Oracle"),
            "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error"),
            "SQLite": (r"SQLite/JDBCDriver", r"System.Data.SQLite.SQLiteException"),
            "Informix": (r"Warning.*ibase_.*", r"com.informix.jdbc"),
            "Sybase": (r"Warning.*sybase.*", r"Sybase message")
        }
        """check SQL error is in HTML or not"""
        for db, errors in sql_errors.items():
            for error in errors:
                if re.compile(error).search(html):
                    #print "\n" + db
                    return True
        return False

    def crawl(self, url):
        href_links = self.extract_links_from(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print(link)
                report_file.write(link)
                self.crawl(link)

    def extract_froms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.text)
        return parsed_html.findAll("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        method = form.get("method")
        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value
            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_froms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                for payload in payload_xss:
                    is_vulnerable_to_xss = self.test_xss_in_form(form, link,payload)
                    if is_vulnerable_to_xss:
                        print("\n\n [+++] XSS discovered in " + link + " in the following form")
                        report_file.write("\n\n [+++] XSS discovered in " + link + " in the following form")
                        print(form.prettify())
                        report_file.write(form.prettify())
                        print("\n Payload : "+payload)
                        report_file.write("\n Payload : "+payload)
                        break

            if "=" in link:
                print("[+] Testing " + link)
                for payload in payload_xss:
                    is_vulnerable_to_xss = self.test_xss_in_link(link,payload)
                    if is_vulnerable_to_xss:
                        print("[***] Discovered XSS in " + link)
                        report_file.write("[***] Discovered XSS in " + link)
                        print("\n Payload : "+payload)
                        report_file.write("\n Payload : "+payload)
                        break
    
    def run_sql_scanner(self):
        for link in self.target_links:
            forms = self.extract_froms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                for payload in payload_sql:
                    is_vulnerable_to_sql = self.test_sql_in_form(form, link,payload)
                    if is_vulnerable_to_sql:
                        print("\n\n [+++] SQL discovered in " + link + " in the following form")
                        report_file.write("\n\n [+++] SQL discovered in " + link + " in the following form")
                        print(form.prettify())
                        report_file.write(form.prettify())
                        print("\n Payload : "+payload)
                        report_file.write("\n Payload : "+payload)
                        break

            if "=" in link:
                print("[+] Testing " + link)
                for payload in payload_sql:
                    is_vulnerable_to_sql = self.test_sql_in_link(link,payload)
                    if is_vulnerable_to_sql:
                        print("[***] Discovered SQL in " + link)
                        report_file.write("[***] Discovered SQL in " + link)
                        print("\n Payload : "+payload)
                        report_file.write("\n Payload : "+payload)
                        break

    def test_sql_in_form(self,form,url,payload):
        sql_payload=payload
        response = self.submit_form(form, sql_payload,url)
        if self.check(response.text):
            return True
    
    def test_sql_in_link(self, url,payload):
        sql_payload = payload
        url = url.replace("=", "=" + sql_payload)
        response = self.session.get(url)
        if self.check(response.text):
            return True

    def test_xss_in_link(self, url,payload):
        xss_test_script = payload
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.text

    def test_xss_in_form(self, form, url,payload):
        xss_test_script = payload
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.text

    