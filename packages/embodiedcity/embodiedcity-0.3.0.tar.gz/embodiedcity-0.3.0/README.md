# embodied-city-python-sdk

A Simple Python SDK to interact with the Embodied City API.
Users can easily achieve perception and control of drone agents through the following functions.
When the command is issued via the API, changes in the agent's first-person view will be observed in the Console.

## Installation

```bash
pip install embodiedcity
```

## Usage

#### Acquire ID and token

Before you can use the SDK, you need to acquire a drone and obtain its token.
You can get one by signing up at [Embodied City](https://embodied-city.fiblab.net/).

In the website, you should go to the "Console" page, choose an available drone, and click on the "Acquire" button.
After that, you will see a token with the drone ID.

> ATTENTION: The token is a secret key that should not be shared with anyone.

> ATTENTION: The token will expire after a certain period of time if you do not use it. (the time constrain will be notified in the website)

#### Initialize the client

```python
from embodiedcity import DroneClient, ImageType, CameraID

base_url = "https://embodied-city.fiblab.net"
drone_id = "xxx"
token = "xxxxxxxx"
client = DroneClient(base_url, drone_id, token)
```

#### Move the drone

```python
# Move the drone forward by 10 meter (Short movement distance may result in action failure)
client.move_back_forth(10)
```

#### Obtain the RGB image of the front camera
    
```python
# Get a RGB image from the front-center camera
image = client.get_image(ImageType.Scene, CameraID.FrontCenter)
```

#### Get the depth image
    
```python
# Get an image of the depth from the front-center camera
image = client.get_image(ImageType.DepthPlanar, CameraID.FrontCenter)
```

## Release the drone

After you finish using the drone, you should release it to make it available for others.

You can do this by clicking on the "Release" button in the "Console" page.


## FAQ

#### After invoking the control action, the drone did not move.

It is possible that the drone collided with a building.
Try issuing a command to move the drone in a direction without obstacles.
Alternatively, use the function DroneClient.move_to_position to force it to a specified location.

#### What should I do if I need the drone to perform more complex operations?

Please download and install the full embodiedcity simulator.

## HTTP Protocol

POST /api/call-function

Body:
```json
{
    "droneId": "drone ID",
    "action": "action string",
    "args": [arg1, arg2, ...],
    "token": "(optional) token for authorization"
}
```

Status code is 200 if the action is successful.

Action string, arg, return value:

| Action            | Args                                  | Description                                                                                                                                                                                                   | Return         | Description                                |
| ----------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------ |
| `move_back_forth` | [`distance`: float]                   | Move the drone back (<0) and forth (>0) by a certain distance (unit: meters)                                                                                                                                  | `None`         | -                                          |
| `move_horizontal` | [`distance`: float]                   | Move the drone left (>0) and right (<0) by a certain distance (unit: meters)                                                                                                                                  | `None`         | -                                          |
| `move_vertical`   | [`distance`: float]                   | Move the drone up (>0) and down (<0) by a certain distance (unit: meters)                                                                                                                                     | `None`         | -                                          |
| `move_by_yaw`     | [`yaw`: float]                        | Rotate the drone by a certain angle. Positive values mean rotating counterclockwise, negative values mean rotating clockwise. (unit: radians)                                                                 | `None`         | -                                          |
| `get_image`       | [`image_type`: int, `camera_id`: str] | Get an image from the specified camera. `image_type` can be 0 (Scene), 1 (DepthPlanar), 2 (Segmentation). `camera_id` can be 0 (FrontCenter), 1 (FrontRight), 2 (FrontLeft), 3 (BottomCenter), 4 (BackCenter) | `image`: bytes | The image data in bytes (MIME: image/jpeg) |
| `get_current_state` | [] | Get the current state of the drone | `[[x, y, z], [pitch, roll, yaw]]` | The current state of the drone |
| `move_to_position` | [`x`: float, `y`: float, `z`: float] | Move the drone to the specified position | `None` | - |
| `set_vehicle_pose` | [`x`: float, `y`: float, `z`: float, `pitch`: float, `roll`: float, `yaw`: float] | Set the pose of the drone | `None` | - |
