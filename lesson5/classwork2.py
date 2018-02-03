class Basket:
    storage = []
    def __init__(self, measure):
        self.measure = measure
    def put_into(self, obj):
        if len(self.storage) < self.measure:
            print("Object inputed")
            self.storage.append(obj)
        else:
            raise ValueError("Can not put into")


class Package(Basket):
    pass


class InputClass:
    pass

bask = Basket(2)
print(bask.measure)
pack = Package(3)
print(pack.measure)

bask.put_into(InputClass())
print(bask.storage)
bask.put_into(InputClass())
bask.put_into(InputClass())
