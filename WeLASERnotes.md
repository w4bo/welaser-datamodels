# WeLASER

- Mission: do we store the planned mission before? Otherwise, how do I pass the plan to the robot? 

## Next steps

- [LE + MF] Create the repository for the new and/or modified entities for the smart data model (let's check the structure of the original data model repository)
- [MF] Create a PoC with robot, devices, and ingestion of the entities
- [MF + MG] Update the meta-model with "historic" properties
- [MF] Prepare some mock-ups for Luis in order to (a) subscribe to robot changes/commands, (b) listen to kafka, (c) read/write to mongo, (d) join information on AgriFarm and AgriParcel
- [LE] Check the (un)necessary attributes of the entities, verify if the entities are generic enough also for other robots/applications in the AgriDomain
- [LE] Update AgriFarm and AgriParcel and add the other entities to describe the CSIC farm
- [LE] Understand how the MissionPlanner works, and who updates the actions

Long-term 
- [LE] Update the simulation with the AgriRobot and the mission. Robot starts on the gate, we `start` the weeding mission, `pause`, `resume`, `stop`.

## Next meetings

- Steering committe April: Show that subsystems can communicate. How I can communicate through kafka (we have several agriparcels). Select a specific data to get information. Two outcomes: smart data model + show how to interact with Kafka.
- June: preliminary demonstration. Robot moving from warehouse go to the field, move 2 turns, go back to the warehouse.

Python demo
- Listen to kafka
- Query mongodb
- Write to mongodb
- Demonstrate update FIWARE entity

## Open questions

- Should we keep some statistics on the weeds?
    - GA: we could have coverage maps, to map the planning. We are not doing that. Bur we can infer coverage maps from the robot / perception system.
    - Do we need to model the table of conditions? Not for now

- What information do we send back
- [Not critical] Map creation: Draw the polygons / linestring

## Entities

### HMI

This is a device. We can start the robot only if the HMI is close to the robot.
For now we assume that the user that is logged is close to the robot (something we can plan to do)

### AgriFarm

Access control
- Farmer (control all the farms): update when he seeds/crop

### Agriparcel
- Orientation
- Forbidden area (?)
- Field: any polygon. Cropts are planted in straight lines. Whatever machine goes in the same direction as crops (i.e., you don't corss the crops). The fields are four main parts: 
    - Headland, where the robot turns and destroy the path, you cannot seed there) 
    - Lanes (seeded space). The lane depend on the width of the robot, you want to pass on each lane only 1 time
    - Alleys are the sides of the fields
    - Gate where the robot can enter and leave
- What about rasters?
- Model of the agriparcel:
- I only need the crops, and the gate, and the robot. Then after I see the first lane, the robot will adapt to the other. To us, we need the gate and the agriparcel.
- `hasCrop` is very important
- `cropStatus` (it should be misurated and should be accurate for WeLASER)
- `lastPlantedAt`
- `agriSoil`

### AgriMission

- JSON files with a sequence of points (this is the most basic mission). But we should also put a semantics on those points. We infer the orientation from consecutive points.
- When the robot enters the lane activate the laser, when it exits deactivate it.

RobotModel & robot
ROS (1 robot -> 1 active controller per time)
- Controller: the robot chooses the best controller depending on the situation (i.e., a table of conditions). Normally you do the simplest action possible (i.e., the shortest path in case of movement and the movement is constraineted to not damagae the field nor the robot. Also the orientation of the robot).
- Task (share the list of tasks. FieldNavigation / FarmNavigation concatenate basic tasks such as GoToGoal, FollowLine, MoveBack, Uturn)
- Action
- Robot pose (x, y, z, orientation). We assume the robot is moving on a plane.
- Local vs remote supervisor (the remote controller can recreate the behavior, but it is not that important)
- ROSbug to recrete the original behavior by storing the sequences of ros messages

Drones?


### Robot

Device with highlighy different sensor rates.

### Snippets

```json
{
    "id": "robotmodel:carob",
    "type": "RobotModel",
    "name": "Carob v1",
    "brandName": "AGC",
    "modelName": "Carob",
    "robotType": "Mobile robot",
    "cargoPayload": 850, // kgs
    "height": 1.5, // meters
    "width": 1.5, // meters
    "length": 2, // meters
    "fuelType": "diesel",
    "fuelEfficiency": ..., //
    "wheelsType" : "tracks",
}

// Using the ISOBUS standard
{
    "id":              "implementmodel:lzhlaser",
    "type":            "ImplementModel",
    "PTO":             ...,
    "auxValve":        [ ... ],
    "valve":           [ ... ],
    "actuationType":   "valve"/"heat"/"elec. power",
    "actuationNumber": ..., 
    ???
}

{
    // static
    "id": "laser-123",
    "type": "AgriLaser",
    "refImplementModel": "implementmodel:lzhlaser",
    "nominalPowerConmsumption": ...,

    // dynamic
    "powerConsumption": ..., // Watt
    "voltage": ..., // Volt
    "current": ..., // Ampere
}

{
    // Static
    "id":               "carob-123",
    "type":             "AgriRobot",
    "hasFarm":          ...,
    "refRobotModel":    "robotmodel:carob",
    "category":         [ ... ],
    "name":             "carob-123",
    "serviceProvided":  [ "weeding", "seeding" ],
    "hasImplement":     [ "laser-123" ]
    "hasDevice":        [ "camera1", "camera2", "therm1" ]

    // Dynamic
    "status":           [ "on", "off" ], // one value for each service
    "hitch":            ..., // number
    "weight":           ..., // number
    "location":         ..., // number
    "speed":            ..., // number
    "bearing":          ..., // number
    "heading":          ..., // number

    // commands
    "cmd":              "startFieldMission", // they value of the cmd should be known to both of us
}

{
    "id": "camera1",
    "type": "Device",
    "controlledProperty": [ "image" ]
    "value": [ ... ], // encoded64 byte
}

{
    "id": "camera2",
    "type": "Device",
    "controlledProperty": [ "image" ]
    "value": [ ... ], // encoded64 byte
}

{
    "id": "therm1",
    "type": "Device",
    "controlledProperty": [ "temperature" ]
    "value": [ ... ], // Number
}


// TASK (what you create offline and send to the robot)
{
    // static / planned
    "dateCreated":         unixtimestamp, // e.g., representing "2022/04/13-08.40.00"
    "id":                  "weeding-132",
    "type":                "Task",
    "goal":                "The robot will weed parcel-123",
    "taskType":            "Operation", // enum(Mission, Operation, Action)
    "name":                "Weeding", 

    "hasAgriRobot":        "carob-123",
    "hasWorkingArea":      "agriparcel-123",
    "workingAreaType":     "AgriParcel",
    "plannedBeginTime":     unixtimestamp, // e.g., representing "2022/04/13-10.40.00"
    "plannedEndTime":       unixtimestamp, // e.g., representing "2022/04/13-10.50.00"
    "plannedLocation":      GEOJSON,
    "plannedSpeed":             0.55 , // desired maximum speed in m/s
    "hasPlannedTaskChildren":  ["turnOnLaser1", "goto1", "goto2", "goto3", ..., "turnOffLaser1"],
    
    // dynamic / executed
    "hasExecutedTaskChildren": ["turnOnLaser1", "goto1", "goto3", "uturn1", ..., "turnOffLaser1"], // update when the lower-level task finished
    "actualBeginTime":      unixtimestamp, // e.g., representing "2022/04/12-10.52",
    "actualEndTime":        unixtimestamp, // e.g., representing "2022/04/12-10.57",
    "actualEndLocation":    GEOJSON,
    "status":               "finished", // this is taken from the agriparcel (planned, ongoing, finished, scheduled, cancelled, SKIPPED)
    "result":               "ok", // this is taken from the agriparcel
    "event":                "", // textual description enum(BATTERY_LOW, RAINING)
}

{
    // static / planned
    "dateCreated":             unixtimestamp, // e.g., representing "2022/04/13-08.40.00"
    "id":                      "goto1",
    "type":                    "Task",
    "goal":                    "foobar", // textual description
    "taskType":                "Action", // enum(Mission, Operation, Action)
    "name":                    "FollowRow", // this free text, but we keep it as enum(FollowRow, ...) 

    "hasAgriRobot":            "carob-123",
    "hasWorkingArea":          "agriparcel-123",
    "workingAreaType":         "AgriParcel",
    "plannedBeginTime":         unixtimestamp, // e.g., representing "2022/04/13-10.40.00"
    "plannedEndTime":           unixtimestamp, // e.g., representing "2022/04/13-10.50.00"
    "plannedLocation":          GEOJSON,
    "plannedSpeed":             0.55 , // desired maximum speed in m/s
    "hasPlannedTaskChildren":   [],
    
    // dynamic / executed
    "hasExecutedTaskChildren": [], // update when the lower-level task finished
    "actualBeginTime":      unixtimestamp, // e.g., representing "2022/04/12-10.52",
    "actualEndTime":        unixtimestamp, // e.g., representing "2022/04/12-10.57",
    "actualLocation":       GEOJSON,
    "status":               "finished", // this is taken from the agriparcel (planned, ongoing, finished, scheduled, cancelled, SKIPPED)
    "result":               "ok",       // this is taken from the agriparcel
    "event":                "",         // textual description enum(BATTERY_LOW, RAINING)
}
```
