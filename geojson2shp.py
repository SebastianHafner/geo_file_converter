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


def convert_geojson2shp(geojson_file: Path, output_path: Path = None):
    if not geojson_file.exists():
        raise Exception(f'file {geojson_file} does not exist')

    output_path = geojson_file.parent if output_path is None else output_path
    if not output_path.exists():
        raise Exception(f'directory {output_path} does not exist')

    output_path = output_path / geojson_file.stem
    if not output_path.exists():
        output_path.mkdir()

    print(f'reading in {geojson_file}...')
    gdf = gpd.read_file(str(geojson_file))

    print(f'saving to {output_path}...')
    shape_file = output_path / f'{geojson_file.stem}.shp'
    gdf.to_file(str(shape_file))
    print(f'done')


def run_geojson2shp_converter(args):
    geojson_file = Path(args.geojson_file)
    output_path = args.shape_file

    if geojson_file.is_dir():
        directory = geojson_file
        print(f'converting all files in directory {directory}')
        geojson_files = [f for f in directory.iterdir() if f.is_file()]
        for geojson_file in geojson_files:
            convert_geojson2shp(geojson_file)
    else:
        output_path = Path(output_path) if not output_path == 'input' else geojson_file.parent
        convert_geojson2shp(geojson_file, output_path)


if __name__ == '__main__':

    parser = argument_parser()
    args = parser.parse_known_args()[0]

    run_geojson2shp_converter(args)
