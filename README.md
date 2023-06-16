
# Event Management Service API Documentation

The Event Management Service provides an API for managing events, allowing users to view events, book tickets, and perform administrative tasks. This documentation provides details on the available endpoints and their functionalities.

## Base URL

The base URL for accessing the Event Management Service API is: `http://localhost:5000`

## Authentication

Authentication is not required to access the endpoints of this API.

## Endpoints

### Get All Events

Retrieve a list of all events.

- **URL**: `/events`
- **Method**: GET
- **Response**: JSON

#### Response

```json
[
  {
    "id": 1,
    "name": "Event 1",
    "description": "Event 1 description",
    "date": "2023-06-15",
    "location": "Event 1 location",
    "type": "offline"
  },
  {
    "id": 2,
    "name": "Event 2",
    "description": "Event 2 description",
    "date": "2023-06-20",
    "location": "Event 2 location",
    "type": "online"
  },
  ...
]
```

### Create Event

Create a new event.

- **URL**: `/create_event`
- **Method**: POST
- **Request**: JSON
- **Response**: JSON

#### Request Body

```json
{
  "name": "New Event",
  "description": "New Event description",
  "date": "2023-06-25",
  "location": "New Event location",
  "type": "offline"
}
```

#### Response

```json
{
  "id": 3,
  "name": "New Event",
  "description": "New Event description",
  "date": "2023-06-25",
  "location": "New Event location",
  "type": "offline"
}
```

### Get Event

Retrieve details of a specific event.

- **URL**: `/events/{event_id}`
- **Method**: GET
- **Response**: JSON

#### Response

```json
{
  "id": 1,
  "name": "Event 1",
  "description": "Event 1 description",
  "date": "2023-06-15",
  "location": "Event 1 location",
  "type": "offline"
}
```

### Update Event

Update details of a specific event.

- **URL**: `/events/{event_id}`
- **Method**: PUT
- **Request**: JSON
- **Response**: JSON

#### Request Body

```json
{
  "name": "Updated Event",
  "description": "Updated Event description",
  "date": "2023-06-15",
  "location": "Updated Event location",
  "type": "offline"
}
```

#### Response

```json
{
  "id": 1,
  "name": "Updated Event",
  "description": "Updated Event description",
  "date": "2023-06-15",
  "location": "Updated Event location",
  "type": "offline"
}
```

### Get Event Summary

Retrieve a summary of a specific event.

- **URL**: `/events/{event_id}/summary`
- **Method**: GET
- **Response**: JSON

#### Response

```json
{
  "id": 1,
  "name": "Event 1",
  "date": "2023-06-15",
  "total_seats": 100,
  "available_seats": 80,
  "booking_open_window": {
    "start_time": "2023-06-01 00:00:00",
    "end_time": "2023-06-14 23:59:59"
  }
}
```

### Book Tickets

Book tickets for an event.

- **URL**: `/events/{event_id}/book`
- **Method**: POST
- **Request**: JSON
- **Response**: JSON

#### Request Body

```json
{
  "user_id": 1,
  "quantity": 2
}
```

- `user_id` (integer): The ID of the user booking the tickets.
- `quantity` (integer): The number of tickets to book.

#### Response

```json
{
  "booking_id": 1,
  "event_id": 1,
  "user_id": 1,
  "quantity": 2,
  "booking_time": "2023-06-14T10:30:00Z"
}
```

### View Tickets

View the tickets booked by a user.

- **URL**: `/users/{user_id}/tickets`
- **Method**: GET
- **Response**: JSON

#### Response

```json
[
  {
    "ticket_id": 1,
    "event_id": 1,
    "event_name": "Event 1",
    "event_date": "2023-06-15",
    "event_location": "Event 1 location",
    "quantity": 2
  },
  {
    "ticket_id": 2,
    "event_id": 2,
    "event_name": "Event 2",
    "event_date": "2023-06-20",
    "event_location": "Event 2 location",
    "quantity": 1
  }
]
```

## Error Responses

If an error occurs while processing a request, the API will respond with an appropriate error message in the JSON format. The response will include an HTTP status code indicating the type of error.

Here are some common error responses:

### 404 Not Found

Returned when the requested resource is not found.

```json
{
  "message": "Event not found"
}
```

### 400 Bad Request

Returned when the request is invalid or missing required parameters.

```json
{
  "message": "Invalid request body"
}
```

### 500 Internal Server Error

Returned when an unexpected error occurs on the server.

```json
{
  "message": "Internal server error"
}
```

That concludes the API documentation for the Event Management Service. Make sure to refer to this documentation when using the API endpoints to ensure proper usage and understanding of the available functionalities.

If you have any further questions or need assistance, feel free to reach out.
