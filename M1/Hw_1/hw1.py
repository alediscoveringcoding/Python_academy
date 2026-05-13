# Exercise 1
base = float(input("Introdu baza triunghiului: "))
height = float(input("Introdu inaltimea triunghiului: "))
area = 0.5 * base * height
print(f"Tipul variabilei rezultate este {type(area)}")
print(f"Aria triunghiului este: {area}")

# Exercise 2
password = 7710
value = input("Introdu parola: ")
if str(password) == value:
     print("Ai ghicit")
else:
     print("Nu ai ghicit")

# Exercise 3
n1 = input("Introdu primul numar: ")
n2 = input("Introdu al doilea numar: ")
print(f"Media numerelor este: {(float(n1) + float(n2)) / 2}")
print(f"Impartirea numerelor este: {int(n1) // int(n2)}")
print(f"A la puterea b: {int(n1) ** int(n2)}")

# Exercise 4
income = input("Introdu venitul lunar: ")
print("Recomandarile noastre:")
print(f"Cheltuieli uzuale: {float(income) * 0.5}")
print(f"Recreere: {float(income) * 0.3}")
print(f"Economii si datorii: {float(income) * 0.2}")