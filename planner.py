from flight import Flight

class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)
        self._heapify_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data.pop()
        min_item = self.data[0]
        self.data[0] = self.data.pop()
        self._heapify_down(0)
        return min_item

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.data[index][0] < self.data[parent][0]:
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        child = 2 * index + 1
        while child < len(self.data):
            if child + 1 < len(self.data) and self.data[child + 1][0] < self.data[child][0]:
                child += 1
            if self.data[index][0] <= self.data[child][0]:
                break
            self.data[index], self.data[child] = self.data[child], self.data[index]
            index = child
            child = 2 * index + 1

    def is_empty(self):
        return len(self.data) == 0


class HashMap:
    def __init__(self, size=16411):
        self.size = size
        self.slots = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        # Compute the slot index and access the corresponding entries list
        slot_index = self._hash(key)
        entries = self.slots[slot_index]

        # Update value if key already exists, otherwise add the new key-value pair
        for i, (k, v) in enumerate(entries):
            if k == key:
                entries[i] = (key, value)
                return
        entries.append((key, value))

    def get(self, key):
        # Compute the slot index and access the corresponding entries list
        slot_index = self._hash(key)
        entries = self.slots[slot_index]

        # Search for the key in entries and return the value if found
        for k, v in entries:
            if k == key:
                return v
        return None  # Key not found

    def remove(self, key):
        # Compute the slot index and access the corresponding entries list
        slot_index = self._hash(key)
        entries = self.slots[slot_index]

        # Search for the key in entries and remove it if found
        for i, (k, v) in enumerate(entries):
            if k == key:
                del entries[i]
                return

    def contains_key(self, key):
        # Compute the slot index and access the corresponding entries list
        slot_index = self._hash(key)
        entries = self.slots[slot_index]

        # Check if the key exists in entries
        for k, _ in entries:
            if k == key:
                return True
        return False



class Planner:
    def __init__(self, flights):
        self.graph = HashMap(16411)
        for flight in flights:
            if not self.graph.contains_key(flight.start_city):
                self.graph.put(flight.start_city, [])
            self.graph.get(flight.start_city).append(flight)

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        # Use a list as a queue for BFS
        queue = []  # Initialize an empty queue
        queue.append((start_city, [], t1))  # (current city, route so far, current time)

        best_route = None
        min_flights = float('inf')
        earliest_arrival = float('inf')

        while queue:
            # Dequeue the first element
            current_city, route_so_far, current_time = queue.pop(0)

            # If we've reached the destination, check if this route is the best one
            if current_city == end_city:
                if (len(route_so_far) < min_flights or
                    (len(route_so_far) == min_flights and current_time < earliest_arrival)):
                    best_route = route_so_far
                    min_flights = len(route_so_far)
                    earliest_arrival = current_time
                continue

            # Get flights from the current city
            city_flights = self.graph.get(current_city) or []

            for flight in city_flights:
                # Ensure the flight is within the allowed time window
                if flight.departure_time >= current_time and flight.arrival_time <= t2:
                    # Check if the flight forms a valid connection
                    if not route_so_far or flight.departure_time - route_so_far[-1].arrival_time >= 20:
                        # Enqueue the next step
                        queue.append((flight.end_city, route_so_far + [flight], flight.arrival_time))

        # Return the best route found, or an empty list if no route exists
        return best_route if best_route else []



    def cheapest_route(self, start_city, end_city, t1, t2):
        queue = MinHeap()
        queue.push((0, start_city, [], t1))  # (total_cost, city, route_so_far, time)

        best_routes = HashMap(16411)
        best_routes.put(start_city, 0)

        while not queue.is_empty():
            current_cost, current_city, route_so_far, current_time = queue.pop()

            if current_city == end_city:
                return route_so_far

            city_flights = self.graph.get(current_city) or []
            if len(city_flights) > 100:
                city_flights = city_flights[:100]

            for flight in city_flights:
                if flight.departure_time >= current_time and flight.arrival_time <= t2:
                    if route_so_far:
                        last_arrival_time = route_so_far[-1].arrival_time
                        if flight.departure_time - last_arrival_time < 20:
                            continue

                    best_cost = best_routes.get(flight.end_city)
                    if best_cost is None or current_cost + flight.fare < best_cost:
                        best_routes.put(flight.end_city, current_cost + flight.fare)
                        queue.push((current_cost + flight.fare, flight.end_city, route_so_far + [flight], flight.arrival_time))

        return []

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        
        queue = MinHeap()
        queue.push(((0, 0), start_city, [], t1))

        # HashMap to store the best route by least flights and cheapest cost
        best_routes = HashMap(16411)
        best_routes.put(start_city, (0, 0))  # Stores (least flights, lowest cost) to each city

        while not queue.is_empty():
            (num_flights, current_cost), current_city, route_so_far, current_time = queue.pop()


            if current_city == end_city:
                return route_so_far

            
            city_flights = self.graph.get(current_city) or []
            if len(city_flights) > 100:
                city_flights = city_flights[:100]  # Limit to the first 100 flights

            for flight in city_flights:
                # Check Time constraints
                if flight.departure_time >= current_time and flight.arrival_time <= t2:
                    
                    if route_so_far:
                        last_arrival_time = route_so_far[-1].arrival_time
                        if flight.departure_time - last_arrival_time < 20:
                            continue

                    new_num_flights = num_flights + 1
                    new_cost = current_cost + flight.fare
                    
                    
                    best_route = best_routes.get(flight.end_city)
                    
                    
                    if (not best_route or 
                        new_num_flights < best_route[0] or 
                        (new_num_flights == best_route[0] and new_cost < best_route[1])):
                        
                        best_routes.put(flight.end_city, (new_num_flights, new_cost))
                        # Use tuple for proper priority comparison
                        queue.push(
                            ((new_num_flights, new_cost), 
                            flight.end_city, 
                            route_so_far + [flight], 
                            flight.arrival_time)
                        )

        return []