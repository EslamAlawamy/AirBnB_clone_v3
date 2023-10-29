#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import inspect
import os
import unittest
from sqlalchemy.orm import scoped_session
import pep8
from models.engine import db_storage
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(
                func[1].__doc__, None,
                f"{func[0]} method needs a docstring"
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                f"{func[0]} method needs a docstring"
            )


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db',
    'Not a file storage'
)
class TestDBStorage(unittest.TestCase):
    """Test cases for db storage"""
    def setUp(self):
        """setup method"""
        self.session = storage._DBStorage__session
        texas = State()
        texas.name = 'Texas'
        austin = City()
        austin.name = 'Austin'
        austin.state_id = texas.id
        dallas = City()
        dallas.name = 'Dallas'
        dallas.state_id = texas.id
        self.objs = {'states': [texas], 'cities': [austin, dallas]}

        for obj in self.objs['states'] + self.objs['cities']:
            self.session.add(obj)
        self.session.commit()

    def tearDown(self):
        """tearDown method"""
        for obj in self.objs['states'] + self.objs['cities']:
            self.session.delete(obj)
        self.session.commit()

    def test_all(self):
        """Test all"""
        objs_from_db = storage.all()
        self.assertIsInstance(objs_from_db, dict)
        self.assertEqual(
            sorted(list(map(
                lambda obj: obj.id, self.objs['states'] + self.objs['cities']
            ))),
            sorted(list(map(lambda obj: obj.id, objs_from_db.values())))
        )

    def test_filtered_all(self):
        """Test filtered all"""
        cities = storage.all(City)
        self.assertEqual(
            sorted(list(map(
                lambda obj: obj.id, self.objs['cities']
            ))),
            sorted(list(map(lambda obj: obj.id, cities.values())))
        )

    def test_new(self):
        """Test new"""
        city = City()
        city.name = 'Houston'
        city.state_id = self.objs['states'][0].id
        self.objs['cities'].append(city)
        storage.new(city)
        self.session.commit()
        cities = self.session.query(City)
        self.assertEqual(
            sorted(list(map(
                lambda obj: obj.id, self.objs['cities']
            ))),
            sorted(list(map(lambda obj: obj.id, cities)))
        )

    def test_save(self):
        """Test save"""
        self.session.delete(self.objs['cities'].pop())
        storage.save()
        cities = self.session.query(City)
        self.assertEqual(
            sorted(list(map(
                lambda obj: obj.id, self.objs['cities']
            ))),
            sorted(list(map(lambda obj: obj.id, cities)))
        )

    def test_delete(self):
        """Test delete"""
        storage.delete(self.objs['cities'].pop())
        self.session.commit()
        cities = self.session.query(City)
        self.assertEqual(
            sorted(list(map(
                lambda obj: obj.id, self.objs['cities']
            ))),
            sorted(list(map(lambda obj: obj.id, cities)))
        )

    def test_reload(self):
        """Test reload"""
        storage.reload()
        self.assertIsInstance(storage._DBStorage__session, scoped_session)
        self.assertNotEqual(self.session, storage._DBStorage__session)
        storage._DBStorage__session.close()
        storage._DBStorage__session = self.session

    def test_get(self):
        """Test get"""
        self.assertEqual(
            storage.all()[f'State.{self.objs["states"][0].id}'],
            storage.get(State, self.objs["states"][0].id)
        )

    def test_count(self):
        """Test count"""
        self.assertEqual(
            len(storage.all()),
            storage.count()
        )
        self.assertEqual(
            len(storage.all(City)),
            storage.count(City)
        )
