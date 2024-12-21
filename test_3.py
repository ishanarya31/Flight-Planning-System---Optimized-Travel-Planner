from flight import Flight
from planner import Planner

def test_complex_network_least_flights_cheapest_route():
    """
    Test with a dense network of flights between 5 cities with multiple possible routes.
    Cities are: 0 (New York), 1 (Chicago), 2 (Denver), 3 (Los Angeles), 4 (Seattle)
    Test cases focus on finding the route with the least number of flights that is also the cheapest within time constraints.
    Returns empty list [] when no route is found.
    """
    
    flights = [
        # Direct flights from New York (0)
        Flight(0, 0, 69, 1, 120, 500),      # NY -> Chicago: expensive direct
        Flight(1, 0, 0, 1, 120, 300),      # NY -> Chicago: expensive direct
        Flight(2, 0, 60, 1, 180, 250),     # NY -> Chicago: cheaper direct
        Flight(3, 0, 0, 3, 360, 800),      # NY -> LA: expensive direct
        Flight(4, 0, 0, 2, 180, 150),      # NY -> Denver: cheap flight
        Flight(12, 0, 30, 2, 210, 200),    # NY -> Denver: alternative route
        Flight(13, 0, 0, 4, 180, 400),     # NY -> Seattle: direct option
        Flight(19, 0, 80, 1, 190, 250),    # NY -> Chicago: medium cost
        
        # Connections through Chicago (1)
        Flight(5, 1, 140, 3, 300, 200),    # Chicago -> LA: medium cost
        Flight(6, 1, 200, 3, 360, 180),    # Chicago -> LA: cheaper option
        Flight(14, 1, 200, 4, 350, 250),   # Chicago -> Seattle: medium route
        Flight(15, 1, 210, 4, 360, 200),   # Chicago -> Seattle: cheaper route
        
        # Connections through Denver (2)
        Flight(7, 2, 200, 3, 380, 200),    # Denver -> LA: medium cost
        Flight(11, 2, 200, 3, 290, 100),   # Denver -> LA: cheapest option
        Flight(16, 2, 220, 4, 380, 150),   # Denver -> Seattle: good route
        
        # Seattle connections (4)
        Flight(17, 4, 200, 3, 360, 180),   # Seattle -> LA: medium route
        Flight(18, 4, 380, 3, 480, 300),   # Seattle -> LA: expensive route
        Flight(20, 4, 370, 2, 380, 200),   # Seattle -> Denver: medium route
        
        # Return flights
        Flight(8, 1, 400, 0, 520, 300),    # Chicago -> NY
        Flight(9, 3, 400, 0, 760, 800),    # LA -> NY
        
        # Late flights
        Flight(10, 0, 500, 3, 860, 700),   # NY -> LA: expensive late direct
    ]
    
    planner = Planner(flights)
    
    test_scenarios = [
        # Original test cases...
        {
            "start": 0, "end": 1, "t1": 0, "t2": 1000,
            "expected_total_cost": 250,
            "expected_flight_numbers": [2],  # Should take cheaper direct flight
            "description": "NY to Chicago - Should take cheaper direct flight"
        },
        {
            "start": 0, "end": 3, "t1": 0, "t2": 1000,
            "expected_total_cost": 700,  # NY->LA cheaper than direct
            "expected_flight_numbers": [10],  
            "description": "NY to LA - Should take expensive direct"
        },
        
        {
            "start": 0, "end": 4, "t1": 0, "t2": 400,
            "expected_total_cost": 400,  # NY->Seattle cheapest
            "expected_flight_numbers": [13],
            "description": "NY to Seattle - Multiple paths, one optimal (Direct)"
        },
        {
            "start": 0, "end": 3, "t1": 40, "t2": 400,
            "expected_total_cost": 430,  # NY->Chicago->LA
            "expected_flight_numbers": [2, 6],
            "description": "NY to LA - Late start forces different cheap route"
        },
        {
            "start": 0, "end": 4, "t1": 40, "t2": 350,
            "expected_total_cost": 500,  # NY->Chicago->Seattle
            "expected_flight_numbers": [2,14],  
            "description": "NY to Seattle - Time window affects route choice, must maintain buffer"
        },
        {
            "start": 4, "end": 3, "t1": 180, "t2": 400,
            "expected_total_cost": 180,
            "expected_flight_numbers": [17],
            "description": "Seattle to LA - Choose direct over expensive multi-hop"
        },
        {
            "start": 0, "end": 2, "t1": 0, "t2": 1000,
            "expected_total_cost": 150,
            "expected_flight_numbers": [4],
            "description": "NY to Denver - Multiple options, should pick cheapest"
        },
        {
            "start": 0, "end": 3, "t1": 190, "t2": 860,
            "expected_total_cost": 700,  # NY->Denver(late)->LA
            "expected_flight_numbers": [10],
            "description": "NY to LA - Late start affects route choice but still optimal"
        },
        {
            "start": 4, "end": 0, "t1": 150, "t2": 800,
            "expected_total_cost": 980,  # Seattle -> LA -> NY
            "expected_flight_numbers": [17, 9],
            "description": "Seattle to NY - Forced multi-stop through LA"
        },
        {
            "start": 0, "end": 3, "t1": 70, "t2": 800,
            "expected_total_cost": 750,  # NY -> Chicago -> Seattle -> LA 
            "expected_flight_numbers": [19, 15, 18],
            "description": "NY to LA - Forced multi-stop through Seattle and Chicago"
        },
        {
            "start": 1, "end": 2, "t1": 0, "t2": 1000,
            "expected_total_cost": 450,  # Chicago -> Denver
            "expected_flight_numbers": [14,20],
            "description": "Chicago to Denver - Multiple paths, one optimal (not forsaking feasibility for cost)"
        },
        # Edge cases
        {
            "start": 0, "end": 0, "t1": 0, "t2": 1000,
            "expected_total_cost": 0,
            "expected_flight_numbers": [],
            "description": "Same city - Should return empty list"
        },
        {
            "start": 0, "end": 3, "t1": 0, "t2": 100,
            "expected_total_cost": 0,
            "expected_flight_numbers": [],
            "description": "Impossible time window"
        },
    ]
    
    print("\nRunning complex network test scenarios for least flights cheapest routes...")
    for scenario in test_scenarios:
        route = planner.least_flights_cheapest_route(
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
            if scenario["expected_total_cost"] == 0:
                assert isinstance(route, list) and len(route) == 0, \
                    f"Expected empty list, but got {route}"
                print("✅ Correctly returned empty list")
                continue
            
            # Validate route exists
            assert isinstance(route, list) and len(route) > 0, \
                "Expected non-empty route, but got empty list"
            
            # Validate correct flights were chosen
            actual_flight_numbers = [f.flight_no for f in route]
            assert actual_flight_numbers == scenario["expected_flight_numbers"], \
                f"Expected flights {scenario['expected_flight_numbers']}, but got {actual_flight_numbers}"
            
            # Validate total cost
            total_cost = sum(f.fare for f in route)
            assert total_cost == scenario["expected_total_cost"], \
                f"Expected total cost {scenario['expected_total_cost']}, but got {total_cost}"
            
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
            print(f"   Total cost: {total_cost}")
            for flight in route:
                print(f"   Flight {flight.flight_no}: City {flight.start_city} -> {flight.end_city}, "
                      f"Time: {flight.departure_time}-{flight.arrival_time}, Cost: {flight.fare}")
            
        except AssertionError as e:
            print(f"❌ Failed: {str(e)}")
            raise e

if __name__ == "__main__":
    test_complex_network_least_flights_cheapest_route()