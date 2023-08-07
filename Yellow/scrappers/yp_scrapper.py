import concurrent
import random
import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from clint.textui import puts, colored

from config.qt_config import QTConfig
from database_layer import business_db
from models.Business import Business
from scrapper_helper import scrapper_helper


URL_BASE = "https://www.yellowpages.ca/search/si"
#URL_BASE = "https://www.yellowpages.com/search/si"

def start():
	config = QTConfig.get_config()
	found = 0

	if config.items is None or len(config.items) == 0:
		raise RuntimeError("No items selected. Try running \"init\" first or adding them in config.yml")

	if config.locations is None or len(config.locations) == 0:
		raise RuntimeError("No locations selected. Try running \"init\" first or adding them in config.yml")


	all_businesses = []
	for location in config.locations:
		for item in config.items:
			puts(colored.green(f"Scrapping YellowPages for {item} in {location}"))
			results = scrap(item, location)
			all_businesses.append(results)
			#business_db.insert_all(results)
			puts(colored.green(f"Found {len(results)} results on YellowPages for {item} in {location}"))
			found += len(results)

	#print(results)
	seen = set()
	all_unique_businesses = []
	#print(all_businesses[0][0].address)
	for list_obj in all_businesses:
		for single_object in list_obj:
			if single_object.address not in seen:
				all_unique_businesses.append(single_object)
				seen.add(single_object.address)
	
	business_db.insert_all(all_unique_businesses)
	
	return found


def scrap(item, location):
	businesses = []

	# Get first page
	url = f"{URL_BASE!s}/1/{__querify_string(item)!s}/{__querify_string(location)}"
	response = requests.get(url, headers=scrapper_helper.get_random_user_agent_header())
	html_response = BeautifulSoup(response.text, 'html.parser')
	businesses_html = html_response.find_all("div", class_="listing")
	#print("businesses html : ", businesses_html)

	for business in businesses_html:
		businesses.append(parse(business))

	try:
		total_pages = int(html_response.find("span", class_="pageCount").get_text().replace("\n", "").split("/")[1])
	except Exception as ex:
		puts(colored.red(f"Failed to find multiple pages for {item} in {location}. Log created"))
		scrapper_helper.write_log(f"Failed to find multiple pages for {item} in {location}.\nError: {ex}\nHTML:{html_response}")
		return businesses

	"""
	for page in range(2, total_pages):
		data = 	__scrap_with_page_number_threaded(item, location, page)
		#print(data)
		businesses.extend(data)
		
	#print("Total pages: ", total_pages)
	"""
	# Bug with yellow pages
	if total_pages > 60:
		total_pages = 60

	# Get 2+ pages
	if total_pages == 1:
		return businesses
	else:

		with ThreadPoolExecutor(max_workers=4) as executor:
			futures = {}
			for i in range(2, total_pages + 1):
				future = executor.submit(__scrap_with_page_number_threaded, item, location, i)
				futures[future] = i
				time.sleep(random.random() * 2 + 2)

			for future in concurrent.futures.as_completed(futures):
				page = futures[future]
				try:
					data = future.result()
					businesses.extend(data)
				except Exception as exc:
					print(f"Generated an exception at page {page} with message: {exc!s}")

		#return businesses
	
	seen = set()
	unique = []
	for obj in businesses:
		if obj.address not in seen:
			unique.append(obj)
			#all_businesses.append(obj)
			seen.add(obj.address)
	
	return unique

def __scrap_with_page_number_threaded(item, location, page):
    businesses = []

    url = f"{URL_BASE!s}/{page}/{__querify_string(item)!s}/{__querify_string(location)}"

    response = requests.get(url, headers=scrapper_helper.get_random_user_agent_header())
    html_response = BeautifulSoup(response.text, 'html.parser')
    businesses_html = html_response.find_all("div", class_="listing")

    if len(businesses_html) > 0:
        for business in businesses_html:
            try:
                businesses.append(parse(business))
            except Exception as ex:
                puts(colored.red(f"Crashed when trying to parse: {business}"))

    return businesses


def parse(html):
    name = None
    phone_number = None
    address = None
    province = None
    
    name_html = html.find("a", class_="listing__name--link")
    if name_html is not None:
        name = name_html.get_text().replace("\n", "")

    address_html = html.find("span", class_="listing__address--full")
    if address_html is not None:
        stripped_address = address_html.get_text().replace("\n", "")
        address = f"\"{stripped_address}\""

    province_html = html.find("span", itemprop="addressRegion")
    if province_html is not None:
        province = province_html.get_text().replace("\n", "")

    phone_number_html = html.find("a", title="Get the Phone Number")
    if phone_number_html is not None:
        phone_number = phone_number_html["data-phone"]

    return Business(name=name, phone=phone_number, address=address, province=province)


def __querify_string(s):
    return s.replace(" ", "+")
