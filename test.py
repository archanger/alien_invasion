class Human:
    __name = ''
    __email = ''

    def __init__(self, name, email):
        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name
    
    def __repr__(self):
        return "Name: {0}, email: {1}".format(self.__name, self.__email)

h = Human('My name', 'cool')
h2 = Human('My second name', 'cool2')
print(h2.name)