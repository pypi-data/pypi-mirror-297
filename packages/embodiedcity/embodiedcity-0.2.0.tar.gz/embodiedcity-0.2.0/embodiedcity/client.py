from typing import Any, Dict, List, NamedTuple, Optional, Tuple, cast

import requests
import numpy as np
import cv2
from pyproj import Proj
from shapely.geometry import Point
from shapely.strtree import STRtree
from scipy.linalg import lstsq


__all__ = ["ImageType", "CameraID", "POI", "DroneClient"]


class ImageType:
    Scene = 0
    """Scene (RGB)"""
    DepthPlanar = 1
    """DepthPlanar (Depth)"""
    Segmentation = 2


class CameraID:
    FrontCenter = 0
    """front_center"""
    FrontRight = 1
    """front_right"""
    FrontLeft = 2
    """front_left"""
    BottomCenter = 3
    """bottom_center"""
    BackCenter = 4
    """back_center"""


class POI(NamedTuple):
    id: int
    x: float
    y: float
    name: str
    category: str


class AffineTransformer:
    def __init__(self):
        # 已知点
        local_points = [
            (5598.70000000, -3432.20000000),
            (5586.00000000, -5588.80000000),
            (7429.30000000, -5542.70000000)
        ]
        latlon_points = [
            (39.90838719666494, 116.46173862693877),
            (39.93371933689764, 116.46173732726206),
            (39.933684214234376, 116.48987439205544)
        ]

        self.local_points = np.array(local_points)
        self.latlon_points = np.array(latlon_points)
        self.local_to_latlon_transform = self.compute_affine_transform(self.local_points, self.latlon_points)
        self.latlon_to_local_transform = self.compute_affine_transform(self.latlon_points, self.local_points)

    def compute_affine_transform(self, src_points, dst_points):
        """
        Computes the affine transformation matrix that maps src_points to dst_points.
        """
        A = []
        B = []
        for (x, y), (x_p, y_p) in zip(src_points, dst_points):
            A.append([x, y, 1, 0, 0, 0])
            A.append([0, 0, 0, x, y, 1])
            B.append(x_p)
            B.append(y_p)

        A = np.array(A)
        B = np.array(B)

        # Solve the least squares problem to find the affine transform
        X, _, _, _ = lstsq(A, B)

        return X.reshape(2, 3)

    def apply_affine_transform(self, points, transform):
        """
        Applies the affine transformation to a set of points.
        """
        points = np.hstack([points, np.ones((points.shape[0], 1))])
        transformed_points = points.dot(transform.T)
        return transformed_points

    def local_to_latlon(self, x, y):
        """
        Converts local coordinates to latitude and longitude.
        """
        lat, lon = self.apply_affine_transform(np.array([[x, y]]), self.local_to_latlon_transform)[0]
        return lat, lon

    def latlon_to_local(self, lat, lon):
        """
        Converts latitude and longitude to local coordinates.
        """
        x, y = self.apply_affine_transform(np.array([[lat, lon]]), self.latlon_to_local_transform)[0]
        return x, y


class DroneClient:
    def __init__(self, base_url: str, drone_id: str, token: str):
        """
        Args:
        - base_url: The base URL of the server
        - drone_id: The ID of the drone
        - token: The token to authenticate requests with the server
        """
        self._base_url = base_url.rstrip("/")
        self._drone_id = drone_id
        self._token = token
        self._transformer = AffineTransformer()
        self._pois, self._poi_tree = self._prepare_pois()

    def _make_request(self, action: str, *args):
        url = f"{self._base_url}/api/call-function"
        res = requests.post(
            url,
            json={
                "droneId": self._drone_id,
                "action": action,
                "args": args,
                "token": self._token,
            },
        )
        if res.status_code != 200:
            raise Exception(f"Failed to make request: {res.text}")

        content_type = res.headers["Content-Type"].split(";")[0]
        if content_type == "application/json":
            return res.json()["data"]
        if content_type == "image/jpeg":
            data = res.content
            # 以彩色模式读取图像二进制数据
            img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            # OpenCV读取的图像是BGR格式，如果是用于显示或处理RGB图像，则需要转换颜色通道
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        raise Exception(f"Unexpected response: {res.headers['Content-Type']}")

    def _prepare_pois(self):
        data = cast(Dict[str, Any], self._make_request("get_pois"))
        projector = Proj(data["projection"])
        pois = [POI(
            id=p["id"],
            x=p["position"]["x"],
            y=p["position"]["y"],
            name=p["name"],
            category=p["category"]
        ) for p in data["pois"]]
        converted_pois = []
        for p in pois:
            lng, lat = projector(p.x, p.y, inverse=True)
            ue_x, ue_y = self._transformer.latlon_to_local(lat, lng)
            converted_pois.append(POI(
                id=p.id,
                x=ue_x,
                y=ue_y,
                name=p.name,
                category=p.category
            ))
        return converted_pois, STRtree([Point(p.x, p.y) for p in converted_pois])

    def move_back_forth(self, distance: float):
        """
        Move the drone back and forth by a certain distance

        Args:
        - distance: The distance to move the drone by (unit: meters). distance > 0 means moving forward, distance < 0 means moving backward.

        Returns:
        - None
        """
        return self._make_request("move_back_forth", distance)

    def move_horizontal(self, distance: float):
        """
        Move the drone left and right by a certain distance

        Args:
        - distance: The distance to move the drone by (unit: meters). distance > 0 means moving left, distance < 0 means moving right.

        Returns:
        - None
        """
        return self._make_request("move_horizontal", distance)

    def move_vertical(self, distance: float):
        """
        Move the drone up and down by a certain distance

        Args:
        - distance: The distance to move the drone by (unit: meters). distance > 0 means moving up, distance < 0 means moving down.

        Returns:
        - None
        """
        return self._make_request("move_vertical", distance)

    def move_by_yaw(self, yaw: float):
        """
        Rotate the drone by a certain angle

        Args:
        - yaw: The angle to rotate the drone by (unit: radians). Positive values mean rotating counterclockwise, negative values mean rotating clockwise.

        Returns:
        - None
        """
        return self._make_request("move_by_yaw", yaw)

    def get_image(self, image_type: ImageType, camera_id: CameraID):
        """
        Get an image from the drone

        Args:
        - image_type: The type of image to get
        - camera_id: The ID of the camera to get the image from

        Returns:
        - numpy.array: The image
        """

        return self._make_request("get_image", int(image_type), str(camera_id))

    def get_current_state(self):
        """
        Get the current state of the drone

        Returns:
        - [x, y, z]: The position of the drone
        - [pitch, roll, yaw]: The orientation of the drone
        """

        response = self._make_request("get_current_state")
        return response[0], response[1]

    def move_to_position(self, x: float, y: float, z: float):
        """
        Move the drone to a certain position

        Args:
        - x: The x-coordinate of the target position
        - y: The y-coordinate of the target position
        - z: The z-coordinate of the target position

        Returns:
        - None
        """
        return self._make_request("move_to_position", x, y, z)

    def set_vehicle_pose(
        self, x: float, y: float, z: float, pitch: float, roll: float, yaw: float
    ):
        """
        Set the pose of the drone.
        Attention: This function will teleport the drone to the target position.

        Args:
        - x: The x-coordinate of the target position
        - y: The y-coordinate of the target position
        - z: The z-coordinate of the target position
        - pitch: The pitch of the drone
        - roll: The roll of the drone
        - yaw: The yaw of the drone

        Returns:
        - None
        """
        return self._make_request("set_vehicle_pose", x, y, z, pitch, roll, yaw)

    def query_pois(
        self,
        x: float,
        y: float,
        radius: float,
        category_prefix: str = "",
        limit: Optional[int] = None,
    ) -> List[Tuple[POI, float]]:
        """
        Query the POIs whose categories satisfy the prefix within the specified radius of the center point (sorted by distance).

        Args:
        - x: The x-coordinate of the center of the area
        - y: The y-coordinate of the center of the area
        - radius: The radius of the area (unit: meters)
        - category_prefix: The prefix of the category of the POIs to query
        - limit: The maximum number of POIs to return, sorted by distance, closest ones first (default to None)

        Returns:
        - List[Tuple[POI, float]]: The (poi, distance) pairs in the area sorted by distance
        """

        center = Point(x, y)
        # 获取半径内的poi
        indices = self._poi_tree.query(center.buffer(radius))
        # 过滤掉不满足类别前缀的poi
        pois = []
        for index in indices:
            poi: POI = self._pois[index]
            if poi.category.startswith(category_prefix):
                distance = center.distance(Point(poi.x, poi.y))
                pois.append((poi, distance))
        # 按照距离排序
        pois = sorted(pois, key=lambda x: x[1])
        if limit is not None:
            pois = pois[:limit]
        return pois
