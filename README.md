# Flight Planner

A Python-based flight route planning system that finds optimal flight routes between cities based on different criteria: minimizing the number of flights, minimizing cost, or finding the best combination of both.

## Overview

This project implements a flight planning system that can calculate the best routes between cities considering various constraints such as time windows, layover requirements, and optimization goals.

## Features

The Flight Planner provides three distinct route optimization strategies:

1. **Least Flights, Earliest Arrival** - Finds routes with the minimum number of flights, and among those, selects the one with the earliest arrival time
2. **Cheapest Route** - Finds the route with the lowest total fare
3. **Least Flights, Cheapest** - Finds routes with the minimum number of flights, and among those, selects the one with the lowest cost

## Project Structure

```
├── flight.py       # Flight class definition
├── planner.py      # Planner class with route optimization algorithms
└── main.py         # Example usage and test cases
```

## Components

### Flight Class (`flight.py`)

Represents a single flight with the following attributes:
- `flight_no`: Unique flight identifier (0 to n-1)
- `start_city`: Origin city identifier (0 to m-1)
- `departure_time`: Departure time (non-negative integer)
- `end_city`: Destination city identifier (0 to m-1)
- `arrival_time`: Arrival time (non-negative integer)
- `fare`: Cost of the flight

### Planner Class (`planner.py`)

The main flight planning engine that includes:
- **Custom data structures**: MinHeap and HashMap implementations for efficient route searching
- **Route optimization methods**:
  - `least_flights_earliest_route(start_city, end_city, t1, t2)`
  - `cheapest_route(start_city, end_city, t1, t2)`
  - `least_flights_cheapest_route(start_city, end_city, t1, t2)`

## Constraints

- **Time Window**: Routes must depart after time `t1` and arrive before time `t2`
- **Layover Requirement**: Minimum 20 time units required between connecting flights
- **Valid Connections**: Each flight in the route must be reachable from the previous flight

## Usage

```python
from flight import Flight
from planner import Planner

# Define available flights
flights = [
    Flight(0, 0, 0, 1, 30, 50),      # City 0 to 1
    Flight(1, 0, 0, 3, 80, 200),     # City 0 to 3
    # ... more flights
]

# Create planner instance
flight_planner = Planner(flights)

# Find routes with different optimization strategies
route1 = flight_planner.least_flights_earliest_route(0, 4, 0, 300)
route2 = flight_planner.cheapest_route(0, 4, 0, 300)
route3 = flight_planner.least_flights_cheapest_route(0, 4, 0, 300)
```

## Example

The `main.py` file includes a complete example with 7 flights connecting 5 cities (0-4):

**Sample Network:**
- City 0 → City 1 (Flight 0: t=0-30, fare=50)
- City 0 → City 3 (Flight 1: t=0-80, fare=200)
- City 1 → City 2 (Flights 2-3)
- City 2 → City 4 (Flight 4)
- City 3 → City 4 (Flights 5-6)

**Results for routes from City 0 to City 4:**
- Least flights, earliest: 0→3→4 (2 flights, arrives t=150)
- Cheapest: 0→1→2→4 (fare=270)
- Least flights, cheapest: 0→3→4 (2 flights, fare=500)

## Running the Project

```bash
python main.py
```

Expected output:
```
Task 1 PASSED
Task 2 PASSED
Task 3 PASSED
```

## Algorithms

- **BFS (Breadth-First Search)**: Used for finding routes with the least number of flights
- **Dijkstra's Algorithm**: Used with custom priority queues for cost optimization and combined optimization strategies
- **Custom HashMap**: Hash-based storage for efficient graph representation and visited state tracking
- **Custom MinHeap**: Priority queue implementation for efficient extraction of minimum cost/flight routes

## Time Modeling

Time is modeled as non-negative integers starting from t=0 and extending to infinity. All time-based constraints use this simple integer representation.

## License

This project is provided as-is for educational and practical use.
