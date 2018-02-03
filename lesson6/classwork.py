class ParentCalc(object):
    def __init__(self, value):
        print("Into parent")
        self.value = value
    def calculate(self):
        return self.value * 2 + 20


class ChildCalc(ParentCalc):
    def __init__(self, value, k=2):
        super().__init__(value)
        print("Into Child")
        self.k = k
    def calculate(self):
        a = self.k + 1
        previous_calc = super().calculate()
        return -1 * self.k * previous_calc

x = ParentCalc(15)
print(x.calculate())

e = ChildCalc(15, k=5)
print(e.calculate())

print(ChildCalc.__mro__)
# method resolution order


a = 257
b = 257
a is b #False

# but

a = 256
b = 256
a is b # True

# -5 to 256