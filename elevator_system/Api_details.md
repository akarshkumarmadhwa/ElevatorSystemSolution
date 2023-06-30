## Model Wise API Endpoints

## Elevator System

Elevator system Model. Equivalent to a building containing a number of elevators Also contains the default ID parameter assigned by django as a primary key. Used to make the project compatible with multiple elevator systems

### GET elevator/elevator_system/
View all the elevator systems

#### Query Parameter
```
{elevator-system-id} = ID of the elevator system (elev_sys_id) in order to view for particular system -> Optional
```

#### Response Example
```
200
[
  {
    "id": 0,
    "system_name": "string",
    "max_floor": 0,
    "number_of_elevators": 0
  }
]
```


### POST elevator/elevator_system/
Create a new elevator system.

#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
system_name         - required  -----> string (System name) [ 1 .. 20 ] characters
max_floor           - required  ----->integer (Max floor)
number_of_elevators - required  -----> integer (Number of elevators)
```

#### Response Example
```
201 Accepted
```

## Elevator
Elevator object model. Represents a single elevator that can move up and down. It is always a part of an entire elevator system. So elevator system is assigned as foreignkey.

### GET elevator/
Given an elevator system list all the elevators and their status.

#### Query Parameter
```
{elevator-system-id} = ID of the elevator system (sys_id) -> Require
```

#### Response Example
```
200
[
  {
    "id": 0,
    "elevator_number": 0,
    "current_floor": 0,
    "is_operational": true,
    "is_door_open": true,
    "running_status": 1,
    "elevator_system": 0
  }
]

```

### GET elevator/
Get details of a specific elevator, given its elevator system id and elevator number with URL

#### Query Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = Elevator unique number of the elevator in order to view details of particular elevator (elev_num)
```

#### Response Example
```
200
{
  "id": 0,
  "elevator_number": 0,
  "current_floor": 0,
  "is_operational": true,
  "is_door_open": true,
  "running_status": 1,
  "elevator_system": 0
}

```

### PUT elevator/
Update details of a specific elevator, open/close Door, mark elevator as operational.

#### Query Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = Elevator unique number of the particular elevator (elev_num)
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
current_floor	    - integer (Current floor)
is_operational	  - boolean (Is operational)
is_door_open	    - boolean (Is door open)
running_status	  - integer (Running status)Expected numbers : (1 , 0 , -1)
```
#### Response Example
```
202 Accepted
```

### GET elevator/destination/
Fetch the next destination floor for a given elevator

#### Query Parameter
```
{elevator-system-id} = ID of the elevator system (elev_num)
{elevator-number} = unique number of the elevator (sys_id)
```

#### Response Example
```
200
{
    "moving_up": True/False,
    "moving_down": True/False,   
    "running" : True/False,
    "destination_floor" : Number representing the next destination / String representing the current status if not running,
    "comment": "The Elevator is not running currently/No pending requests"
}

```

## Elevator Request
User request targeted to a specific elevator. This can be improved further using model managers  to clean the invalid requests like request elevator in negative floor greater than maximum floor request an elevator that doesn't exist.

### GET elevator/ele_sys_req/
List all the requests for a given elevator.

#### Query Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Params
```
is_active ----> False/0 ---> All the processed requests by the elevator(False is case insensitive)
is_active ----> True/1 ---> All the pending requests by the elevator(True is case insensitive)
```
#### Response Example
```
200
[
  {
    "id": 0,
    "requested_floor": 0,
    "destination_floor": 0,
    "request_time": "2019-08-24T14:15:22Z",
    "is_active": true,
    "elevator": 0
  }
]
```
### POST elevator/ele_sys_req/
Create a new request for a specific elevator, given its elevator system and elevator number with URL. The inputs of requested and destinatiom floor is sent with the form-data.

#### Query Parameter
```
{elevator-system-id} = ID of the elevator system
{elevator-number} = unique number of the elevator
```
#### Request Body Schema
```
REQUEST BODY SCHEMA: application/json
requested_floor       - required integer 
destination_floor	    - required integer
```
#### Response Example
```
201 Accepted
```