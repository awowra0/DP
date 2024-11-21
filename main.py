
class Book:
    def __init__(self, name, identify, year):
        self.name = name
        self.identify = identify
        self.year = year

    def __str__(self):
        return f"{self.name}, {self.year}, id: {self.year}"

#Singleton
class LibraryCatalog(object):
    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(LibraryCatalog, self).__new__(self)
            self.catalog = ["A", "B", "C"]
            self.current = 0
        return self.instance
    
    def get_catalog(self):
        return self.catalog
        
    #Iterator
    def get_next(self):
        if self.current == len(self.get_catalog()):
            self.current = 0
        self.current += 1
        return self.get_catalog()[self.current-1]

#Adapter
class DataAdapter:
    def read():
        pass


#Iterator



a = LibraryCatalog()
print(a.get_catalog())
b = LibraryCatalog()
print(a is b)
print(a == b)
print(range(5) is range(5))
print(range(5) == range(5))
for i in range(7):
    print(a.get_next())
