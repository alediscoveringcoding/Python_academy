#there are 2 ways of creating populating/changin the state of the attributes

#1. constructors
#2. setters

class Animal:
    number_of_legs=0    #starea interna a obiectului instantiat 

    def __init__(self, number_of_legs=0)->None:
        self.number_of_legs = number_of_legs

    def __str__(self)->str:
        return f"This animal has {self.number_of_legs} legs"

    def set_number_of_legs(self, n)->None:
        self.number_of_legs = n

    def display_internal_state(self):
        print(self.number_of_legs)
    
    @staticmethod #decorator
    def breath():
        print("... huh huh ...")

print('Bear')
bear = Animal()
bear.set_number_of_legs(4) #used setter to change internal state
#print(bear.number_of_legs)
bear.display_internal_state()
print(bear.__str__())

print('Dog')
dog=Animal(4) #used constructor to set internal state
#print(dog.number_of_legs)
#dog.display_internal_state()
bear.display_internal_state()

print('Omida')
omida=Animal() #used constructor with default value
omida.number_of_legs=200
#print(omida.number_of_legs)
omida.display_internal_state()
omida.breath()


