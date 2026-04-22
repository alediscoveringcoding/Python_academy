#there are 2 ways of creating populating/changin the state of the attributes

#1. constructors
#2. setters

class Animal:
    number_of_legs=0    #starea interna a obiectului instantiat 

    def __init__(self, number_of_legs=0)->None:
        self.number_of_legs = number_of_legs

    def set_number_of_legs(self, n)->None:
        self.number_of_legs = n

print('Bear')
bear = Animal()
bear.set_number_of_legs(4) #used setter to change internal state
print(bear.number_of_legs)

print('Dog')
dog=Animal(4) #used constructor to set internal state

print(dog.number_of_legs)

