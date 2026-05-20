using EnergyScheduler.Api.Models;
using EnergyScheduler.Api.Interfaces;

namespace EnergyScheduler.Api.Infrastructure;

public class MockPriceProvider : IPriceProvider
{
    public Task<List<EnergyPrice>> GetDayAheadPricesAsync(DateTime date)
    {
        var prices = new List<EnergyPrice>();
        for (int i = 0; i < 48; i++) // 24 hours * 2 (30 min intervals)
        {
            prices.Add(new EnergyPrice
            {
                StartTime = date.AddHours(i * 0.5),
                PricePerKwh = 0.20m + (decimal)(i * 0.005) // Mock increasing price
            });
        }
        return Task.FromResult(prices);
    }
}