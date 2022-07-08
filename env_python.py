#!/usr/bin/env python

from urllib import response
import requests
from bs4 import BeautifulSoup
from urllib import urlparse


def request(url):
    try:
        return requests.get(url)
    except requests.exception.ConeectionError:
        pass

# this the where u should put the target url


target_url = ""
reponse = request(target_url)
# ### check the response of the website
###
#
parsed_html = BeautifulSoup(response.content)
forms_list = parsed_html.findAll("form")
# This where the parsing take place and the payload will add ot it
for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    print(post_url)
    method = form.get("method")
    print(method)

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"
        post_data[input_name] = input_value
    result = request.post(post_url, data=post_data)
    print(result.content)

#        print(input_name)

# print(forms_list)
