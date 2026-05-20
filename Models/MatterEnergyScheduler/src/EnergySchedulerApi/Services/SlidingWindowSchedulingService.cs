using System;
using System.Linq;
using EnergyScheduler.Api.Models;
using EnergyScheduler.Api.Interfaces;

namespace EnergyScheduler.Api.Services;

public class SlidingWindowSchedulingService : ISchedulingService
{
    private const double IntervalHours = 0.5; // Assume 30 min intervals

    public DateTime CalculateOptimalStartTime(Appliance appliance, List<EnergyPrice> prices)
    {
        if (prices == null || prices.Count == 0) throw new ArgumentException("Prices cannot be empty");

        // Sort prices by StartTime
        prices = prices.OrderBy(p => p.StartTime).ToList();

        // Calculate number of intervals for duration
        int numIntervals = (int)Math.Ceiling(appliance.Duration.TotalHours / IntervalHours);
        if (numIntervals == 0) numIntervals = 1; // at least one

        // Find possible start indices
        double minCost = double.MaxValue;
        DateTime optimalStart = DateTime.MinValue;

        for (int i = 0; i <= prices.Count - numIntervals; i++)
        {
            DateTime startTime = prices[i].StartTime;
            DateTime endTime = startTime.AddHours(numIntervals * IntervalHours);
            if (endTime > appliance.Deadline) continue; // cannot finish by deadline

            // Calculate cost: sum of prices over the window * power * interval
            double cost = 0;
            for (int j = 0; j < numIntervals; j++)
            {
                cost += (double)prices[i + j].PricePerKwh * appliance.PowerUsageKw * IntervalHours;
            }

            if (cost < minCost)
            {
                minCost = cost;
                optimalStart = startTime;
            }
        }

        if (optimalStart == DateTime.MinValue) throw new InvalidOperationException("No feasible schedule found");

        return optimalStart;
    }
}