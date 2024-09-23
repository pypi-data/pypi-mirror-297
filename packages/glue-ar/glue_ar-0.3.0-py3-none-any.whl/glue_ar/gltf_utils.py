import operator
import struct
from typing import Callable, Iterable, List, Optional, Type, TypeVar, Union

from gltflib import Material, PBRMetallicRoughness

__all__ = [
    "slope_intercept_between",
    "clip_linear_transformations",
    "bring_into_clip",
    "offset_triangles",
    "create_material_for_color",
    "add_points_to_bytearray",
    "add_triangles_to_bytearray",
    "index_mins",
    "index_maxes",
]


GLTF_COMPRESSION_EXTENSIONS = {
    "draco": "KHR_draco_mesh_compression",
    "meshoptimizer": "EXT_meshopt_compression",
}


def slope_intercept_between(a, b):
    slope = (b[1] - a[1]) / (b[0] - a[0])
    intercept = b[1] - slope * b[0]
    return slope, intercept


def clip_linear_transformations(bounds, clip_size=1):
    ranges = [abs(bds[1] - bds[0]) for bds in bounds]
    max_range = max(ranges)
    line_data = []
    for bds, rg in zip(bounds, ranges):
        frac = rg / max_range
        target = frac * clip_size
        line_data.append(slope_intercept_between((bds[0], -target), (bds[1], target)))
    return line_data


def bring_into_clip(points, transforms):
    return [tuple(transform[0] * c + transform[1] for transform, c in zip(transforms, pt)) for pt in points]


def offset_triangles(triangle_indices, offset):
    return [tuple(idx + offset for idx in triangle) for triangle in triangle_indices]


def create_material_for_color(
    color: List[int],
    opacity: float
) -> Material:
    rgb = [t / 256 for t in color[:3]]
    return Material(
            pbrMetallicRoughness=PBRMetallicRoughness(
                baseColorFactor=rgb + [opacity],
                roughnessFactor=1,
                metallicFactor=0
            ),
            alphaMode="BLEND"
    )


def add_points_to_bytearray(arr: bytearray, points: Iterable[Iterable[Union[int, float]]]):
    for point in points:
        for coordinate in point:
            arr.extend(struct.pack('f', coordinate))


def add_triangles_to_bytearray(arr: bytearray, triangles: Iterable[Iterable[int]]):
    for triangle in triangles:
        for index in triangle:
            arr.extend(struct.pack('I', index))


T = TypeVar("T", bound=Union[int, float])


def index_extrema(items: List[List[T]],
                  extremum: Callable[[T, T], T],
                  previous: Optional[List[List[T]]] = None,
                  type: Type[T] = float) -> List[List[T]]:
    size = len(items[0])
    extrema = [type(extremum([operator.itemgetter(i)(item) for item in items])) for i in range(size)]
    if previous is not None:
        extrema = [extremum(x, p) for x, p in zip(extrema, previous)]
    return extrema


def index_mins(items, previous=None, type: Type[T] = float) -> List[List[T]]:
    return index_extrema(items, extremum=min, type=type, previous=previous)


def index_maxes(items, previous=None, type: Type[T] = float) -> List[List[T]]:
    return index_extrema(items, extremum=max, type=type, previous=previous)
