<img width="2107" height="1001" alt="Screenshot 2026-02-20 225425" src="https://github.com/user-attachments/assets/e1003dbd-7c92-4360-b6cb-c036ba04c5c5" />

### Attributes
- Identifier: households.id, smart_meters.id
- Mandatory: address, global_active_power
- Optional: firmware_version, global_reactive_power
- Single-value: city, voltage

### Entities
- Strong: households, smart_meters, rate_plans
- Weak: energy_readings (smart_meters and has composite primary key)
- Associative: household_to_rate_plans (for M:M)

### Relationships
- 1:1 smart_meters and meter_locations
- 1:M households → smart_meters
- M:M households and rate_plans (thru household_to_rate_plans)
