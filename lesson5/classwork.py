class Room:
    number = "Room 1"
    floor = 1
    def __init__(self, room_size, conditioner=False):
        print("Init started")
        self.room_size = room_size
        self.conditioner = conditioner
    
    def __repr__(self):
        return "this is Room object"

    def funcname(self):
        print("JJJJ")

r = Room("2 bed")
r1 = Room("1 bed", True)

print(r.number, r1.number)
print(r.floor, r1.floor)
r.funcname()
print(r.room_size)
print(r.conditioner)
print(r)