from os import walk
from csv import reader
from pygame import image


def import_csv_layout(path) -> list:
    level_map = []
    with open(path) as file:
        layout = reader(file, delimiter=",")
        for row in layout:
            level_map.append(list(row))
    return level_map


def import_folder(path) -> list:
    surface_list = []
    for _, __, filenames in walk(path):
        for filename in filenames:
            full_path = path + "/" + filename
            image_surface = image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list
