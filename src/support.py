from os import walk
import pygame as pg


def import_folder(path, is_alpha: bool = True):
    surf_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = path + "/" + image
            image_surf = (
                pg.image.load(full_path).convert_alpha()
                if is_alpha
                else pg.image.load(full_path).convert()
            )
            surf_list.append(image_surf)
    return surf_list
