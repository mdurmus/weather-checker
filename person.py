class Person:
    '''
    This class defining the person object
    '''
    def __init__(self, person_name, person_email):
        self.person_name = person_name
        self.person_email = person_email
        self.locations = []

    def add_location_person(self, location):
        self.locations.append(location)
