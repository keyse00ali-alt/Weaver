namespace EnergyScheduler.Api.Models;

public class Appliance
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Name { get; set; } = string.Empty;
    
    // Power consumption in kW (e.g., 2.5 for a washing machine)
    public double PowerUsageKw { get; set; } 
    
    // How long the cycle lasts
    public TimeSpan Duration { get; set; }
    
    // The user's deadline (must be finished by this time)
    public DateTime Deadline { get; set; }
    
    // ID for the Matter-enabled hardware
    public string MatterDeviceId { get; set; } = string.Empty;
}