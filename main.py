class Book:
    """
    Class representing book.
    
    Parameters:
    name (str): Book name.
    identify (int): Book ID.
    year (int): Book year publication.
    """
    def __init__(self, name: str, identify: int, year: int):
        self.name = name
        self.identify = identify
        self.year = year

    def __str__(self) -> str:
        return f"{self.name}, {self.year}, id: {self.identify}"

#Singleton + Iterator
class LibraryCatalog(object):
    """
    Class representing book catalog in library.
    It uses Singleton pattern design (one catalog is enough) and 
    Iterator (to show next books in catalog).
    
    Constructor parameters:
    None
    
    Parameters:
    instance (LibraryCatalog): Singleton instance.
    catalog (dict(Book: list(int, int))): Dictionary with books in catalog, their available count and total count.
    current (int): Index used for Iterator design pattern in get_next() method.
    
    Methods:
    get_catalog() -> dict: Returns full catalog.
    get_next() -> str: Returns next book in catalog.
    add_book(book: Book) -> int: Adds book to catalog. Increases count and returns 1 if book already exists, otherwise returns 2.
    """
    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(LibraryCatalog, self).__new__(self)
            self.catalog = {}
            self.current = 0
        return self.instance
    
    def get_catalog(self) -> list:
        return self.catalog
        
    #Iterator
    def get_next(self) -> Book:
        if len(self.get_catalog()) < 1:
            return None
        if self.current == len(self.get_catalog()):
            self.current = 0
        self.current += 1
        book_key = list(self.get_catalog().keys())[self.current-1] 
        return f"{book_key}, {self.catalog[book_key][0]}/{self.catalog[book_key][1]}"
        
    def add_book(self, book: Book) -> int:
        if book not in self.catalog:
            self.catalog[book] = [1, 1]
            return 2
        else:
            self.catalog[book][0] += 1
            self.catalog[book][1] += 1
        return 1

#Adapter
class DataAdapter:
    def read():
        pass


#Classes for Factory
class User:
    def __init__(self, name: str):
        self.name = name
        self.limit = 0
        self.books = []
        raise NotImplementedError("User is supposed to be an abstract class")

    def borrow_book(identify: int) -> bool:
        if self.limit >= len(self.books):
            #log "max book limit reached"
            return False
        #Code for facade - find book, borrow it or not, connect user with Observer
        return True
            
    def return_book(identify: int) -> bool:
        for i in self.books:
            if i.identify == identify:
                #Code for Facade, make book available, update Observer
                return True
        return False


class Student(User):
    def __init__(self, name: str):
        self.name = name
        self.limit = 5
        self.books = []


class Teacher(User):
    def __init__(self, name: str):
        self.name = name
        self.limit = 15
        self.books = []


class Librarian(User):
    def __init__(self, name: str):
        self.name = name
        self.limit = 25
        self.books = []


#Factory
class UserFactory:
    def create_user(user: str, name: str) -> User:
        if user == "student":
            return Student(name)
        elif user == "teacher":
            return Teacher(name)
        elif user == "librarian":
            return Librarian(name)
        else:
            raise TypeError("Unknown user kind inserted.")


#Facade
class ActionInterface:
    def __init__(self, catalog: LibraryCatalog):
        self.catalog = catalog
        
    def add_book(self, book):
        return self.catalog.add_book(book)
        
    def show_catalog(self):
        return self.catalog.get_catalog()
    
    def show_any_book(self):
        return self.catalog.get_next()
        
    def borrow_book(self):
        pass
    
    def return_book(self):
        pass

#Observer


a = LibraryCatalog()
for i in ["A", "B", "C", "D"]:
    a.add_book(i)
print(a.get_catalog())
b = LibraryCatalog()
print(a is b)
print(a == b)
print(range(5) is range(5))
print(range(5) == range(5))
for i in range(7):
    print(a.get_next())
try:
    error_class = User("A")
except Exception as e:
    print(e)
try:
    error_class = UserFactory.create_user(User, "A")
except Exception as e:
    print(e)
test_interface = ActionInterface(a)
print(test_interface.add_book("D"))
print(test_interface.show_catalog())
print(test_interface.show_any_book())
