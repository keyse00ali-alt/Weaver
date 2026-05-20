using EnergyScheduler.Api.Models;
using EnergyScheduler.Api.Interfaces;

namespace EnergyScheduler.Api.Infrastructure;

public class MockGeoService : IGeoService
{
    public Task<Location> GetLocationAsync()
    {
        return Task.FromResult(new Location { Latitude = 53.3498, Longitude = -6.2603 }); // Dublin, Ireland
    }
}