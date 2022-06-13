#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pickle, time, sys
import requests
from lxml import html
import time

rent_price = {
	'83': '中古 8800+2.8/KM', 
	'84': '中古 10800+3.36/KM', 
	'85': '中古 12800+4.0/KM', 
	'86': '中古 14800+4.64/KM', 
	'87': '中古 16800+4.64/KM', 
	'173': '中古 20800+5.2/KM', 
	'177': '中古 38800+6.8/KM',
	'178': '中古 46800+8/KM',
	'172': '全新 8800+2.8/KM',
	'152': '全新 10800+3.36/KM',
	'153': '全新 12800+4.0/KM',
	'154': '全新 14800+4.64/KM',
	'155': '全新 16800+4.64/KM',
	'163': '全新 16800+4.64/KM',
	'156': '全新 18800+4.8/KM',
	'164': '618 優惠  8800+2.8/KM',
	'165': '618 優惠  10800+3.36/KM',
	'166': '618 優惠  12800+4/KM',
	'167': '618 優惠  14800+4.64/KM',
	'168': '618 優惠  16800+4.64/KM',
	'169': '618 優惠  20800+5.2/KM',
	'170': '618 優惠  34800+6/KM',
	'171': '618 優惠  42800+6.8/KM'
} 

def get_cookie(id, pwd):
	print("開啟 Selenium...")
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	s=Service("./chromedriver")
	web = webdriver.Chrome(service=s, options = chrome_options)
	web.get("https://sealand.tw/user/login")

	print("載入中...")
	email = web.find_element(By.ID, "email")
	password = web.find_element(By.ID, "password")

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
