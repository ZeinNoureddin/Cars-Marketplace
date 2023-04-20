import scrapy
import json
import time
import datetime
import re
from datetime import datetime
from scrapy.http import HtmlResponse
from scrapy import Request

count = 1
class OlxspiderSpider(scrapy.Spider):

    name = "adScraper"
    allowed_domains = ["www.olx.com.eg"]
    start_urls = ["https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?filter=new_used_eq_2%2Cyear_between_2000_to_2023"]

    # FUNCTION THAT GOES TO THE MAIN PAGES AND NAVIGATES TO EACH LINK OF THE ADS
    def parse(self, response):

        global count
        with open('cookies.txt','r') as f:
                 cookiesJson = json.load(f)

        for link in response.css('li.c46f3bfe'):
            adPostingDate = link.css('span._2e28a695 span::text').get()
            if "hour" in adPostingDate or "hours" in adPostingDate or "day" in adPostingDate or "days" in adPostingDate or "week" in adPostingDate or "weeks" in adPostingDate or "1 month" in adPostingDate:
                adLink = link.css('div._41d2b9f3 a::attr(href)').get()
                adLink = 'https://www.olx.com.eg' +  adLink
                request = Request(url = adLink, cookies = cookiesJson, callback = self.parsePage)
                request.cb_kwargs['isAdLink'] = True
                yield request
                
        count = count + 1
        yield scrapy.Request(f'https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?page={count}&filter=new_used_eq_2%2Cyear_between_2000_to_2023', callback = self.parse, cookies = cookiesJson)


    # FUNCTION THAT GOES TO EACH AD AND SCRAPES THE DATA
    # The boolean isAdLink is used to check if the link is the link of the ad or the api link to get the phone number. We only yield after we've found the phone number, but first we scrape the data from the page itself.
    def parsePage(self,response: HtmlResponse, isAdLink: bool, **kwargs):
        if isAdLink:
            #CAR DETAILS
            # list = ['Brand', 'Kia', 'Model', 'Rio', 'Ad Type', 'For Sale', 'Fuel Type', 'Benzine', 'Price', '387,000', 'Price Type', 'Price', 'Payment Options', 'Cash', 'Year', '2015', 'Kilometers', '100000 to 119999',
            # 'Transmission Type', 'Automatic', 'Condition', 'Used', 'Color', 'Red', 'Body Type', 'Sedan', 'Engine Capacity (CC)', '1400 - 1500', 'Video', 'Not Available', 'Virtual Tour', 'Not Available']
            list = response.css('div.b44ca0b3 span::text').getall()
            adID = response.selector.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[6]/div[1]/text()').get().replace('Ad id ', ''),
            
            keys = list[::2]
            values = list[1::2]

            # CREATING A DICTIONARY TO STORE THE DATA
            dictionary = dict(zip(keys, values))

            carData = {}
            carData['Brand'] = dictionary['Brand'] if 'Brand' in dictionary else ''
            carData['Model'] = dictionary['Model'] if 'Model' in dictionary else ''
            carData['Ad Type'] = dictionary['Ad Type'] if 'Ad Type' in dictionary else ''
            carData['Fuel Type'] = dictionary['Fuel Type'] if 'Fuel Type' in dictionary else ''
            carData['Price'] = dictionary['Price'] if 'Price' in dictionary else ''
            carData['Price Type'] = dictionary['Price Type'] if 'Price Type' in dictionary else ''
            carData['Payment Options'] = dictionary['Payment Options'] if 'Payment Options' in dictionary else ''
            carData['Year'] = dictionary['Year'] if 'Year' in dictionary else ''
            carData['Kilometers'] = dictionary['Kilometers'] if 'Kilometers' in dictionary else ''
            carData['Transmission Type'] = dictionary['Transmission Type'] if 'Transmission Type' in dictionary else ''
            carData['Condition'] = dictionary['Condition'] if 'Condition' in dictionary else ''
            carData['Color'] = dictionary['Color'] if 'Color' in dictionary else ''
            carData['Body Type'] = dictionary['Body Type'] if 'Body Type' in dictionary else ''
            carData['Engine Capacity (CC)'] = dictionary['Engine Capacity (CC)'] if 'Engine Capacity (CC)' in dictionary else ''
            
            # TRY AND EXCEPT FOR LOCATION
            try:
                location = response.css('div._1075545d.e3cecb8b._5f872d11')
                location = location.css('span::text').get().replace(', Cairo','')
            except:
                location = ''

            # TRY AND EXCEPT FOR DESCRIPTION
            try: 
                description = response.css('div._0f86855a span::text').get()
            except:
                description = ''

            # GETTING THE OWNER JOINING DATE
            ownerJoinDate = response.css('div._05330198 span::text').get().replace('Member since ','')
            ownerJoinDate = datetime.strptime(ownerJoinDate.replace(' ', '-'), '%b-%Y')
            ownerJoinDateFinal = ownerJoinDate.strftime('%Y-%m-%d')

            # GETTING EXTRA PHONE NUMBERS FROM DESCRIPTION
            extraPhoneNumbers = []
            if description != '':
                phoneNoPattern = re.compile(r'(\+2)?01\d{9}')
                for match in phoneNoPattern.finditer(description):
                    extraPhoneNumbers.append(match.group(0))
                extraPhoneNumbers = '-'.join(extraPhoneNumbers)


            # GETTING ENGINE CAPACITY MAX AND MIN
            if carData['Engine Capacity (CC)'] != '':
                if "More than" in carData['Engine Capacity (CC)']:
                    ECMin = "3000"
                    ECMax = ""
                elif " - " in carData['Engine Capacity (CC)']:
                    ECMin = carData['Engine Capacity (CC)'].split(" - ")[0]
                    ECMax = carData['Engine Capacity (CC)'].split(" - ")[1]
                else:
                    ECMin = carData['Engine Capacity (CC)']
                    ECMax = carData['Engine Capacity (CC)']
            else:
                ECMin = ''
                ECMax = ''

            # GETTING KILOMETERS MAX AND MIN   
            if "More than" in carData['Kilometers']:
                KilometersMin = "200000"
                KilometersMax = ""
            else: 
                KilometersMin = carData['Kilometers'].split(" to ")[0]
                KilometersMax = carData['Kilometers'].split(" to ")[1]

            # GETTING EXTRA FEATURES 
            try:
                extraFeatures = response.css('div._27f9c8ac span::text')
                extraFeatures = extraFeatures.getall()
                extraFeatures = ','.join(extraFeatures)
            except:
                extraFeatures = None

            # GETTING THE LINK TO GET OWNER'S PHONE NUMBER
            apiLink = f'https://www.olx.com.eg/api/listing/{adID[0]}/contactInfo/'

            # PASSING THE COOKIES BE ABLE TO PARSE THE PAGE
            with open('cookies.txt','r') as f:
                 cookiesJson = json.load(f)

            request = Request (url = apiLink, cookies = cookiesJson, callback = self.parsePage)
            # PASSING THE RETRIEVED DATA TO THE NEXT FUNCTION CALL
            request.cb_kwargs['isAdLink'] = False
            request.cb_kwargs['dataToYield'] = {
                'adID' : adID,
                'ownerName': response.selector.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[2]/div/a/div/div[2]/span/text()').get(),
                'joinDate' : ownerJoinDateFinal,
                'location': location, #response.selector.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[5]/div/span[2]/text()').get().replace(', Cairo', ''),
                'description': description,

                'extraPhoneNumbers': extraPhoneNumbers,
                'extrafeatures': extraFeatures,

                'Brand': carData['Brand'],
                'Model': carData['Model'],
                'Ad Type': carData['Ad Type'],
                'Fuel Type': carData['Fuel Type'],
                'Price': carData['Price'],
                'Price Type': carData['Price Type'],
                'Payment Options': carData['Payment Options'],
                'Year': carData['Year'],
                'Minimum Kilometers': KilometersMin,
                'Maximum Kilometers': KilometersMax,
                'Transmission Type': carData['Transmission Type'],
                'Condition': carData['Condition'],
                'Color': carData['Color'],
                'Body Type': carData['Body Type'],
                'Minimum Engine Capacity (CC)': ECMin,
                'Maximum Engine Capacity (CC)': ECMax,
            }
            yield request

        else: 

            # GETTING THE PHONE NUMBER
            englishPhonePattern = re.compile(r'(\+?\d{1,3}[-\.\s]?)?\d{10,13}')
            numbers = []
            for match in englishPhonePattern.finditer(response.text):
                numbers.append(match.group(0))

            # STORING EVERYTHING I WANT TO YIELD
            newInfo = {
                'adID' : response.cb_kwargs['dataToYield']['adID'],
                'ownerName' : response.cb_kwargs['dataToYield']['ownerName'],
                'joinDate' : response.cb_kwargs['dataToYield']['joinDate'],
                'location' : response.cb_kwargs['dataToYield']['location'],
                'description' : response.cb_kwargs['dataToYield']['description'],
                'extraPhoneNumbers' : response.cb_kwargs['dataToYield']['extraPhoneNumbers'],
                'extrafeatures' : response.cb_kwargs['dataToYield']['extrafeatures'],
                'Brand' : response.cb_kwargs['dataToYield']['Brand'],
                'Model' : response.cb_kwargs['dataToYield']['Model'],
                'Ad Type' : response.cb_kwargs['dataToYield']['Ad Type'],
                'Fuel Type' : response.cb_kwargs['dataToYield']['Fuel Type'],
                'Price' : response.cb_kwargs['dataToYield']['Price'],
                'Price Type' : response.cb_kwargs['dataToYield']['Price Type'],
                'Payment Options' : response.cb_kwargs['dataToYield']['Payment Options'],
                'Year' : response.cb_kwargs['dataToYield']['Year'],
                'Minimum Kilometers' : response.cb_kwargs['dataToYield']['Minimum Kilometers'],
                'Maximum Kilometers' : response.cb_kwargs['dataToYield']['Maximum Kilometers'],
                'Transmission Type' : response.cb_kwargs['dataToYield']['Transmission Type'],
                'Condition' : response.cb_kwargs['dataToYield']['Condition'],
                'Color' : response.cb_kwargs['dataToYield']['Color'],
                'Body Type' : response.cb_kwargs['dataToYield']['Body Type'],
                'Minimum Engine Capacity (CC)' : response.cb_kwargs['dataToYield']['Minimum Engine Capacity (CC)'],
                'Maximum Engine Capacity (CC)' : response.cb_kwargs['dataToYield']['Maximum Engine Capacity (CC)'],
                'ownerPhoneNumber' : numbers[0],
            }
            # YIELDING IF WE FIND A PHONE NUMBER
            if numbers[0] is not None:
                yield newInfo