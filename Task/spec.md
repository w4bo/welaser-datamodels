Entity: Task  
================
  
Global description: **This entity contains a harmonised description of a generic task.**  

## List of properties  

### Static

- `id`: Unique identifier of the entity  
- `type`: NGSI Entity Type. It has to be Task
- `name`: The name of this item.
- `goal`: A generic description of the goal
- `taskType`: The conceptual level of the task, enum(Mission, Operation, Action)
- `hasAgriRobot`: List of ids of the robots involved in the task
- `hasWorkingArea`: Id of the AgriFarm or ArgriParcel on which the robot is operating
- `hasWorkingAreaType`: Type of the working aera
- `plannedBeginTime`: The planned being time, in unixtimestamp, // e.g., representing "2022/04/13-10.40.00"
- `plannedEndTime`: The planned end time, in unixtimestamp, // e.g., representing "2022/04/13-10.50.00"
- `plannedLocation`: The planned location of the task, a valid GEOJSON
- `plannedSpeed`: The desired speed, in m/s
- `hasPlannedTaskChildren`: The list of planned subtask ids

### Dynamic

- `hasActualTaskChildren`: The list of actually executed subtask ids. This is updated when the lower-level task finished.
- `actualBeginTime`: The actual begin time, in unixtimestamp; e.g., representing "2022/04/12-10.52"
- `actualEndTime`: The actual end time, in unixtimestamp; e.g., representing "2022/04/12-10.57"
- `actualEndLocation`: The actual location of the task, a valid GEOJSON
- `status`: The status of the task, enum: (planned, ongoing, finished, scheduled, cancelled, SKIPPED)
- `result`: The result of the task, enum: **TBD** 
- `event`: List of the events recorded during the task, enum: (BATTERY_LOW, RAINING, **TBD** )