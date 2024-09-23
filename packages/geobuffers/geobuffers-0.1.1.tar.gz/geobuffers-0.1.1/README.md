# geobuffers

This repository contains code that allows simple definitions of polygons defined around a coordinate of interest using geodesic distances. Some of the functionality can be reproduced with [geopandas buffer](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.buffer.html) functionality.

Instead, all methods here rely on [pyproj.Geod](https://pyproj4.github.io/pyproj/stable/api/geod.html) geodetic computations using Clarke 1866 Ellipsoid.

## Available shapes

|          | Name    | Parameters | Description |
| -------- | ------- | :--------  | :---------- |
| ![square](https://github.com/user-attachments/assets/e0253ee4-ecd4-4344-90aa-833c82c248c0)     |  square   | `radius`, `azimuth_angle`             | Square with a distance center-to-corner `radius` and rotated by `azimuth_angle`  |
| ![triangle](https://github.com/user-attachments/assets/57c0cf0b-c6d5-42b6-a2bf-b3d85109bbab)   |  triangle | `radius`, `azimuth_angle`             | Square with a distance center-to-corner `radius` and rotated by `azimuth_angle`  |
| ![hex](https://github.com/user-attachments/assets/185172e1-10e2-4b30-b70c-7efe2a12b68e)        | hexagon   | `radius`, `azimuth_angle`             | Hexagon with a distance center-to-vertex `radius` and rotated by `azimuth_angle` |
| ![13-gon](https://github.com/user-attachments/assets/7dc35c41-cc9d-425c-aa28-36680a804b42)     | regpol    | `n`, `radius`, `azimuth_angle`        | Regular polygon with `n` vertices `radius` metres away from the center, with first vertex at azimuth of `azimuth_angle` degrees |
| ![fov](https://github.com/user-attachments/assets/3a41efe8-14ce-4ba6-ad15-cca5b708bbec)        | fov       | `radius`, `azimuth_angle`, `fov_angle`| Field of view traingle at distance `radius`, pointing towards angle `azimuth_angle` with angular width of `fov_angle` degrees |

## Example Usage
```python
  import geobuffers as gbf
  from shapely import Point

  my_point = Point([1.0, -1.0])

  square(my_point)
```




