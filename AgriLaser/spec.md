Entity: AgriLaser 
================
 
Global description: **This entity contains a harmonised description of a generic laser implement.** 

## List of properties 

### Static 

- `id`: Unique identifier of the entity
- `type`: NGSI Entity Type. It has to be AgriLaser
- `refImplementModel`: Id of the reference implement model
- `hasAgriRobot`: Id of the robot in which the implement is operating
- `nominalPowerConmsumption`: (**TBD**)
- `hasDevice`: List of the mounted device ids
- `serviceProvided`: List of services provided by the implement
- `areaServed`: Id of the farm in which the implement is operating
- `scanners`: number of scanners
- `scanner range`: Lateral range in meters of the scanners

### Dynamic
- `location`: Location of the implement, GEOJSON point
- `rate`: Current application rate (weeds/second)
- `powerConsumption`: (**TBD**), in Watt
- `status`:   List of service statuses, one for each provided service
- `weedDensity`: Current weed density

---------------------------
- `voltage`: (**TBD**), in Volt
- `current`: (**TBD**), in Ampere
