from os import walk
import pygame as pg


image_load = pg.image.load
pg_surface = pg.Surface


def import_folder(
    path: str, is_alpha: bool = True, scale: float = 1
) -> list[pg.Surface]:
    surf_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = path + "/" + image
            image_surf = (
                pg.image.load(full_path).convert_alpha()
                if is_alpha
                else pg.image.load(full_path).convert()
            )
            if scale != 1:
                image_surf = pg.transform.scale_by(image_surf, scale)
            surf_list.append(image_surf)
    return surf_list


def new_image_load(*args, **kwargs):
    print("Image loaded:", args[0])
    return image_load(*args, **kwargs)


def new_surface(*args, **kwargs):
    print("Surface created")
    return pg_surface(*args, **kwargs)


pg.image.load = new_image_load
pg.Surface = new_surface
