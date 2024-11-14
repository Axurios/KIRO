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
