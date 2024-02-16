class Location:
    '''
    The class object that defines the target
    '''


    def __init__(self, location_name, latitude, longitude, arrival_date,
                 weather, celsius, kelvin, postal_code, country):

        self.country = country
        self.location_name = location_name
        self.latitude = latitude
        self.longitude = longitude
        self.arrival_date = arrival_date
        self.weather = weather
        self.celsius = celsius
        self.kelvin = kelvin
        self.postal_code = postal_code
