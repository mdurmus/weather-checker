import re
import requests
import smtplib
from location import Location
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
from datetime import datetime


def get_name():
    '''
    Method that allows the user to enter a real or valid name
    '''
    
    
    while True:
        name = input('What is your name? ')
        #I use it to verify that the information entered is 
        # only alphanumeric characters
        if name.isalpha():
            print()
            print(f'Welcome {name}')
            print()
            return name
        else:
            print()
            print('Please enter valid name (only alpha characters)'+
                  ' and one word!')
            print()


def get_email():
    '''
    Method that allows the user to enter a valid email
    '''


    while True:
        # I use regex to make sure that the user enters a real email address.
        email = input('Please enter your email: ')
        pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+')
        match = re.fullmatch(pattern, email)
        if match:
            return email
        else:
            print()
            print('Please enter a valid email address, for example: xx@xx.com')
            print()


def show_map_hint():
    '''
    A method that shows the user how to get latitude and longitude numbers on maps.
    '''


    print()
    need_help = input('Please type Y or N and press return key. If you press a letter other than Y, the system accept it as N! ')
    need_help = need_help.upper()
    if need_help =='Y':
        print()
        print('Open the Google maps service. Find the place you want to go on the map. When you click the right mouse button on the place you want to go, you will see two decimal numbers at the top of the menu that opens, these are the numbers I want from you. For example: 53.298185248091954, -6.178650603203118')
        print()
        print('For more information please visit: https://support.google.com/maps/answer/18539?hl=en&co=GENIE.Platform%3DDesktop')
        print()
    else:
        print()
    print('Good sound!')


def get_valid_date():
    '''
    User must input valid date string
    '''
    
    
    reg_pattern = r'^\d{4}-\d{2}-\d{2}$'
    while True:
        user_input = input('Enter arrival date (YYYY-MM-DD): ')
        if re.fullmatch(reg_pattern,user_input):
            return user_input
        else:
            print('Invalid date format. Please enter in \'YYYY-MM-DD\' format.')


def get_location_information(location_count):
    '''
    Method that gets the city information to be added 
    to the system from the user and creates an object.
    '''


    # I create a city list item.
    location_list = []

    # I create a loop with the number of cities entered by the user.    
    for i in range(location_count):
        # I used a tuple to store the city information.
        location_data = get_latitude_longitude(i)
        name = f'{i + 1}'
        print()
        arrival_date = get_valid_date() 
        # I converted the date because the Openweather 
        # API works with unix datetime.
        time_stamp = convert_date_time(arrival_date)
        weather_data = get_weather_info(location_data[0],
                                        location_data[1],time_stamp)
        kelvin = weather_data['temperature']
        weather = weather_data['description']
        celcius = kelvin_to_celcius_convert(kelvin)
        # I create a city object
        location = Location(name,location_data[0],location_data[1],
                            arrival_date,weather,celcius,kelvin,
                            location_data[2],location_data[3])
        location_list.append(location)

    return location_list


def kelvin_to_celcius_convert(kelvin):
    '''
    This method convert kelvin value to celcius value
    '''
    celcius = kelvin - 273.15
    celcius_format = "{:.1f}".format(celcius)
    return celcius_format


def check_latitude_longitude(type, location_no):
    '''
    Method that allows the user to enter the actual latitude and longitude
    '''
    while True:
        data = input(f"Please paste  {location_no}. city {type} value: ")
        if '.' not in data:
            print("Please enter a dotted float value!")
        try:
            data = float(data)
            return data
        except ValueError:
            print(f"The value you entered is not in" +  
                  "the required format, please check and try again")


def get_latitude_longitude(location_no):
    '''
    Method to verify entered coordinates
    '''


    location_no +=1
    while True:
        print()

        latitude = check_latitude_longitude('latitude',location_no)

        longitude = check_latitude_longitude('longitude',location_no)

        print()
        geolocator = Nominatim(user_agent = "demo")
        location = geolocator.reverse(f"{latitude},{longitude}")
        # I wrote the whole address on the screen to be able to verify it.
        print(location.address)
        post_code = location.raw['address']['postcode']
        country = location.raw['address']['country']
        print()
        location_result = input('Is this correct city? Y / N ').upper()
        if location_result == 'Y':
            print()
            print('Location added.')
            return (latitude,longitude,post_code,country)
        elif location_result == 'N':
            print('\nPlease enter another latitude or longitude data.')
        else:
            print('Invalid input!')           


def get_weather_info(latitude,longitude,date):
    '''
    Method to retrieve weather information.
    '''


    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&dt={date}&appid=1406b02bd8391df1c6d7b280122de5ca"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
         # I only got two pieces of information, but there is actually much more
        return {
            "description": weather_description,
            "temperature": temperature
        }
    else:
        return None


def convert_date_time(date):
    '''
    This method convert date to unix date format
    '''


    date = datetime.strptime(date,"%Y-%m-%d")
    api_format = int(date.timestamp())
    return api_format


def show_all_route(locations):
    print()
    print('##################################')
    print()
    print('Here is the weather list for the locations you want to visit!')
    print()
    for location in locations:
        print(f"Location: {location.location_name}\nPostal Code: {location.postal_code}\nCountry: {location.country}\nLatitude: {location.latitude}\nLongitude: {location.longitude}\nArrival Date: {location.arrival_date}\nWeather: {location.weather}\nCelsius: {location.celsius}°C\nKelvin: {location.kelvin}K\n")
    print('##################################')
    print()


def send_mail(person):
    subject = f"Hello {person.person_name}, report from Weather Reporter"
    body = "The locations and weather conditions you want to go to: \n "
    for location in person.locations:
        text = f"Location: {location.location_name}\nPostal Code: {location.postal_code}\nCountry: {location.country}\nLatitude: {location.latitude}\nLongitude: {location.longitude}\n Arrival Date: {location.arrival_date}\nWeather: {location.weather}\nCelsius: {location.celsius}°C\nKelvin: {location.kelvin}K\n-----------\n"
        body += text

    password = "Demo123?"
    receiver = person.person_email
    sender = "demo@mehmetdurmus.de"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('mail.your-server.de',465) as smtp_server : 
           smtp_server.login(sender,password)
           smtp_server.sendmail(sender,receiver, msg.as_string())

    print('Weather report sended your email, please check your mailbox...')
