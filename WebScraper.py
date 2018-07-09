#import libraries
import urllib2
from bs4 import BeautifulSoup
import csv
import time
import sys

#run once to update list
#list of all cars on autotrader
args = sys.argv
if (len(args) <= 1) :
	print "please use correct arguments usage option + car id"
else :
	if('u' in args[1]) :
		all_cars = ['ALFA%20ROMEO', 'AUDI', 'BMW', 'CHEVROLET', 'CHRYSLER', 'CITROEN',
		 'DODGE', 'FIAT', 'FORD', 'GWM', 'HONDA', 'HYUNDAI', 'ISUZU', 'JEEP', 'KIA', 'LAND ROVER',
		 'LEXUS', 'MAHINDRA', 'MAZDA', 'MERCEDES-AMG', 'MERCEDES-BENZ', 'MINI', 'MITSUBISHI', 'NISSAN', 'OPEL', 'PEUGEOT', 'PORSCHE',
		 'RENAULT', 'SUBARU', 'SUZUKI', 'TATA', 'TOYOTA', 'VOLKSWAGEN', 'VOLVO']
		pages = [1,2]
		#specify url for each make and save to text file
		#for car in all_cars:
		car = all_cars[int(args[2])]
		with open('car_links/'+args[2]+'.csv', 'a') as csvF:
			something = [1]
			writer = csv.writer(csvF)
			for pageCount in pages:
				print('hi')
				quote_page = 'https://www.autotrader.co.za/sort/price/asc/perpage/60/makemodel/make/'+str(car)+'/price/more-than-50001/page/'+str(pageCount)+'/search'


				#query website and return html to variable 'page'
				page = urllib2.urlopen(quote_page)

				#Get beautiful soup format
				soup = BeautifulSoup(page, 'lxml')

				
				#go through list and find links in adverts and append to list
				possible_links = soup.find_all('a', class_='list-item-advert-link')
				for link in possible_links:
					if link.has_attr('href'):
						print(link.attrs['href'])
						something[0] = link.attrs['href']
						writer.writerow(something)
			

	#Goes into each webpage and scrapes data
	if('s' in args[1]):
		car_db = open('car_details/'+args[2]+'.csv','a')

		writerCsv = csv.writer(car_db)

		i=1
		with open('car_links/'+args[2]+'.csv', 'rb') as csvF:
			linkReader = csv.reader(csvF)
			for link in linkReader:
				
				details = ['dummy']*9
				

				#Gets full page	
				page = urllib2.urlopen(link[0])	
				soup = BeautifulSoup(page, 'lxml')
				#Start scrapping

				#Price scrape
				header = soup.find('div', class_='title-container evo')
				possible_prices = header.find('div',class_='price') 
				pp = possible_prices.find('h2')
				details[7] = pp.text.strip()
				if details[7] != 'POA':
					details[7] = details[7].replace('R','') #Replaces R in price if it has a price



				#Find year, colour, mileage (clear Km and comma from mileage)
				header = soup.find_all('div', class_='col-xs-6 col-md-4 bullet-point')
			
				for spec in header:

					if 'Registration year' in spec.text.strip() :
						details[0] = spec.text.strip().replace('Registration year','') 
					elif 'Colour' in spec.text.strip() :
						details[4] = spec.text.strip().replace('Colour','')
					elif 'Mileage' in spec.text.strip() :
						details[3] = spec.text.strip().replace('Mileage','')
						details[3] = details[3].replace(' Km','')
						details[3] = details[3].replace(',','')
				
				#Find fuel type, make, model and gearbox
				header = soup.find_all('div', class_='accordion-body')
				header_soup = BeautifulSoup(str(header[0]),'lxml')
				header = header_soup.find_all('div',class_='row')
				for spec in header:

					if 'Fuel type' in spec.text.strip() :
						details[6] = spec.text.strip().replace('Fuel type','')
					elif 'Make' in spec.text.strip() :
						details[1] = spec.text.strip().replace('Make','')
					elif 'Model' in spec.text.strip() :
						details[2] = spec.text.strip().replace('Model','')
					elif 'Gearbox' in spec.text.strip() :
						details[5] = spec.text.strip().replace('Gearbox','')
				
				details[8] = i
				i += 1
				#Write to csv file 
				#We filter out cars with 0 mileage
				write = 0
				for value in details :
					#filter out cars with 0 Km as mileage
					if value == '0':
						write -= 1
					#add only when all values were added to array to avoid 
					if value != 'dummy':
						write += 1
					if write == 9:
						writerCsv.writerow(details)
				#writerCsv.writerow(details)
		car_db.close()


