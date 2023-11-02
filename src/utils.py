from os import walk
from os.path import join
from csv import reader
from pygame import image


def import_csv_layout(path) -> list:
    level_map = []
    with open(path) as file:
        layout = reader(file, delimiter=",")
        for row in layout:
            level_map.append(list(row))
    return level_map


def import_folder(path, isObject=False) -> list:
    surface_list = []
    filenames = []
    for _, _, files in walk(path):
        for filename in files:
            filenames.append(filename)

    if isObject:
        # Sort the filenames numerically
        filenames.sort(key=lambda x: int(x.split(".")[0]))

    for filename in filenames:
        full_path = join(path, filename)
        image_surface = image.load(full_path).convert_alpha()
        surface_list.append(image_surface)

    return surface_list
