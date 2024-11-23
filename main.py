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
    """
    Abstract class representing user. Do not use it directly.
    
    Constructor parameters:
    name (str): User name.
    
    Parameters:
    name (str): User name.
    limit (int): Book limit.
    books (list(Book, str)): List containing books and their statuses - "Ordered" or "Borrowed"
    """
    def __init__(self, name: str):
        self.name = name
        self.limit = 0
        self.books = []
        raise NotImplementedError("User is supposed to be an abstract class")


class Student(User):
    """
    Class representing student.
    
    Constructor parameters:
    name (str): User name.
    
    Parameters:
    name (str): User name.
    limit (int): Book limit.
    books (list(Book, str)): List containing books and their statuses - "Ordered" or "Borrowed"
    """
    def __init__(self, name: str):
        self.name = name
        self.limit = 5
        self.books = []


class Teacher(User):
    """
    Class representing teacher.
    
    Constructor parameters:
    name (str): User name.
    
    Parameters:
    name (str): User name.
    limit (int): Book limit.
    books (list(Book, str)): List containing books and their statuses - "Ordered" or "Borrowed"
    """
    def __init__(self, name: str):
        self.name = name
        self.limit = 15
        self.books = []


class Librarian(User):
    """
    Class representing librarian.
    
    Constructor parameters:
    name (str): User name.
    
    Parameters:
    name (str): User name.
    limit (int): Book limit.
    books (list(Book, str)): List containing books and their statuses - "Ordered" or "Borrowed"
    """
    def __init__(self, name: str):
        self.name = name
        self.limit = 25
        self.books = []


#Observer
class Observer:
    """
    Class representing Observer design pattern.
    
    Constructor parameters:
    user (User): Reference to user who awaits book.
    book (Book): Observed book.
    
    Parameters:
    user (User): Reference to user who awaits book.
    books (list(Book)): List of observed books.
    infos (list(str)): A list of notification sent to user.
    
    Methods:
    update(text: str) -> str: Adds new notification. 
    """
    def __init__(self, user: User, book: Book):
        self.user = user
        self.books = [book]
        self.infos = []
    
    def update(self, text: str) -> str:
        self.infos.append(text)
        return text

class ObserverManager:
    """
    Class representing manager for Observer design pattern.
    
    Parameters:
    observers (list(Observer)): List of observers.
    
    Methods:
    attach(user: User, book: Book) -> int: Tries to create a new observer from given user and book. Adds new observer and returns 1 if user is not an observer, adds new book to observer's list and returns 0 if user is one or returns -1 if user has already been waiting for this book.
    deattach(user: User, book: Book) -> int: Tries to remove book from user's observer instance. Removes this book and returns 1 if the book is in observer's list, return 0 if observer has no book in list, returns -1 if book is not in observer's list or returns -2 if given user is not an observer.
    notify(book: Book): Notifies proper observers that their book is currently available.
    
    Notes:
    Why Observer? It gives an opportunity to create an automated system that sends information about books to interested users as soon as possible.
    """
    def __init__(self):
        self.observers = []
    
    def attach(self, user: User, book: Book) -> int:
        for i in self.observers:
            if i.user.name == user.name:
                for j in i.books:
                    if j.identify == book.identify:
                        i.update(f"User: {i.user.name} already wishlisted book {book}.")
                        return -1
                i.books.append(book)
                i.update(f"User: {i.user.name} added book {book} to wishlist.")
                return 0
        self.observers.append(Observer(user, book))
        self.observers[-1].update(f"User {self.observers[-1].user.name} wishlisted book {book}.")
        return 1
    
    def deattach(self, user: User, book: Book) -> 1:
        for i in self.observers:
            if i.user.name == user.name:
                if len(user.books) < 1:
                    #User has no book in wishlist
                    return 0
                for j in i.books:
                    if j.identify == book.identify:
                        #remove book from wishlist
                        i.books.remove(j)
                        return 1
                #Book not found in wishlist
                return -1
        #Observer not found
        return -2
    
    def notify(self, book):
        for i in self.observers:
            for j in i.books:
                if j.identify == book.identify:
                    #Inform observer
                    i.update(f"User {i.user.name} - book {book} is available.")
                    break


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
    borrow_book(user: User, identify: int, manager: ObserverManager) -> int: Tries to find a book by its ID and declare one of copies as ordered by user. Decreases book count and returns 1 if user has not reached book limit and book is available, 0 if book is unavailable right now, -1 if user reached book limit, -2 if user already ordered this book or -3 if book does not exist. Informs ObserverManager to notify users.
    return_book(user: User, identify: int, manager: ObserverManager) -> int: Tries to find a book by its ID and return it to library. Increases book count, removes it from user's list and returns 1 if the book exists and user has it, -1 if user has no book borrowed, -2 if user has not borrowed this book or -3 if the book does not exist. Informs ObserverManager to notify users.
    update_borrow(user: User, identify: int) -> int: Tries to update book's status in user's list from "Ordered" to "Borrowed". Changes status and returns 1 if user has this book and it is "Ordered", -1 if the book is not "Ordered" or -2 if user does not have this book in its list. 
    
    Notes:
    Why Singleton? Library needs only one catalog for books. Creating second one may make a mess with searching in two catalog and this would be troublesome.
    Why Iterator? Catalog may become very big in time and looking at dictionary of all books can be confusing. By showing one book lineally, user can look at different book every time if catalog is big enough.
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
        
    def borrow_book(self, user: User, identify: int, manager: ObserverManager) -> int:
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
                    manager.attach(user, i)
                    return 0
                else:
                    #Give book to user's list as ordered (not taken yet)
                    user.books.append([i, "Ordered"])
                    self.catalog[i][0] -= 1
                    manager.deattach(user, i)
                    return 1
        #This book is not in catalog
        return -3
            
    def return_book(self, user:User, identify: int, manager: ObserverManager) -> int:
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
                        if self.catalog[i][0] == 1:
                            #Book is available, inform observers
                            manager.notify(i)
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
    """
    Class implementing Factory design pattern to create new users.
    
    Methods:
    create_user(user: str, name: str) -> User: Tries to create a proper user class. Return Student, Teacher or Librarian class with chosen name or raises Error for different class names.
    
    Notes:
    Why Factory? It is a simple solution to create multiple various accounts. Now it is obvious what classes are available plus method input can be universal.
    """
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
    """
    Class implementing Facade design pattern to show available commands as simple 'interface'.
    
    Constructor parameters:
    catalog (LibraryCatalog): Catalog that does every method presented by interface.
    manager (ObserverManager): Manager for Observers awaiting for books.
    
    Parameters:
    catalog (LibraryCatalog): Catalog that does every method presented by interface.
    manager (ObserverManager): Manager for Observers awaiting for books.
    
    Methods:
    get_catalog() -> dict: Returns full catalog.
    get_next() -> str: Returns next book in catalog.
    add_book(book: Book) -> int: Adds book to catalog. Increases count and returns 1 if book already exists, otherwise returns 2.
    borrow_book(user: User, identify: int, manager: ObserverManager) -> int: Tries to find a book by its ID and declare one of copies as ordered by user. Decreases book count and returns 1 if user has not reached book limit and book is available, 0 if book is unavailable right now, -1 if user reached book limit, -2 if user already ordered this book or -3 if book does not exist. Informs ObserverManager to notify users.
    return_book(user: User, identify: int, manager: ObserverManager) -> int: Tries to find a book by its ID and return it to library. Increases book count, removes it from user's list and returns 1 if the book exists and user has it, -1 if user has no book borrowed, -2 if user has not borrowed this book or -3 if the book does not exist. Informs ObserverManager to notify users.
    update_borrow(user: User, identify: int) -> int: Tries to update book's status in user's list from "Ordered" to "Borrowed". Changes status and returns 1 if user has this book and it is "Ordered", -1 if the book is not "Ordered" or -2 if user does not have this book in its list.
    
    Why Facade? It allows to show available commands that are located in more advanced and complicated class. Here everything looks better and complex processing is hidden from view.
    """
    def __init__(self, catalog: LibraryCatalog, manager: ObserverManager):
        self.catalog = catalog
        self.manager = manager
        
    def add_book(self, book: Book) -> bool:
        return self.catalog.add_book(book)
        
    def show_catalog(self) -> dict:
        return self.catalog.get_catalog()
    
    def show_any_book(self) -> str:
        return self.catalog.get_next()
        
    def borrow_book(self, user: User, identify: int) -> int:
        return self.catalog.borrow_book(user, identify, self.manager)
    
    def return_book(self, user: User, identify: int) -> int:
        return self.catalog.return_book(user, identify, self.manager)

    def update_borrow(self, user: User, identify: int) -> int:
        return self.catalog.update_borrow(user, identify)
