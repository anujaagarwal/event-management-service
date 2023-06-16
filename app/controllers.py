import datetime
from app import app, db
from flask import jsonify, request
from models import User, Event, Ticket

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.date).all()
    event_data = []
    for event in events:
        event_data.append({
            'id': event.id,
            'name': event.name,
            'event_type': event.event_type,
            'max_seats': event.max_seats,
            'date': event.date.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(event_data)

@app.route('/events/<event_id>/book', methods=['POST'])
def book_event(event_id):
    user_id = request.json.get('user_id')
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    # Check if booking window is valid
    current_time = datetime.utcnow()
    if current_time < event.booking_window_start or current_time > event.booking_window_end:
        return jsonify({'message': 'Booking window has closed'}), 400

    # Check if event has available seats
    booked_seats = Ticket.query.filter_by(event_id=event_id).count()
    if booked_seats >= event.max_seats:
        return jsonify({'message': 'No seats available for this event'}), 400

    # Create a new ticket
    ticket = Ticket(user_id=user_id, event_id=event_id)
    db.session.add(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket booked successfully'})


# User Functionality: View Ticket
@app.route('/tickets/<ticket_id>', methods=['GET'])
def view_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({'message': 'Ticket not found'}), 404

    user = User.query.get(ticket.user_id)
    event = Event.query.get(ticket.event_id)

    ticket_data = {
        'id': ticket.id,
        'user_id': ticket.user_id,
        'user_name': user.name,
        'event_id': ticket.event_id,
        'event_name': event.name,
        'event_type': event.event_type,
        'event_date': event.date.strftime('%Y-%m-%d %H:%M:%S')
    }

    return jsonify(ticket_data)

# User Functionality: View Registered Events Sorted by Date
@app.route('/users/<user_id>/events', methods=['GET'])
def view_registered_events(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    tickets = Ticket.query.filter_by(user_id=user_id).all()

    # Sort the tickets by event date in ascending order
    sorted_tickets = sorted(tickets, key=lambda t: t.event.date)

    event_data = []
    for ticket in sorted_tickets:
        event = ticket.event
        event_data.append({
            'id': event.id,
            'name': event.name,
            'event_type': event.event_type,
            'date': event.date.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(event_data)

# Admin Functionality: Create Event
@app.route('/create_event', methods=['POST'])
def create_event():
    name = request.json.get('name')
    event_type = request.json.get('event_type')
    max_seats = request.json.get('max_seats')
    booking_window_start = request.json.get('booking_window_start')
    booking_window_end = request.json.get('booking_window_end')

    new_event = Event(
        name=name,
        event_type=event_type,
        max_seats=max_seats,
        booking_window_start=booking_window_start,
        booking_window_end=booking_window_end
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event created successfully'}), 201

# Admin Functionality: List Events
@app.route('/events', methods=['GET'])
def list_events():
    events = Event.query.all()

    event_data = []
    for event in events:
        event_data.append({
            'id': event.id,
            'name': event.name,
            'event_type': event.event_type,
            'max_seats': event.max_seats,
            'date': event.date.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(event_data)

# Admin Functionality: Update Event
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    event.name = request.json.get('name', event.name)
    event.event_type = request.json.get('event_type', event.event_type)
    event.max_seats = request.json.get('max_seats', event.max_seats)
    event.booking_window_start = request.json.get('booking_window_start', event.booking_window_start)
    event.booking_window_end = request.json.get('booking_window_end', event.booking_window_end)

    db.session.commit()

    return jsonify({'message': 'Event updated successfully'})

# Admin Functionality: View Event Summary
@app.route('/events/<event_id>/summary', methods=['GET'])
def view_event_summary(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    booked_seats = Ticket.query.filter_by(event_id=event_id).count()
    available_seats = event.max_seats - booked_seats

    return jsonify({
        'name': event.name,
        'event_type': event.event_type,
        'max_seats': event.max_seats,
        'booked_seats': booked_seats,
        'available_seats': available_seats
    })