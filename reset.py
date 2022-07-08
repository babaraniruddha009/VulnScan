from operator import is_
import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup



    
def reset_data(self):
    url = "http://192.168.194.212/dvwa/setup.php"
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text)
    forms = parsed_html.findAll("form")
    action = forms.get("action")
    post_url = urlparse.urljoin(url, action)
    method = forms.get("method")
    if method == "post":
        requests.post(post_url)
