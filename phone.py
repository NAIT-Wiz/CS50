people = [
    "Carter" , "number": "236773701940",
    "David" , "number": "2367737019",
    "John" , "number": "23677370",
    "Car" , "number": "236773",
]

name = input("Name:")

if name in people:
    number =people[name]
    print(f"Found {number}")
        break
else:
   print("Not found")
