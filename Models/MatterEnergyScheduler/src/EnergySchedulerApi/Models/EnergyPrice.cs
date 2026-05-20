namespace EnergyScheduler.Api.Models;

public class EnergyPrice
{
    public DateTime StartTime { get; set; }
    public decimal PricePerKwh { get; set; }
}