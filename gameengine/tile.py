import pygame
import json
import os
import logging
import math
import sys

logging.getLogger().setLevel("INFO")

##################################################################
# Tiles
##################################################################

class Tile:
    WALL = 1
    STAIR = 2
    DANGER = 4
    ALL_FLAGS = 255

    def __init__(self, surface, tile_id, flags):
        self.surface = surface
        self.anim_surfaces = []
        self.tileid = tile_id
        self.anim_counter = 0
        self.frame_delay = 0
        self.flags = 0
        self.flags |= self.WALL if "wall" in flags.lower() else 0
        self.flags |= self.STAIR if "stair" in flags.lower() else 0
        self.flags |= self.DANGER if "stair" in flags.lower() else 0

    def has_flags(self, flags):
        return self.flags & flags

    def tick(self):
        if self.frame_delay > 0:
            self.frame_delay -= 1
            return
        else:
            self.frame_delay = 15

        if len(self.anim_surfaces) == 0:
            return
        else:
            self.anim_counter += 1
            self.anim_counter = self.anim_counter % len(self.anim_surfaces)
            self.surface = self.anim_surfaces[self.anim_counter]


class Tileset:
    def __init__(self):
        self.idmap = {}
        self.ids_anim = []
        self.tilecount = 0
        self.tileheight = 0
        self.tilewidth = 0
        self.tiles = []

    def load(self, path, first_gid=0):
        """ Tileset erzeugen über Filepath
            'firstgid' wird bei mehreren Tilesets in einer Map enthalten sind.
        """
        logging.info(f"Tileset.load: Aufruf Tileset.load('{path}', first_gid={first_gid})")
        tileset_json = json.load(open(path))

        # Handelt es sich um ein Tileset mit Sprites statt Tiles?
        if "image" not in tileset_json.keys():
            return  # wird nicht eingelesen
        logging.info(f'Tileset.load: Lade Tileset "{path}"')
        columns = tileset_json["columns"]
        rows = math.ceil(tileset_json["tilecount"] / columns)
        logging.info(f"Tileset.load: Columns={columns}, Rows={rows}")
        self.tilecount = tileset_json["tilecount"]
        self.tileheight = tileset_json["tileheight"]
        self.tilewidth = tileset_json["tilewidth"]
        try:
            fname = os.path.join(os.path.dirname(path), tileset_json["image"])
            self.img = pygame.image.load(fname)
        except FileNotFoundError:
            logging.error(f"Tileset.load: Fehler. Tileset '{fname}' nicht gefunden")
            sys.exit()
        self.img.convert_alpha()

        # tile_info_json enthält für einige Tiles Zusatzinfos (Animationen oder Typ-Informationen ("WALL" etc.))
        if "tiles" in tileset_json:
            tiles_list_json = tileset_json["tiles"]
        else:
            tiles_list_json = []

        anim_tiles_json = []
        # Alle
        for row in range(rows):
            for col in range(columns):
                # ID berechnen
                tile_id = row * columns + col
                rect = pygame.Rect(self.tilewidth * col, self.tileheight * row, 16, 16)
                sf = pygame.Surface((self.tilewidth, self.tileheight), pygame.SRCALPHA)
                sf.blit(self.img, (0, 0), rect)

                # Ist die aktuelle tile_id in der Tiles_List enthalten?
                if search := [x for x in tiles_list_json if x["id"] == tile_id]:
                    js_tile = search[0]
                else:
                    # Keine
                    js_tile = None

                # Animation-Tiles erstmal zurückstellen...
                if js_tile and "animation" in js_tile.keys():
                    anim_tiles_json.append(js_tile)
                    continue

                # Tiles mit Type-Flags
                flags = ""
                if js_tile and "type" in js_tile.keys():
                    flags = js_tile["type"].lower()

                t = Tile(sf, tile_id + first_gid, flags)
                self.tiles.append(t)
                self.idmap[tile_id + first_gid] = t

        # Jetzt die Animation-Tiles durchgehen und erstellen
        for js_tile in anim_tiles_json:
            tile_id = js_tile["id"]
            # Flags berücksichtigen
            flags = ""
            if js_tile and "type" in js_tile.keys():
                flags = js_tile["type"].lower()
            frame_ids = []
            # print(js_tile.keys())
            for frame in js_tile["animation"]:
                duration = frame["duration"]
                frame_id = frame["tileid"]
                frame_ids.append(frame_id)

            # Erste Surface
            sf = self.get(frame_ids[0] + first_gid).surface
            # Anim-Tile erstellen mit erstem Frame
            t = Tile(sf, tile_id + first_gid, flags)
            # Surface-Liste der Animation-Frames erstellen
            t.anim_surfaces = [self.get(i + first_gid).surface for i in frame_ids]
            self.tiles.append(t)
            self.idmap[tile_id + first_gid] = t
            # Tiles in ids_anim erhalten ticks
            self.ids_anim.append(t)

        logging.info(f"Tileset.load: Tileset '{path}' loaded successfully. Tilecount={self.tilecount} Number of anim_tiles: {len(self.ids_anim)}")

    def get(self, tileid):
        if tileid in self.idmap.keys():
            return self.idmap[tileid]
        else:
            return None

    def tick(self):
        for _ in self.ids_anim:
            _.tick()

class TilemapObject:
    def __init__(self, type, rect, subtype, id):
        self.type = type  # "Point", "Rect"
        self.r = rect
        self.subtype = subtype
        self.id = id


class Tilemap:
    def __init__(self, game):
        self.game = game
        self.tileheight = 0
        self.tilewidth = 0
        self.width = 0
        self.height = 0
        self.backgroundcolor = pygame.Color("black")
        self.mapdata = []
        self.object_layers = []
        self.tilesets = []

        self.last_collision_rects = []

    def load(self, filepath: str) -> None:
        # global triggers

        """Lädt eine Tilemap im json-Format (Tiled)"""
        dirname = os.path.dirname(filepath)
        tilemap_json = json.load(open(filepath))

        self.tileheight = tilemap_json["tileheight"]
        self.tilewidth = tilemap_json["tilewidth"]
        self.width = tilemap_json["width"]
        self.height = tilemap_json["height"]

        if "backgroundcolor" in tilemap_json:
            self.backgroundcolor = pygame.Color(tilemap_json["backgroundcolor"])

        self.mapdata = []
        self.tilesets = []

        self.last_collision_rects = []

        # Tilesets einlesen
        for ts in tilemap_json["tilesets"]:
            if ts:
                tileset = Tileset()
                tileset.load(os.path.join(dirname, ts["source"]), ts["firstgid"])
                self.tilesets.append(tileset)
            else:
                logging.error(f"Tilemap.load: No tileset in Tilemap..")

        for layer in tilemap_json["layers"]:
            name = layer["name"]

            #
            # Tile - Layer
            #
            if layer["type"] == "tilelayer":
                if self.mapdata:
                    # Can read only one tilelayer yet..
                    continue
                map_temp = layer["data"]
                self.mapdata = []
                for y in range(self.height):
                    row = []
                    for x in range(self.width):
                        row.append(self.get_tile_from_id(map_temp[x + (self.width * y)]))
                        # self.mapdata.append(map_temp[self.width * y:self.width * y + self.width])
                    self.mapdata.append(row)

                logging.info(f"Tilemap.load: Tilemap-Layer '{name}' of size {self.width}*{self.height} imported..")

            #
            # Object - Layer
            #
            elif layer["type"] == "objectgroup":
                for o in layer["objects"]:
                    if "point" in o.keys():
                        self.object_layers.append(TilemapObject("Point", pygame.Rect(o["x"],o["y"],0,0), o["type"], o["id"]))

                    elif "ellipse" in o.keys():
                        logging.info("Ellipse überlesen...")
                        continue

                    elif "polygon" in o.keys():
                        logging.info("Polygon überlesen...")
                        continue
                    elif "text" in o.keys():
                        logging.info("Text überlesen")
                        continue
                    else:
                        self.object_layers.append(TilemapObject("Rect", pygame.Rect(o["x"],o["y"],o["width"],o["height"]), o["type"], o["id"]))
                        logging.info("Polygon überlesen...")



        logging.info(f"Tilemap.load: Tilemap width={self.width} height={self.height}")
        logging.info(f"Tilemap.load: Tilemap {filepath} loaded successfully.")

    def get(self, celx, cely):
        return int(math.floor(celx / self.tilewidth)), int(math.floor(cely / self.tileheight))

    def __get_tile_rect(self, celx, cely):
        return pygame.rect.Rect(celx * self.tilewidth, cely * self.tileheight, self.tilewidth, self.tileheight)

    def get_collision_tiles(self, rect, flags=Tile.ALL_FLAGS) -> list[pygame.Rect]:
        """"Liefert zu einem Rechteck eine Liste aller kollidierenden Rects zurück mit gegebenen Flags"""

        collision_tiles = []
        topleft = self.get(rect.topleft[0], rect.topleft[1])
        bottomright = self.get(rect.x + rect.w - 1, rect.y + rect.h - 1)

        for y in range(topleft[1], bottomright[1] + 1):
            for x in range(topleft[0], bottomright[0] + 1):
                tile = self.mapdata[y][x]
                if tile and tile.has_flags(flags):  # not empty Room
                    collision_tiles.append(self.__get_tile_rect(x, y))
        self.last_collision_rects = collision_tiles
        return collision_tiles

    def get_tile_from_id(self, tid: int):
        if tid == 0:
            return None
        for ts in self.tilesets:
            if tile := ts.get(tid):
                return tile
        logging.error(f"TileId {tid} from map not found..")
        sys.exit()

    def tick(self):
        for _ in self.tilesets:
            _.tick()

    def draw(self, surface, delta, camera):
        first_tile_x = math.floor(camera.x / self.tilewidth)
        first_tile_y = math.floor(camera.y / self.tileheight)
        tiles2draw_hor = math.floor((camera.w / self.tilewidth)) + 2
        tiles2draw_vert = math.floor((camera.h / self.tilewidth)) + 2

        offset_x = abs(math.fmod(camera.x, self.tilewidth))
        if camera.x < 0 and offset_x > 0:
            offset_x = self.tilewidth - offset_x

        offset_y: float = abs(math.fmod(camera.y, self.tileheight))
        if camera.y < 0 and offset_y > 0:
            offset_y = self.tileheight - offset_y

        for step_y in range(tiles2draw_vert):
            for step_x in range(tiles2draw_hor):
                tile_x = first_tile_x + step_x
                tile_y = first_tile_y + step_y
                draw_pos_x = (step_x * self.tilewidth) - offset_x
                draw_pos_y = (step_y * self.tileheight) - offset_y
                if tile_y < 0 or tile_y > (self.height - 1) or tile_x < 0 or tile_x > (self.width - 1):
                    pass
                    # Grünes Gitter außerhalb der Map zeichnen (Debug)
                    if self.game.debug:
                      pygame.draw.rect(surface, pygame.Color("green"),
                                      (int(draw_pos_x), int(draw_pos_y), self.tilewidth, self.tileheight), 1)
                else:
                    if tile := self.mapdata[tile_y][tile_x]:
                        surface.blit(tile.surface, (int(draw_pos_x), int(draw_pos_y)))
                if self.game.debug:
                    pygame.draw.line(surface, "green", (draw_pos_x, draw_pos_y), (draw_pos_x, draw_pos_y))

        if self.game.debug:
            for _ in self.object_layers:
                if _.type == "Rect":
                    pygame.draw.rect(surface, "red", _.r.move(-camera.x,-camera.y), 1)
                if _.type == "Point":
                    pygame.draw.rect(surface, "blue", _.r.move(-camera.x,-camera.y), 1)
