from main import *


class Tester():
    def __init__(self):
        self.cat = LibraryCatalog()
        self.users = []
        self.manager = ObserverManager()
        self.interface = ActionInterface(self.cat, self.manager)
        
    def start_tests(self):
        self.test_1_add_book()
        self.test_2_get_catalog()
        self.test_3_singleton()
        self.test_4_iterator()
        self.test_5_factory_success()
        self.test_6_factory_fail()
        self.test_7_abstract_class()
        self.test_8_facade_add_copy_book()
        self.test_9_facade_show_catalog()
        self.test_10_facade_iterator()
        self.test_11_facade_borrow_book()
        self.test_12_facade_borrow_book_fail()
        self.test_13_facade_update_book()
        self.test_14_observers_empty()
        self.test_15_observers_attach()
        self.test_16_observers_notify()
        self.test_17_observers_deattach()
        print("Tests finished.")
    
    def test_1_add_book(self):
        expect = 2
        for i in [Book("A", 0, 1999), Book("B", 1, 2002), Book("C", 2, 2004), Book("D", 3, 2020)]:
            got = self.cat.add_book(i)
            assert (expect==got)
        print(f"Test 1 - added 4 books.")
    
    def test_2_get_catalog(self):
        expect = self.cat.catalog
        got = self.cat.get_catalog()
        assert (expect==got)
        print(f"Test 2 - catalog shown")
        
    def test_3_singleton(self):
        temp = LibraryCatalog()
        expect = [True, True]
        got = [self.cat is temp, self.cat == temp]
        assert (expect==got)
        print(f"Test 3 - singleton")
        
    def test_4_iterator(self):
        expect = "C, 2004, id 2, count: 1/1"
        for i in range(7):
            got = self.cat.get_next()
        assert (expect==got)
        print(f"Test 4 - iterator")
        
    def test_5_factory_success(self):
        expect = 3
        self.users.append(UserFactory.create_user("student", "AAA"))
        self.users.append(UserFactory.create_user("teacher", "BBB"))
        self.users.append(UserFactory.create_user("librarian", "CCC"))
        got = len(self.users)
        assert (expect==got)
        print(f"Test 5 - factory created users")
    
    def test_6_factory_fail(self):
        expect = "Unknown user kind inserted."
        try:
            got = UserFactory.create_user("user", "A")
        except Exception as e:
            got = str(e)
        assert (expect==got)
        print(f"Test 6 - factory refused to create unknown user")
    
    def test_7_abstract_class(self):
        expect = "User is supposed to be an abstract class"
        try:
            got = User("A")
        except Exception as e:
            got = str(e)
        assert (expect==got)
        print(f"Test 7 - abstract class")
        
    def test_8_facade_add_copy_book(self):
        expect = 1
        got = self.interface.add_book(Book('D', 3, 2020))
        assert (expect==got)
        print(f"Test 8 - facade book copy")
        
    def test_9_facade_show_catalog(self):
        expect = self.cat.catalog
        got = self.interface.show_catalog()
        assert (expect==got)
        print(f"Test 9 - facade catalog shown")
        
    def test_10_facade_iterator(self):
        expect = "D, 2020, id 3, count: 2/2"
        got = self.interface.show_any_book()
        assert (expect==got)
        print(f"Test 10 - facade book shown")
        
    def test_11_facade_borrow_book(self):
        expect = 1
        got = self.interface.borrow_book(self.users[0], 3)
        assert (expect==got)
        print(f"Test 11 - facade book borrowed")
        
    def test_12_facade_borrow_book_fail(self):
        expect = -2
        got = self.interface.borrow_book(self.users[0], 3)
        assert (expect==got)
        print(f"Test 12 - facade refused to borrow same book")
        
    def test_13_facade_update_book(self):
        expect = ["Ordered", 1, "Borrowed"]
        got = []
        got.append(self.users[0].books[0][1])
        got.append(self.interface.update_borrow(self.users[0], 3))
        got.append(self.users[0].books[0][1])
        assert (expect==got)
        print(f"Test 13 - facade updated book status")
        
    def test_14_observers_empty(self):
        expect = []
        got = self.interface.manager.observers
        assert (expect==got)
        print(f"Test 14 - no observers yet")
        
    def test_15_observers_attach(self):
        expect = [0, 1, ['User BBB wishlisted book B, 2002, id 1.']]
        got = []
        self.interface.borrow_book(self.users[0], 1)
        got.append(self.interface.borrow_book(self.users[1], 1))
        got.append(len(self.interface.manager.observers))
        got.append(self.interface.manager.observers[-1].infos)
        assert (expect==got)
        print(f"Test 15 - observer attached")
        
    def test_16_observers_notify(self):
        expect = "User BBB - book B, 2002, id 1 is available."
        self.interface.return_book(self.users[0], 1)
        got = self.interface.manager.observers[-1].infos[-1]
        assert (expect==got)
        print(f"Test 16 - observer notified")
        
    def test_17_observers_deattach(self):
        expect = []
        self.interface.borrow_book(self.users[1], 1)
        got = self.interface.manager.observers[-1].books
        assert (expect==got)
        print(f"Test 17 - observer deattached - borrowed book")
        

if __name__ == "__main__":
    a = Tester()
    a.start_tests()
