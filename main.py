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
    catalog (list): List of book in catalog.
    current (int): Index used for Iterator design pattern in get_next() method.
    
    Methods:
    get_catalog() -> list: Returns full catalog.
    get_next() -> Book: Returns next book in catalog.
    add_book(book: Book): Adds book to catalog.
    """
    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(LibraryCatalog, self).__new__(self)
            self.catalog = ["A", "B", "C"]
            self.current = 0
        return self.instance
    
    def get_catalog(self) -> list:
        return self.catalog
        
    #Iterator
    def get_next(self) -> Book:
        if self.current == len(self.get_catalog()):
            self.current = 0
        self.current += 1
        return self.get_catalog()[self.current-1]
        
    def add_book(self, book: Book) -> bool:
        pass

#Adapter
class DataAdapter:
    def read():
        pass


#Factory
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


#Observer


a = LibraryCatalog()
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
