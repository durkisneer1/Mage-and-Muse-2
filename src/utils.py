from os import walk
import pygame as pg


image_load = pg.image.load
pg_surface = pg.Surface


def import_folder(
    path: str, is_alpha: bool = True, scale: float = 1, highlight: bool = False
) -> list[pg.Surface]:
    surf_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = path + "/" + image
            surface = import_image(full_path, is_alpha, scale, highlight)
            surf_list.append(surface)
    return surf_list


def import_image(
    path: str, is_alpha: bool = True, scale: float = 1, highlight: bool = False
) -> pg.Surface:
    image_surf = (
        pg.image.load(path).convert_alpha()
        if is_alpha
        else pg.image.load(path).convert()
    )

    if scale != 1 and scale > 0:
        image_surf = pg.transform.scale_by(image_surf, scale)
    if highlight:
        image_surf.fill((40, 40, 40, 0), special_flags=pg.BLEND_RGB_ADD)

    return image_surf


def new_image_load(*args, **kwargs):
    print("Image loaded:", args[0])
    return image_load(*args, **kwargs)


def new_surface(*args, **kwargs):
    print("Surface created")
    return pg_surface(*args, **kwargs)


pg.image.load = new_image_load
pg.Surface = new_surface
