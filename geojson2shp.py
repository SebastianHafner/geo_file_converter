import argparse
import geopandas as gpd
from pathlib import Path


def argument_parser():

    parser = argparse.ArgumentParser(description="Download Args")
    parser.add_argument('-geojson', "--geojson-file", dest='geojson_file', default="", required=True, metavar="FILE",
                        help="path to geojson file")
    parser.add_argument('-output', "--output-path", dest='shape_file', default="input", required=False, metavar="FILE",
                        help="output path of shape file")

    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )

    return parser


def convert_geojson2shp(args):
    geojson_file = Path(args.geojson_file)
    if not geojson_file.exists():
        raise Exception(f'file {geojson_file} does not exist')

    output_path = args.shape_file
    output_path = Path(output_path) if not output_path == 'input' else geojson_file.parent
    if not output_path.exists():
        raise Exception(f'directory {output_path} does not exist')

    output_path = output_path / geojson_file.stem
    if not output_path.exists():
        output_path.mkdir()

    print(f'reading in {geojson_file}...')
    gdf = gpd.read_file(geojson_file)

    print(f'saving to {output_path}...')
    shape_file = output_path / f'{geojson_file.stem}.shp'
    gdf.to_file(shape_file)
    print(f'done')


if __name__ == '__main__':

    parser = argument_parser()
    args = parser.parse_known_args()[0]

    convert_geojson2shp(args)
