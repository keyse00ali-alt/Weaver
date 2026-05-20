using EnergyScheduler.Api.Models;

namespace EnergyScheduler.Api.Interfaces;

public interface ISchedulingService
{
    DateTime CalculateOptimalStartTime(Appliance appliance, List<EnergyPrice> prices);
}