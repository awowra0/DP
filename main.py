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
        return f"{self.name}, {self.year}, id {self.identify}"

    def __repr__(self) -> str:
        return f"{self.name}, {self.year}, id {self.identify}"


#Classes for Factory
class User:
    def __init__(self, name: str):
        self.name = name
        self.limit = 0
        self.books = []
        raise NotImplementedError("User is supposed to be an abstract class")


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
        return f"{book_key}, count: {self.catalog[book_key][0]}/{self.catalog[book_key][1]}"
        
    def add_book(self, book: Book) -> int:
        for i in list(self.catalog.keys()):
            if (i.name, i.identify, i.year) == (book.name, book.identify, book.year):
                self.catalog[i][0] += 1
                self.catalog[i][1] += 1
                return 1
        else:
            self.catalog[book] = [1, 1]
            return 2
        
    def borrow_book(self, user: User, identify: int) -> int:
        if user.limit <= len(user.books):
            #Max book limit reached
            return -1
        for i in self.catalog:
            if i.identify == identify:
                for j in user.books:
                    if j[0].identify == identify:
                        #User already has this book
                        return -2
                if self.catalog[i][0] < 1:
                    #Book unavailable right now, add user to observers
                    #Observer code
                    return 0
                else:
                    #Give book to user's list as ordered (not taken yet)
                    user.books.append([i, "Ordered"])
                    self.catalog[i][0] -= 1
                    return 1
        #This book is not in catalog
        return -3
            
    def return_book(self, user:User, identify: int) -> int:
        if len(user.books) < 1:
            #What does user want to return?
            return -1
        for i in self.catalog:
            if i.identify == identify:
                for j in user.books:
                    if j[0].identify == identify:
                        #Everything is in order
                        user.books.remove(j)
                        self.catalog[i][0] += 1
                        return 1
                #User did not borrow this book
                return -2
        #This book is not in catalog
        return -3
        
    def update_borrow(self, user: User, identify: int) -> int:
        for i in user.books:
            if i[0].identify == identify:
                if i[1] == "Ordered":
                    #User took the book
                    i[1] = "Borrowed"
                    return 1
                #Book is not ordered (it is probably taken already)
                return -1
        #User does not have this book in list
        return -2

#Adapter
class DataAdapter:
    def read():
        pass


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
        
    def add_book(self, book) -> bool:
        return self.catalog.add_book(book)
        
    def show_catalog(self) -> dict:
        return self.catalog.get_catalog()
    
    def show_any_book(self) -> str:
        return self.catalog.get_next()
        
    def borrow_book(self, user: User, identify: int) -> int:
        return self.catalog.borrow_book(user, identify)
    
    def return_book(self, user: User, identify: int) -> int:
        return self.catalog.return_book(user, identify)

    def update_borrow(self, user: User, identify: int) -> int:
        return self.catalog.update_borrow(user, identify)


#Observer


a = LibraryCatalog()
for i in [Book("A", 0, 1999), Book("B", 1, 2002), Book("C", 2, 2004), Book("D", 3, 2020)]:
    a.add_book(i)
print(f"Called LibraryCatalog.get_catalog(): {a.get_catalog()}")
b = LibraryCatalog()
print(f"Called 'a is b': {a is b}")
print(f"Called 'a == b': {a == b}")
print(f"Called 'range(5) is range(5)': {range(5) is range(5)}")
print(f"Called 'range(5) == range(5)': {range(5) == range(5)}")
print(f"Called Iterator 7 times:")
for i in range(7):
    print(a.get_next())
print(f"Creating abstract class User ...")
try:
    error_class = User("A")
except Exception as e:
    print(e)
print(f"Creating unknown user type ...")
try:
    error_class = UserFactory.create_user("user", "A")
except Exception as e:
    print(e)
test_interface = ActionInterface(a)
print(f"Called Facade add_book(): {test_interface.add_book(Book('D', 3, 2020))}")
print(f"Called Facade show_catalog(): {test_interface.show_catalog()}")
print(f"Called Facade show_any_book(): {test_interface.show_any_book()}")

test_user = UserFactory.create_user("student", "XYZ")
print(f"Called Facade borrow_book: {test_interface.borrow_book(test_user, 3)}")
print(f"Called Facade borrow_book again: {test_interface.borrow_book(test_user, 3)}")
print(f"Checked user books: {test_user.books}")
print(f"Called Facade update_borrow(): {test_interface.update_borrow(test_user, 3)}")
print(f"Checked user books: {test_user.books}")
print(f"Called Facade return_book: {test_interface.return_book(test_user, 3)}")
print(f"Checked user books: {test_user.books}")
