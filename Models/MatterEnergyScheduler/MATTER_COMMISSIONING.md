# Matter Device Commissioning

This API commissions and controls Matter devices through `python-matter-server`, following the Matter protocol model: commissioning may use BLE, Wi-Fi Soft AP, or DNS-SD, then normal device control happens as Matter operational traffic over IPv6 on Wi-Fi, Ethernet, or Thread.

For 100% realistic testing with Podman appliances, do not register fake localhost devices from the UI. Run virtual Matter devices and a Matter server/controller on an IPv6-capable network path, commission the devices with their Matter setup payloads, and let operational discovery resolve their node IDs and addresses.

## Commissioning Process

### 1. Device Discovery (Optional)
Discover commissionable Matter devices through the Matter server:

```http
GET /matter/discover
```

### 2. Commission Device
Commission a device using its QR code:

```http
POST /matter/commission
Content-Type: application/json

{
  "qr_code": "MT:ABC123...",  // QR code from device
  "device_name": "Kitchen Light",
  "ip_address": "operational-discovery",
  "port": 5540
}
```

**Response:**
```json
{
  "device": {
    "id": "uuid-generated",
    "name": "Kitchen Light",
    "matter_device_id": "matter_12345",
    "ip_address": "operational-discovery",
    "port": 5540,
    "device_type": "unknown",
    "node_id": 12345,
    "fabric_id": 1,
    "vendor_id": 1234,
    "product_id": 5678,
    "commissioning_date": "2026-04-21T10:30:00",
    "is_commissioned": true
  },
  "message": "Device commissioned successfully"
}
```

### 3. Manage Commissioned Devices

**List all commissioned devices:**
```http
GET /matter/commissioned-devices
```

**Get specific device:**
```http
GET /matter/commissioned-devices/{device_id}
```

**Remove commissioned device:**
```http
DELETE /matter/commissioned-devices/{device_id}
```

## QR Code Format

Matter QR codes contain commissioning information encoded in base45 format with the prefix `MT:`. The QR code includes:

- Vendor ID
- Product ID
- Discriminator
- Setup PIN code
- Commissioning flow information

## Security Notes

- Commissioning establishes secure credentials between the device and your fabric
- Each commissioned device gets a unique node ID and operational certificates
- Operational commands use Matter CASE-secured sessions over IPv6, not an HTTP localhost shim
- Thread devices require a Thread Border Router or an equivalent realistic test topology
- The 20% BESS buffer is respected during scheduling to prevent battery depletion

## Integration with Scheduling

Once commissioned, devices can be used in appliance scheduling:

1. Commission the appliance from its Matter QR/manual setup code.
2. Weaver auto-registers a schedulable appliance with the commissioned Matter node ID.
3. Use the scheduling endpoints with the appliance ID.
4. The background runner sends commands through `python-matter-server` to the Matter node.

## Example Workflow

```bash
# 1. Commission a device
curl -X POST http://localhost:8000/matter/commission \
  -H "Content-Type: application/json" \
  -d '{
    "qr_code": "MT:ABC123...",
    "device_name": "Washing Machine",
    "ip_address": "operational-discovery"
  }'

# 2. Schedule the auto-registered appliance for optimal time
curl -X POST http://localhost:8000/schedule/grid-pv-bess \
  -H "Content-Type: application/json" \
  -d '{
    "appliance_id": "appliance-uuid",
    "household": {
      "household_type": "grid_pv_and_bess",
      "pv_capacity_kw": 5.0,
      "bess_capacity_kwh": 10.0
    }
  }'
```
