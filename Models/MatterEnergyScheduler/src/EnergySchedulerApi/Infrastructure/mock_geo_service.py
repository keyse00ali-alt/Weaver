from ..Models.location import Location

class MockGeoService:
    async def get_location(self) -> Location:
        return Location(latitude=53.3498, longitude=-6.2603)  # Dublin