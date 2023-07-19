Entity: RobotModel  
================
  
Global description: **This entity contains a harmonised description of a generic robot model.**  

## List of properties  


- `id`: Unique identifier of the entity  
- `type`: NGSI Entity Type. It has to be RobotModel  
- `name`: The name of this item.  
- `brandName`: The brand
- `modelName`: The name of the model
- `robotType`: The type of robot (enum: "manipulator", "mobile platform", "wearable robot")
- `cargoPayload`: In kilograms
- `height`: The height of the robot model, in meters
- `width`: The width of the robot model, in meters
- `length`: The length of the robot model, in meters
- `fuelType`: The fuel type (enum: "electricity", "gasoline", "diesel", "fuel cell")
- `fuelEfficiency`: in percentage
- `locomotionType`: The type of locomotion/actuation (enum: for the mobile platform: "wheeled", "legged", "biped", "crawler", "tracked", "humanoid" ; for manipulator: "Cartesian", "cylindrical", "spherical", "pendular", "articulated", "SCARA", "parallel")
