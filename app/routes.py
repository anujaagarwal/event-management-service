from flask import jsonify, request
from app import app, db
from models import Event
import controllers

app.add_url_rule('/events', 'get_events', controllers.get_events, methods=['GET'])
app.add_url_rule('/events/<event_id>/book', 'book_event', controllers.book_event, methods=['POST'])
app.add_url_rule('/tickets/<ticket_id>', 'view_ticket', controllers.view_ticket, methods=['GET'])
app.add_url_rule('/users/<user_id>/events', 'view_registered_events', controllers.view_registered_events, methods=['GET'])


# Admin Functionality:
app.add_url_rule('/create_event', 'create_event', controllers.create_event, methods=['POST'])
app.add_url_rule('/list_events', 'list_events', controllers.list_events, methods=['GET'])
app.add_url_rule('/events/<event_id>', 'update_event', controllers.update_event, methods=['PUT'])
app.add_url_rule('/events/<event_id>/summary', 'view_event_summary', controllers.view_event_summary, methods=['GET'])


