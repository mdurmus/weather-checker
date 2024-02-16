import pyfiglet
from person import Person
from location import Location
from tools import get_single_valid_date, get_single_select_cities
from tools import convert_date_time, want_report_mail
from tools import get_name, get_email, show_map_hint
from tools import get_weather_info, kelvin_to_celcius_convert, fill_locations
from tools import get_location_information, show_all_route, send_mail
welcome_text = 'Weather Checker!'

banner = pyfiglet.figlet_format(welcome_text)
print(banner)

# Method that retrieves the user's name.
name = get_name()

# The method that retrieves the user's mail address.
mail = get_email()

print()
print(f'Ok {name}, now i will prepare your personal data file...')
print()

# I create person object and fill data
person = Person(name, mail)

print(f'Yes your personal data is ready. I\'ll help ' +
      'you plan your trip or vacation. But we need ' +
      'to agree on some things. Firstly, you need to ' +
      'give me the latitude and longitude of your ' +
      'destination. Can you do that or should ' +
      'I give you a hint?')

# Method that shows the user how to use maps.
show_map_hint()
print()
print('Ok now can continue...')
print()
print('Do you want to select the location from ' +
      'the list or do you want to enter it yourself?')
print()
select = input('1. I select from list \n2. I can enter manually \n')


def manual_enter_location():
    '''
    Method to work if the user wants to enter the locations themselves
    '''
    # I want the user to enter only numeric character.
    while True:
        try:
            print()
            location_count = int(input(f'How many cities do you' +
                                       ' want to add? \n'))
            break
        except ValueError:
            print()
            print('Please enter only numeric value!')
            print()

    # Method that asks for the number of cities
    # specified by the user one by one
    locations = get_location_information(location_count)
    person.locations = locations

    # Method that shows all the cities entered by
    # the user with all relevant information.
    show_all_route(person.locations)
    want_report_mail(person)


def select_from_list():
    '''
    Method to work if the user wants to select locations from a list
    '''
    locations = fill_locations()

    print()
    print('1 - Istanbul, Türkiye')
    print('2 - Paris, France')
    print('3 - London, United Kingdom')
    print('4 - Rome, Italy')
    print('5 - Bangkok, Thailand')
    print()
    print('Which city or cities would you like to go to? ')
    print()
    selected_cities = get_single_select_cities()
    # I created a list of the user's input separated by commas
    selected_indexes = selected_cities.split(',')
    selected_locations = []
    for index in selected_indexes:
        # I fill selected locations
        selected_locations.append(locations[int(index) - 1])
    print()
    # I need to get the departure dates from the user
    for item in selected_locations:
        arrival_date = get_single_valid_date(item.location_name)
        item.arrival_date = arrival_date
    print()
    # updating weather conditions for locations.
    for item in selected_locations:
        converted_date = convert_date_time(item.arrival_date)
        weather_data = get_weather_info(item.latitude, item.longitude,
                                        converted_date)
        item.weather = weather_data['description']
        item.kelvin = weather_data['temperature']
        item.celsius = kelvin_to_celcius_convert(item.kelvin)
    # I must update person object.
    person.locations = selected_locations
    # Listing location informations
    show_all_route(person.locations)
    want_report_mail(person)


if select == "1":
    select_from_list()
elif select == "2":
    manual_enter_location()
