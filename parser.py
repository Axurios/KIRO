import json


class dataParser:
    def __init__(self, filename):
        self.filename = filename
        self.shops = {}
        self.parameters = {}
        self.vehicles = {}
        self.constraints = []
        self._load_data()

    def _load_data(self):
        """Load JSON data from the file."""
        with open(self.filename, 'r') as file:
            data = json.load(file)
        self._parse_data(data)

    def _parse_data(self, data):
        """Parse JSON data into structured format."""
        # Parse shops and their resequencing lags
        self.shops = {shop['name']: shop['resequencing_lag'] for shop in data['shops']} # noqa:

        # Parse general parameters
        self.parameters = data.get('parameters', {})

        # Parse vehicle information
        self.vehicles = {vehicle['id']: vehicle['type'] for vehicle in data['vehicles']} # noqa:

        # Parse constraints
        self.constraints = data.get('constraints', [])

    def get_shops(self):
        """Return shops data."""
        return self.shops

    def get_parameters(self):
        """Return parameters data."""
        return self.parameters

    def get_vehicles(self):
        """Return vehicles data."""
        return self.vehicles

    def get_constraints(self):
        """Return constraints data."""
        return self.constraints

    def compute_costs(self):
        """Compute individual costs based on constraints."""
        batch_cost = 0
        lot_change_cost = 0
        rolling_window_cost = 0
        two_tone_cost = 0
        resequencing_cost = self.parameters.get('resequencing_cost', 0)

        for constraint in self.constraints:
            cost = constraint.get("cost", 0)
            if constraint['type'] == 'batch_size':
                # Example placeholder calculation for batch size constraint
                min_vehicles = constraint.get('min_vehicles', 0)
                max_vehicles = constraint.get('max_vehicles', 0)
                batch_cost += cost * (max_vehicles - min_vehicles)

            elif constraint['type'] == 'lot_change':
                # Example placeholder calculation for lot change constraint
                lot_change_cost += cost  # Directly add cost for demonstration

            elif constraint['type'] == 'rolling_window':
                # Example placeholder calculation for rolling window constraint
                max_vehicles = constraint.get('max_vehicles', 0)
                window_size = constraint.get('window_size', 0)
                rolling_window_cost += cost * (window_size - max_vehicles)

            elif constraint['type'] == 'two_tone':
                # Example placeholder calculation for two-tone constraint
                two_tone_cost += cost

        # Total cost calculation (sum of all individual costs)
        total_cost = batch_cost + lot_change_cost + rolling_window_cost + two_tone_cost + resequencing_cost
        return {
            "batch_cost": batch_cost,
            "lot_change_cost": lot_change_cost,
            "rolling_window_cost": rolling_window_cost,
            "two_tone_cost": two_tone_cost,
            "resequencing_cost": resequencing_cost,
            "total_cost": total_cost
        }
