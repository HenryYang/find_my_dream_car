#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle, time, sys
import requests
from lxml import html
import time

rent_price = {
	'118': '6800+2.24/KM', 
	'83': '8800+2.8/KM', 
	'84': '10800+3.36/KM', 
	'85': '12800+4.0/KM', 
	'86': '14800+4.64/KM', 
	'87': '16800+4.64/KM', 
	'88': '20800+5.2/KM', 
	'89': '26800+6/KM',
	'107': '30800+6.24/KM',
	'90': '34800+6.4/KM',
	'109': '38800+6.8/KM',
	'108': '46800+8.0/KM'
} 

def get_cookie(id, pwd):
	print("開啟 Selenium...")
	chrome_options = Options()
	chrome_options.add_argument('--headless') 
	web = webdriver.Chrome("./chromedriver", options = chrome_options)
	web.get("https://sealand.tw/user/login")

	print("載入中...")
	email = web.find_element_by_id("email")
	password = web.find_element_by_id("password")

	email.send_keys(id)
	password.send_keys(pwd)
	password.submit()
	print("登入中...")

	for g in web.get_cookies():
		if (g["name"]) == "sealand_session":
			cookie_value = (g["value"])
			break
		
	print("取得 Cookie...")
	web.quit()
	print(" ")
	return cookie_value


def get_vehicle(my_cookies, city):
	
	my_params = {'search_city_id': city}
	my_cookies = {'sealand_session': my_cookies}
	
	for i in rent_price:
		
		r = requests.get('https://sealand.tw/temp/'+ i , params = my_params, cookies = my_cookies)
		tree = html.fromstring(r.text)
		vehicle_type = tree.xpath('//td[@class="temp_top_td"]/text()')
		vehicle_info = tree.xpath('//td[@class="temp_content_td"]/text()')
		print('目前租金區間: ' + rent_price[i] + '，現有車數: ' + str(int(len(vehicle_type)/2)) + ' 台' )
		for i in range(int(len(vehicle_type)/2)):
			print("車款:" + vehicle_info[7*i] + " " +  vehicle_type[i].splitlines()[0] + " ,規格:" + vehicle_info[7*i+1] + " ,原始車價:" + vehicle_info[7*i+2] + " ,顏色:" + vehicle_info[7*i+3] + " ,年份:" + vehicle_info[7*i+5] + " ,公里數:" + vehicle_info[7*i+6])
		print("---------------------------------------------------")
		print(" ")
		
	print("現在時間：" + time.asctime(time.localtime(time.time())) )


if __name__ == '__main__':
	current_cookies = get_cookie('<帳號>', '<密碼>')
	get_vehicle(current_cookies, '<城市代號>')
