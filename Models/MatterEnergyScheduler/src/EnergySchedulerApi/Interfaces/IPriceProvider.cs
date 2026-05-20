using EnergyScheduler.Api.Models;

namespace EnergyScheduler.Api.Interfaces;

public interface IPriceProvider
{
    Task<List<EnergyPrice>> GetDayAheadPricesAsync(DateTime date);
}