import unittest
from app.app import app, db
from app.models import User, Event, Ticket

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        # Create the application context
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        # Create the application context
        with app.app_context():
            db.drop_all()

    # User API Tests

    def test_view_events(self):
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)

    def test_book_ticket(self):
        # Create a test event
        event = Event(name='Test Event', event_type='offline', max_seats=100)
        db.session.add(event)
        db.session.commit()

        # Send a request to book a ticket
        response = self.app.post('/events/{}/book'.format(event.id), json={'user_id': 1})
        self.assertEqual(response.status_code, 201)

    def test_view_ticket(self):
        # Create a test user
        user = User(name='Test User')
        db.session.add(user)
        db.session.commit()

        # Create a test event
        event = Event(name='Test Event', event_type='offline', max_seats=100)
        db.session.add(event)
        db.session.commit()

        # Create a test ticket
        ticket = Ticket(user_id=user.id, event_id=event.id)
        db.session.add(ticket)
        db.session.commit()

        # Send a request to view the ticket
        response = self.app.get('/tickets/{}'.format(ticket.id))
        self.assertEqual(response.status_code, 200)

    def test_view_registered_events(self):
        # Create a test user
        user = User(name='Test User')
        db.session.add(user)
        db.session.commit()

        # Create test events
        event1 = Event(name='Event 1', event_type='offline')
        event2 = Event(name='Event 2', event_type='offline')
        db.session.add_all([event1, event2])
        db.session.commit()

        # Create test tickets for the user
        ticket1 = Ticket(user_id=user.id, event_id=event1.id)
        ticket2 = Ticket(user_id=user.id, event_id=event2.id)
        db.session.add_all([ticket1, ticket2])
        db.session.commit()

        # Send a request to view registered events
        response = self.app.get('/users/{}/events'.format(user.id))
        self.assertEqual(response.status_code, 200)

    # Admin API Tests

    def test_create_event(self):
        response = self.app.post('/create_event', json={'name': 'Test Event', 'event_type': 'offline', 'max_seats': 100})
        self.assertEqual(response.status_code, 201)

    def test_list_events(self):
        response = self.app.get('/list_events')
        self.assertEqual(response.status_code, 200)

    def test_update_event(self):
        # Create a test event
        event = Event(name='Test Event', event_type='offline', max_seats=100)
        db.session.add(event)
        db.session.commit()

        # Send a request to update the event
        response = self.app.put('/events/{}'.format(event.id), json={'name': 'Updated Event'})
        self.assertEqual(response.status_code, 200)

    def test_view_event_summary(self):
        # Create a test event
        event = Event(name='Test Event', event_type='offline', max_seats=100)
        db.session.add(event)
        db.session.commit()

        # Send a request to view the event summary
        response = self.app.get('/events/{}/summary'.format(event.id))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

