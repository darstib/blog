# 学习类的继承
class Person:
    def __init__(self, fname, lname, age):
        self.fname = fname
        self.lname = lname
        self.age = age

    def name(self):
        print(self.fname, self.lname, self.age)


class Student(Person):
    def __init__(self, fname, lname, age, year):
        super().__init__(fname, lname, age)
        self.graduationyear = year

    def welcome(self):
        print(
            "Welcome",
            self.fname,
            self.lname,
            "to the class of",
            self.graduationyear,
        )


# 学习迭代器
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 20:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration


# myclass = MyNumbers()
# myiter = iter(myclass)

# for x in myiter:
#     print(x)

# quantity = 3
# itemno = 567
# price = 49
# myorder = "I want {} pieces of item number {} for {:.2f} dollars."
# print(myorder.format(quantity, itemno, price))

f = open("demofile.txt", "r")
print(f.read(10000))
f.close()
