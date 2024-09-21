"""
   Copyright 2024 - Gael Systems

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import argparse
from typing import List
from dataclasses import dataclass

import folium
import geopandas as gpd
import shapely
from geopandas.array import GeometryArray
from shapely import Geometry, wkt
from shapely.geometry import shape, MultiPolygon
import geojson
from pyproj import Geod

import footprint_facility
import logging

logger = logging.getLogger('footprint_statistics')


def compute_area_from_4326(geometry):
    """
    Shapely don't care about the unity used in polygons. Is epsg:4326, polygons
    coordinates are in decimal degrees values whereas the area shall be
    expressed in meter. The simplest and most accurate method to manage the
    geographic to geodesic coordinates is to use pyproj library to map
    the polygon on a geoid (i.e. WGS84)
    :param geometry:
    :return:
    """
    geod = Geod(ellps="WGS84")
    if isinstance(geometry, GeometryArray):
        area = 0
        for geo in geometry:
            area += compute_area_from_4326(geo)
    else:
        area = abs(geod.geometry_area_perimeter(geometry)[0])
    return area


def area_to_user_readable(area: float) -> str:
    if area > 1e6:
        return '%.2f km<sup>2' % (area / 1e6)
    else:
        return '%.2f m<sup>2' % area


@dataclass
class FootprintStatistics:
    origin_footprint: Geometry
    reworked_footprint: Geometry
    tolerance: float = None

    def origin_points(self):
        return len(shapely.get_coordinates(self.origin_footprint))

    def reworked_points(self):
        return len(shapely.get_coordinates(self.reworked_footprint))

    def delta_point(self):
        return self.origin_points() - self.reworked_points()

    def map(self):
        d1 = {'name': ['origin'],
              'point no': self.origin_points(),
              'area': [area_to_user_readable(
                  compute_area_from_4326(self.origin_footprint))],
              'geometry': [self.origin_footprint]}
        d2 = {'name': ['reworked'],
              'point no': self.reworked_points(),
              'area': [area_to_user_readable(
                  compute_area_from_4326(self.reworked_footprint))],
              'geometry': [self.reworked_footprint]}

        gdf1 = gpd.GeoDataFrame(d1, crs='epsg:4326')
        gdf2 = gpd.GeoDataFrame(d2, crs='epsg:4326')

        intersect = gpd.overlay(gdf1, gdf2, how='intersection')
        union = gpd.overlay(gdf1, gdf2, how='union')
        diff = gpd.overlay(union, intersect, how='difference')

        added = gpd.overlay(gdf2, gdf1, how='difference')
        removed = gpd.overlay(gdf1, gdf2, how='difference')

        m = gdf1.explore(
            color='green',
            tooltip=True,
            name="Origin Footprint")

        gdf2.explore(m=m, color='blue', name='Reworked Footprint')

        diff['name'] = 'Full Difference'
        diff['area'] = area_to_user_readable(
            compute_area_from_4326(diff.geometry.values))
        diff.explore(m=m, color='red', name='Full Difference',
                     tooltip=['name', 'area'])

        added['name'] = "Added Part"
        added['area'] = area_to_user_readable(compute_area_from_4326(
            added.geometry.values))
        added.explore(m=m, color='black', name='Added Part',
                      tooltip=['name', 'area'])

        removed['name'] = "Removed Part"
        removed['area'] = area_to_user_readable(compute_area_from_4326(
            removed.geometry.values))
        removed.explore(m=m, color='black', name='Removed Part',
                        tooltip=['name', 'area'])

        folium.LayerControl().add_to(m)  # use folium to add layer control
        return m


def _compare_footprints(
        geometry1: Geometry, geometry2: Geometry) -> FootprintStatistics:
    stats = FootprintStatistics(geometry1, geometry2)
    try:
        stats.difference = shapely.difference(geometry1, geometry2)
    except Exception as e:
        logger.error('Cannot compute footprints difference', e)
    return stats


def _compute_simplify(
        geometry: Geometry, tolerance: float) -> FootprintStatistics:
    """
    Compute the simplification of the passed geometry and set the tolerance
    statistic info.
    :param geometry: geometry to simplify
    :param tolerance: the expected tolerance
    """
    simplified_geometry = footprint_facility.simplify(geometry, tolerance)
    stats = _compare_footprints(geometry, simplified_geometry)
    stats.tolerance = tolerance
    return stats


def _compute_convex_hull(geometry: Geometry) -> FootprintStatistics:
    """
    Compute the convex hull of the passed geometry and statistic info.
    :param geometry: geometry to simplify
    """
    if isinstance(geometry, shapely.geometry.MultiPolygon):
        hull = []
        for geo in geometry.geoms:
            hull.append(geo.convex_hull)
        simplified_geometry = MultiPolygon(hull)
    else:
        simplified_geometry = getattr(geometry, 'convex_hull')

    return _compare_footprints(geometry, simplified_geometry)


def main_stats():  # pragma: no cover
    main_parser = argparse.ArgumentParser(
        description='Compare footprint optimization results')
    main_parser.add_argument(
        '-f', metavar='orig_footprint', required=True,
        help='The footprint to be optimized')
    main_parser.add_argument(
        '-o', metavar='output', default='output.html',
        help='The html output of the results')
    main_parser.add_argument(
        '--format', default='wkt', choices=['wkt', 'geojson'],
        help='The format of the passed footprint (default=wkt)')
    main_parser.add_argument(
        '-r', action='store_true',
        help='The passed footprint shall be reworked before optimization')
    main_parser.add_argument(
        '-a', default='simplify', choices=['simplify', 'convex_hull'],
        help='Select the footprint simplification algorithm')
    main_parser.add_argument(
        '-t', metavar='tolerance', action='append', required=True, type=float,
        help='the simlify tolerance expected (can be multiple)')

    args = main_parser.parse_args()
    if args.format == 'wkt':
        orig_footprint = wkt.loads(args.f)
    elif args.format == 'geojson':
        orig_footprint = shape(geojson.loads(args.f))
    else:
        raise ValueError("Bad footprint format parameter")

    if args.r:
        orig_footprint = footprint_facility.rework_to_polygon_geometry(
            orig_footprint)

    output_file = args.o

    if args.a == 'simplify':
        if hasattr(args, 't'):
            print('simplify')
            print(f'tolerance {args.t}')
            stats = _compute_simplify(orig_footprint, tolerance=args.t[0])
            stats.map().save(output_file)
        else:
            raise main_parser.error(
                "Tolerance value must be defined for simplify algorithm.")
    elif args.o == 'convex_hull':
        print('convex_hull')
        stats = _compute_convex_hull(orig_footprint)
        stats.map().save(output_file)
    else:
        raise main_parser.error(f"Unknown algorithm '{args.a}'")


if __name__ == '__main__':  # pragma: no cover
    main_stats()
