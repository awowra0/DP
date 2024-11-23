from main import *


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
test_manager = ObserverManager()
test_interface = ActionInterface(a, test_manager)
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
print(f"Checked observers (should be empty): {test_interface.manager.observers}")
test_user_b = UserFactory.create_user("teacher", "TUVW")
print(f"Called Facade borrow_book: {test_interface.borrow_book(test_user, 1)}")
print(f"Called Facade borrow_book for unavailable book: {test_interface.borrow_book(test_user_b, 1)}")
try:
    print(f"Checked observers (should not be empty): {len(test_interface.manager.observers)}")
    print(f"Checked last observer's notifications: {test_interface.manager.observers[-1].infos}")
except Exception as e:
    print(f"Observer test failed: {e}")
