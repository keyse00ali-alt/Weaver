using EnergyScheduler.Api.Models;

namespace EnergyScheduler.Api.Interfaces;

public interface IGeoService
{
    Task<Location> GetLocationAsync();
}