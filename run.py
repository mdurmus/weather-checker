import pyfiglet
from person import Person
from tools import get_name, get_email, show_map_hint 
from tools import get_location_information, show_all_route,send_mail
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
person = Person(name,mail)

print(f'Yes your personal data is ready. I\'ll help you plan your trip or vacation. But we need to agree on some things. Firstly, you need to give me the latitude and longitude of your destination. Can you do that or should I give you a hint?')

# Method that shows the user how to use maps.
show_map_hint()

print('Ok now can continue...')
print()


# I want the user to enter only numeric character.
while True:
    try:
        print()
        location_count = int(input('How many cities do you want to add? '))
        break
    except ValueError:
        print()
        print('Please enter only numeric value!')
        print()

# Method that asks for the number of cities specified by the user one by one
locations = get_location_information(location_count)
person.locations = locations

# Method that shows all the cities entered by the user with all relevant information.
show_all_route(person.locations)


mail_result = input('Do you want me to send this information to your email address? Y / N ').upper()

if mail_result == 'Y':
    # If user want, this method send all information to user as e-mail
    send_mail(person)
else:
    print('See you again!')


