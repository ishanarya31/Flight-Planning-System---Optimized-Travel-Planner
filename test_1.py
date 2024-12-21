from flight import Flight
from planner import Planner

def test_complex_dense_network():
    """
    Test with a dense network of flights between 5 cities with multiple possible routes.
    Cities are: 0 (New York), 1 (Chicago), 2 (Denver), 3 (Los Angeles), 4 (Seattle)
    Test cases focus on finding routes with fewest flights and earliest arrival.
    Returns empty list [] when no route is found.
    """
    
    flights = [
        # Direct flights from New York (0)
        Flight(1, 0, 0, 1, 120, 300),      # NY -> Chicago: 0-120
        Flight(2, 0, 60, 1, 180, 250),     # NY -> Chicago: 60-180
        Flight(3, 0, 0, 3, 360, 800),      # NY -> LA: 0-360 (direct but long)
        Flight(4, 0, 0, 2, 180, 500),      # NY -> Denver: 0-180
        
        # Connections through Chicago (1)
        Flight(5, 1, 140, 3, 300, 200),    # Chicago -> LA: 140-300 (faster path)
        Flight(6, 1, 200, 3, 360, 180),    # Chicago -> LA: 200-360
        
        # Connections through Denver (2)
        Flight(7, 2, 200, 3, 380, 200),    # Denver -> LA: 200-380
        
        # Some return flights
        Flight(8, 1, 400, 0, 520, 300),    # Chicago -> NY: 400-520
        Flight(9, 3, 400, 0, 760, 800),    # LA -> NY: 400-760
        
        # Late flights
        Flight(10, 0, 500, 3, 860, 700),   # NY -> LA: 500-860 (late direct)

        Flight(11, 2, 200, 3, 290, 100)    # Denver -> LA: 200-290
    ]
    
    planner = Planner(flights)
    
    test_scenarios = [
        # Basic direct flight test
        {
            "start": 0, "end": 1, "t1": 0, "t2": 1000,
            "expected_flights": 1,
            "expected_flight_numbers": [1],  # Should take first direct flight
            "description": "NY to Chicago - Should take earliest direct flight"
        },
        
        # Multi-hop vs Direct comparison
        {
            "start": 0, "end": 3, "t1": 0, "t2": 1000,
            "expected_flights": 1,
            "expected_flight_numbers": [3],  # Should take direct flight even if longer
            "description": "NY to LA - Should take direct flight over multi-hop"
        },
        
        # Time window forcing specific route
        {
            "start": 0, "end": 3, "t1": 0, "t2": 350,
            "expected_flights": 2,
            "expected_flight_numbers": [4, 11],  # Must go through Denver due to time constraint
            "description": "NY to LA - Time window forces route through Denver over the route through Chicago"
        },
        
        # Testing buffer time constraints
        {
            "start": 0, "end": 3, "t1": 0, "t2": 1000,
            "expected_flights": 1,
            "expected_flight_numbers": [3],  # Direct flight is better than tight connections
            "description": "NY to LA - Direct flight vs connections with buffer time"
        },
        
        # empty list cases
        {
            "start": 0, "end": 0, "t1": 0, "t2": 1000,
            "expected_flights": 0,
            "expected_flight_numbers": [],
            "description": "Same city - Should return empty list"
        },
        {
            "start": 0, "end": 3, "t1": 0, "t2": 100,
            "expected_flights": 0,
            "expected_flight_numbers": [],
            "description": "Impossible time window"
        },
    ]
    
    print("\nRunning complex network test scenarios...")
    for scenario in test_scenarios:
        route = planner.least_flights_earliest_route(
            scenario["start"], 
            scenario["end"], 
            scenario["t1"], 
            scenario["t2"]
        )
        
        print(f"\nScenario: {scenario['description']}")
        print(f"From City {scenario['start']} to City {scenario['end']}, "
              f"Time window: [{scenario['t1']}, {scenario['t2']}]")
        
        try:
            # Check empty list cases
            if scenario["expected_flights"] == 0:
                assert isinstance(route, list) and len(route) == 0, \
                    f"Expected empty list, but got {route}"
                print("✅ Correctly returned empty list")
                continue
            
            # Validate route exists and has correct length
            assert isinstance(route, list) and len(route) > 0, \
                f"Expected route with {scenario['expected_flights']} flights, but got empty list"
            assert len(route) == scenario["expected_flights"], \
                f"Expected {scenario['expected_flights']} flights, but got {len(route)}"
            
            # Validate correct flights were chosen
            actual_flight_numbers = [f.flight_no for f in route]
            assert actual_flight_numbers == scenario["expected_flight_numbers"], \
                f"Expected flights {scenario['expected_flight_numbers']}, but got {actual_flight_numbers}"
            
            # Validate route continuity and buffer time
            for i in range(len(route) - 1):
                assert route[i].end_city == route[i + 1].start_city, \
                    f"Discontinuous route: Flight {route[i].flight_no} ends at {route[i].end_city} " \
                    f"but next flight starts from {route[i + 1].start_city}"
                
                buffer = route[i + 1].departure_time - route[i].arrival_time
                assert buffer >= 20, \
                    f"Insufficient buffer time ({buffer} min) between flights"
            
            # Validate time window constraints
            assert route[0].departure_time >= scenario["t1"], \
                f"First flight departs before t1: {route[0].departure_time} < {scenario['t1']}"
            assert route[-1].arrival_time <= scenario["t2"], \
                f"Last flight arrives after t2: {route[-1].arrival_time} > {scenario['t2']}"
            
            # Print successful route
            print("✅ Route found and validated:")
            for flight in route:
                print(f"   Flight {flight.flight_no}: City {flight.start_city} -> {flight.end_city}, "
                      f"Time: {flight.departure_time}-{flight.arrival_time}")
            
        except AssertionError as e:
            print(f"❌ Failed: {str(e)}")

if __name__ == "__main__":
    test_complex_dense_network()