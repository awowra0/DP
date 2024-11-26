"""
Test file for main.py; use with pytest.
"""
import os
from main import LibraryCatalog, ObserverManager, ActionInterface, \
                 DataAdapter, Book, UserFactory, User


cat = LibraryCatalog()
users = []
manager = ObserverManager()
interface = ActionInterface(cat, manager)
adapter = DataAdapter()
factory = UserFactory()


class Tester:
    """
    Class running tests. Use with pytest.
    """
    def test_1_add_book(self):
        """
        Test 1.
        """
        expect = 2
        for i in [Book("A", 0, 1999), Book("B", 1, 2002), Book("C", 2, 2004), Book("D", 3, 2020)]:
            got = cat.add_book(i)
            assert expect == got
        print("Test 1 - added 4 books.")

    def test_2_get_catalog(self):
        """
        Test 2.
        """
        expect = cat.catalog
        got = cat.get_catalog()
        assert expect == got
        print("Test 2 - catalog shown")

    def test_3_singleton(self):
        """
        Test 3.
        """
        temp = LibraryCatalog()
        expect = [True, True]
        got = [cat is temp, cat == temp]
        assert expect == got
        print("Test 3 - singleton")

    def test_4_iterator(self):
        """
        Test 4.
        """
        expect = "C, 2004, id 2, count: 1/1"
        for _ in range(7):
            got = cat.get_next()
        assert expect == got
        print("Test 4 - iterator")

    def test_5_factory_success(self):
        """
        Test 5.
        """
        expect = 3
        users.append(factory.create_user("student", "AAA"))
        users.append(factory.create_user("teacher", "BBB"))
        users.append(factory.create_user("librarian", "CCC"))
        got = len(users)
        assert expect == got
        print("Test 5 - factory created users")

    def test_6_factory_fail(self):
        """
        Test 6.
        """
        expect = "Unknown user kind inserted."
        try:
            got = factory.create_user("user", "A")
        except TypeError as e:
            got = str(e)
        assert expect == got
        print("Test 6 - factory refused to create unknown user")

    def test_7_abstract_class(self):
        """
        Test 7.
        """
        expect = "User is supposed to be an abstract class"
        try:
            got = User("A")
        except NotImplementedError as e:
            got = str(e)
        assert expect == got
        print("Test 7 - abstract class")

    def test_8_facade_add_copy_book(self):
        """
        Test 8.
        """
        expect = 1
        got = interface.add_book(Book('D', 3, 2020))
        assert expect == got
        print("Test 8 - facade book copy")

    def test_9_facade_show_catalog(self):
        """
        Test 9.
        """
        expect = cat.catalog
        got = interface.show_catalog()
        assert expect == got
        print("Test 9 - facade catalog shown")

    def test_10_facade_iterator(self):
        """
        Test 10.
        """
        expect = "D, 2020, id 3, count: 2/2"
        got = interface.show_any_book()
        assert expect == got
        print("Test 10 - facade book shown")

    def test_11_facade_borrow_book(self):
        """
        Test 11.
        """
        expect = 1
        got = interface.borrow_book(users[0], 3)
        assert expect == got
        print("Test 11 - facade book borrowed")

    def test_12_facade_borrow_book_fail(self):
        """
        Test 12.
        """
        expect = -2
        got = interface.borrow_book(users[0], 3)
        assert expect == got
        print("Test 12 - facade refused to borrow same book")

    def test_13_facade_update_book(self):
        """
        Test 13.
        """
        expect = ["Ordered", 1, "Borrowed"]
        got = []
        got.append(users[0].books[0][1])
        got.append(interface.update_borrow(users[0], 3))
        got.append(users[0].books[0][1])
        assert expect == got
        print("Test 13 - facade updated book status")

    def test_14_observers_empty(self):
        """
        Test 14.
        """
        expect = []
        got = interface.manager.observers
        assert expect == got
        print("Test 14 - no observers yet")

    def test_15_observers_attach(self):
        """
        Test 15.
        """
        expect = [0, 1, ['User BBB wishlisted book B, 2002, id 1.']]
        got = []
        interface.borrow_book(users[0], 1)
        got.append(interface.borrow_book(users[1], 1))
        got.append(len(interface.manager.observers))
        got.append(interface.manager.observers[-1].infos)
        assert expect == got
        print("Test 15 - observer attached")

    def test_16_observers_notify(self):
        """
        Test 16.
        """
        expect = "User BBB - book B, 2002, id 1 is available."
        interface.return_book(users[0], 1)
        got = interface.manager.observers[-1].infos[-1]
        assert expect == got
        print("Test 16 - observer notified")

    def test_17_observers_deattach(self):
        """
        Test 17.
        """
        expect = []
        interface.borrow_book(users[1], 1)
        got = interface.manager.observers[-1].books
        assert expect == got
        print("Test 17 - observer deattached - borrowed book")

    def test_18_adapter_xml(self):
        """
        Test 18.
        """
        expect = 6
        with open("test_xml.xml", "w") as f:
            f.write("""<?xml version="1.0"?>
    <data>
        <book>
            <name>E</name>
            <id>4</id>
            <year>1999</year>
        </book>
        <book>
            <name>F</name>
            <id>5</id>
            <year>2009</year>
        </book>
    </data>""")
        adapter.read(cat, "test_xml.xml")
        os.remove("test_xml.xml")
        got = len(cat.get_catalog())
        assert expect == got
        print("Test 18 - xml adapter")

    def test_19_adapter_csv(self):
        """
        Test 19.
        """
        expect = 8
        with open("test_csv.csv", "w") as f:
            f.write("""name,id,year
G,6,2012
H,7,2002""")
        adapter.read(cat, "test_csv.csv")
        os.remove("test_csv.csv")
        got = len(cat.get_catalog())
        assert expect == got
        print("Test 19 - csv adapter")

    def test_20_adapter_json(self):
        """
        Test 20.
        """
        expect = 9
        with open("test_json.json", "w") as f:
            f.write("""{
  "books": [
    {
      "name": "I",
      "id": 8,
      "year": 2016
    },
    {
      "name": "H",
      "id": 7,
      "year": 2002
    }
  ]
}""")
        f.close()
        adapter.read(cat, "test_json.json")
        os.remove("test_json.json")
        got = len(cat.get_catalog())
        assert expect == got
        print("Test 20 - json adapter")
