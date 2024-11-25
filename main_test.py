from main import *
import os


cat = LibraryCatalog()
users = []
manager = ObserverManager()
interface = ActionInterface(cat, manager)
adapter = DataAdapter()


class Tester:
    def test_1_add_book(self):
        expect = 2
        for i in [Book("A", 0, 1999), Book("B", 1, 2002), Book("C", 2, 2004), Book("D", 3, 2020)]:
            got = cat.add_book(i)
            assert (expect == got)
        print(f"Test 1 - added 4 books.")

    def test_2_get_catalog(self):
        expect = cat.catalog
        got = cat.get_catalog()
        assert (expect == got)
        print(f"Test 2 - catalog shown")

    def test_3_singleton(self):
        temp = LibraryCatalog()
        expect = [True, True]
        got = [cat is temp, cat == temp]
        assert (expect == got)
        print(f"Test 3 - singleton")

    def test_4_iterator(self):
        expect = "C, 2004, id 2, count: 1/1"
        for i in range(7):
            got = cat.get_next()
        assert (expect == got)
        print(f"Test 4 - iterator")

    def test_5_factory_success(self):
        expect = 3
        users.append(UserFactory.create_user("student", "AAA"))
        users.append(UserFactory.create_user("teacher", "BBB"))
        users.append(UserFactory.create_user("librarian", "CCC"))
        got = len(users)
        assert (expect == got)
        print(f"Test 5 - factory created users")

    def test_6_factory_fail(self):
        expect = "Unknown user kind inserted."
        try:
            got = UserFactory.create_user("user", "A")
        except Exception as e:
            got = str(e)
        assert (expect == got)
        print(f"Test 6 - factory refused to create unknown user")

    def test_7_abstract_class(self):
        expect = "User is supposed to be an abstract class"
        try:
            got = User("A")
        except Exception as e:
            got = str(e)
        assert (expect == got)
        print(f"Test 7 - abstract class")

    def test_8_facade_add_copy_book(self):
        expect = 1
        got = interface.add_book(Book('D', 3, 2020))
        assert (expect == got)
        print(f"Test 8 - facade book copy")

    def test_9_facade_show_catalog(self):
        expect = cat.catalog
        got = interface.show_catalog()
        assert (expect == got)
        print(f"Test 9 - facade catalog shown")

    def test_10_facade_iterator(self):
        expect = "D, 2020, id 3, count: 2/2"
        got = interface.show_any_book()
        assert (expect == got)
        print(f"Test 10 - facade book shown")

    def test_11_facade_borrow_book(self):
        expect = 1
        got = interface.borrow_book(users[0], 3)
        assert (expect == got)
        print(f"Test 11 - facade book borrowed")

    def test_12_facade_borrow_book_fail(self):
        expect = -2
        got = interface.borrow_book(users[0], 3)
        assert (expect == got)
        print(f"Test 12 - facade refused to borrow same book")

    def test_13_facade_update_book(self):
        expect = ["Ordered", 1, "Borrowed"]
        got = []
        got.append(users[0].books[0][1])
        got.append(interface.update_borrow(users[0], 3))
        got.append(users[0].books[0][1])
        assert (expect == got)
        print(f"Test 13 - facade updated book status")

    def test_14_observers_empty(self):
        expect = []
        got = interface.manager.observers
        assert (expect == got)
        print(f"Test 14 - no observers yet")

    def test_15_observers_attach(self):
        expect = [0, 1, ['User BBB wishlisted book B, 2002, id 1.']]
        got = []
        interface.borrow_book(users[0], 1)
        got.append(interface.borrow_book(users[1], 1))
        got.append(len(interface.manager.observers))
        got.append(interface.manager.observers[-1].infos)
        assert (expect == got)
        print(f"Test 15 - observer attached")

    def test_16_observers_notify(self):
        expect = "User BBB - book B, 2002, id 1 is available."
        interface.return_book(users[0], 1)
        got = interface.manager.observers[-1].infos[-1]
        assert (expect == got)
        print(f"Test 16 - observer notified")

    def test_17_observers_deattach(self):
        expect = []
        interface.borrow_book(users[1], 1)
        got = interface.manager.observers[-1].books
        assert (expect == got)
        print(f"Test 17 - observer deattached - borrowed book")

    def test_18_adapter_xml(self):
        expect = 6
        f = open("test_xml.xml", "w")
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
        f.close()
        adapter.read(cat, "test_xml.xml")
        os.remove("test_xml.xml")
        got = len(cat.get_catalog())
        assert (expect == got)
        print(f"Test 18 - xml adapter")

    def test_19_adapter_csv(self):
        expect = 8
        f = open("test_csv.csv", "w")
        f.write("""name,id,year
G,6,2012
H,7,2002""")
        f.close()
        adapter.read(cat, "test_csv.csv")
        os.remove("test_csv.csv")
        got = len(cat.get_catalog())
        assert (expect == got)
        print(f"Test 19 - csv adapter")

    def test_20_adapter_json(self):
        expect = 9
        f = open("test_json.json", "w")
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
        assert (expect == got)
        print(f"Test 20 - json adapter")
