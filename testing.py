import os
import unittest

from noyo_run import app, db
from noyo_run import Person

TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        project_dir = os.path.abspath(os.path.dirname(__file__))
        database_file = "sqlite:///{}".format(os.path.join(project_dir, "test.db"))
        app.config["SQLALCHEMY_DATABASE_URI"] = database_file
        self.app = app.test_client()
        db.create_all()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_html(self):
        response = self.app.get('/noyo/person/')
        assert  b'<doctype html>' in response.data
        self.assertEqual(response.status_code, 200)

    def test_json(self):
        response = self.app.get('/noyo/all_persons/')
        assert 'json' in response.content_type
        self.assertEqual(response.status_code, 200)

    def test_db(self):
        #Create person entries
        user1 = Person("JohnD", "John", "", "Doe", "jdoe@jdoe.com", "22")
        db.session.add(user1)
        db.session.commit()

        user2 = Person("sthakkar", "Shraddha", "B", "Thakkar", "shraddhat28@gmail.com", "28")
        db.session.add(user2)
        db.session.commit()

        user3 = Person("Noyo_1", "firstName", "", "lastName", "name@gmail.com", "50")
        db.session.add(user3)
        db.session.commit()

        #Check that all person entries exist
        self.assertEqual(len(Person.query.all()), 3)

        #Check fetch_person using userId
        response = self.app.get('/noyo/person/sthakkar/')
        self.assertEqual(response.status_code, 200)
        print (response.data)
        assert  b'userId' in response.data
        assert  b'firstName' in response.data
        assert  b'middleName' in response.data
        assert  b'lastName' in response.data
        assert  b'email' in response.data
        assert  b'age' in response.data

        #Check fetch_versioned_person using userId and version
        response = self.app.get('/noyo/person/sthakkar/0/')
        self.assertEqual(response.status_code, 200)
        assert  b'sthakkar' in response.data

        response = self.app.get('/noyo/person/sthakkar/11/')
        assert  b'does not exist' in response.data

        #Check delete_person using userId
        response = self.app.get('/noyo/person/Noyo_1/')
        self.assertEqual(response.status_code, 200)
        assert  "Noyo_1" in str(response.data)
        db.session.delete(user3)
        db.session.commit()
        response = self.app.get('/noyo/person/Noyo_1/')
        assert  b'does not exist' in response.data

        #Check person entries exist
        response = self.app.get('/noyo/all_persons/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Person.query.all()), 2)

    def test_update_html(self):
        response = self.app.get('/noyo/person/update/')
        assert  b'<doctype html>' in response.data
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
