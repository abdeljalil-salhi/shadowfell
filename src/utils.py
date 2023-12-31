from os import walk
from os.path import join
from csv import reader
from pygame import image, transform

from settings import TILE_SIZE


def import_csv_layout(path) -> list:
    level_map = []
    with open(path) as file:
        layout = reader(file, delimiter=",")
        for row in layout:
            level_map.append(list(row))
    return level_map


def import_folder(path, isObject=False, forceTransform=False, isParticle=False) -> list:
    surface_list = []
    filenames = []
    for _, _, files in walk(path):
        for filename in files:
            filenames.append(filename)

    if isObject or isParticle:
        # Sort the filenames numerically
        filenames.sort(key=lambda x: int(x.split(".")[0]))

    for filename in filenames:
        image_surface = image.load(join(path, filename)).convert_alpha()
        if isObject:
            width, height = image_surface.get_size()
            if height > width:
                image_surface = transform.scale(
                    image_surface, (TILE_SIZE, TILE_SIZE * 2)
                )
            else:
                image_surface = transform.scale(
                    image_surface, (TILE_SIZE * 2, TILE_SIZE * 2)
                )
        elif forceTransform:
            image_surface = transform.scale(image_surface, (TILE_SIZE, TILE_SIZE))
        surface_list.append(image_surface)

    return surface_list
