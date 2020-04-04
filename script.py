import http.client
import datetime
import ssl
import os
from bs4 import BeautifulSoup
import csv

class GasPriceDataScraper:
	HOST_URL = 'www.eia.gov'
	PATH_URL = '/dnav/ng/hist/rngwhhdD.htm'
	CSV_DAILY_DIR = 'csvfiles/gas_daily_prices.csv'
	CSV_MONTHLY_DIR = 'csvfiles/gas_monthly_prices.csv'

	def __init__(self):
		self.date_and_price_data = []
		self.page_node = None
	
	def daily_prices(self):
		
		with open(self.CSV_DAILY_DIR, mode='w') as csv_file:
			writer = csv.writer(csv_file)
			# check if file already exist
			if os.path.exists(self.CSV_DAILY_DIR):
				print(self.CSV_DAILY_DIR, 'will be overwritten')
			# write the csv header
			writer.writerow(['date', 'price'])
			# write all the date and time data
			writer.writerows(self.date_and_price_data)
	
		print('Data saved in', self.CSV_DAILY_DIR)

	def monthly_prices(self):

		with open(self.CSV_MONTHLY_DIR, 'w') as csv_file:
			writer = csv.writer(csv_file)
			# check if file already exist
			if os.path.exists(self.CSV_DAILY_DIR):
				print(self.CSV_MONTHLY_DIR, 'will be overwritten')

			writer.writerow(['date', 'price'])
			price_data = self.date_and_price_data[::-1]
			prev_day_price = price_data[0]
			for daily_price in self.date_and_price_data[::-1]:
				if self.date_day(daily_price[0]) > self.date_day(prev_day_price[0]):
					writer.writerow(prev_day_price)
				prev_day_price = daily_price
		
		print('Data saved in', self.CSV_MONTHLY_DIR)

	def load_page_data(self):
		try:
			connection = http.client.HTTPSConnection(self.HOST_URL, context = ssl._create_unverified_context())
			connection.request("GET", self.PATH_URL)
			req = connection.getresponse()
			print(req.status, req.reason)
			if req.status == 200:
				page_node = BeautifulSoup(req.read(), 'html.parser')
				# target the data with the summary
				table_html_data = page_node.find(summary="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)")
				self.extract_and_format_data(table_html_data)
				print('HTML document fetched successfully')
			else:
				print('Could not fetch data from the ' + self.HOST_URL + 'please try again')
		except Exception as error:
			print('Something went wrong', error)

	def date_day(self, date):
		return int(date.split('-')[-1])

	def extract_and_format_data(self, page_node):
		date_and_price_data = []
		for each_tr in page_node.find_all('tr'):
			date_node = each_tr.find('td', {'class': 'B6'})
			if date_node:
				day_offset = 0
				# get the start date for the week
				start_date = date_node.string.replace('\xa0\xa0', '')[:11].replace('- ', ' ').replace(' ', '-')
				for price_node in each_tr.find_all('td', {'class': 'B3'}):
					price = price_node.text
					# check if there is a price for the day
					if price != '' and price != 'NA':
						# get only the startdate and use the count of the price for the week to get all the date of the week
						day = (datetime.datetime.strptime(start_date, '%Y-%b-%d') + datetime.timedelta(days = day_offset)).strftime('%Y-%m-%d')
						date_and_price_data.append([day, price])
					day_offset+=1

		self.date_and_price_data=date_and_price_data
		return date_and_price_data


def main():
  gas_price_data = GasPriceDataScraper()
#   using the power instatiation of class here and the loadpage would only be run once
  gas_price_data.load_page_data()
  gas_price_data.daily_prices()
  gas_price_data.monthly_prices()
  

if __name__ ==  '__main__':
  main()