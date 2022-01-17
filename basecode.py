import math
from enum import IntFlag

import pygame
from pygame.font import *
import pygame.draw
import sys
from random import randint
from typing import List

import logging
import os
import json

import ctypes
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()


# Globals
screen = pygame.display.set_mode((480, 256),pygame.SCALED|pygame.RESIZABLE, vsync=1)

logging.getLogger().setLevel("INFO")


## PIPRINT
font = Font("mago3.ttf", 16, bold=False, italic=False)
pico_colors=["black", "darkblue", "darkred", "darkgreen",
             "brown", "darkgrey", "lightgrey", "white",
             "red", "orange", "yellow", "green",
             "blue", "grey", "pink", "lightpink"]
last_color = 7

print_map ={}

def piprint(text, x, y, color="white"):
    if (text, color) in print_map.keys():
        screen.blit(print_map[(text, color)], (x,y))
    else:
        s = font.render(text, False, color)
        print_map[(text, color)] = s
        screen.blit(s, (x,y))

## circ

def circ(x, y, r, color=7, surface=screen):
    pygame.draw.circle(surface, pico_colors[color % 16], (x, y), r, width=1)

def circfill(x, y, r, color=7, surface=screen):
    pygame.draw.circle(surface,  pico_colors[color % 16], (x, y), r, width=0)

class Controller:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.menu = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def tick(self):
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_RETURN]:
            self.a += 1
        else:
            self.a = 0

        if pygame.key.get_pressed()[pygame.K_s]:
            self.b += 1
        else:
            self.b = 0

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.up += 1
        else:
            self.up = 0

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.down += 1
        else:
            self.down = 0

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.left += 1
        else:
            self.left = 0

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.right += 1
        else:
            self.right = 0

class Actor:
    def __init__(self):
        self.dirty = False

    def tick(self):
        pass

    def draw(self):
        pass

    def destroy(self):
        self.dirty = True

class Camera(Actor):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.w = 480
        self.h = 256
        self.r = pygame.Rect(0,0,480,256)

    def follow(self, fobj):
        self.follow_obj = fobj

    def tick(self):
        if self.follow_obj:
            self.x = self.follow_obj.r.centerx - 240
            #self.y = self.follow_obj.r.centery - 128

# Globals ################


class TestScene2(Actor):
    """ Test-Scene mit Schneeflocken"""
    def __init__(self):
        super().__init__()
        self.stars = []
        for i in range(100):
            self.stars.append((randint(2, 480), randint(2, 256)))

    def tick(self):
        for i in range(len(self.stars)):
            s = self.stars[i]
            if s[1] > 270:
                s = (s[0], 0)
            else:
                s = (s[0], s[1]+s[0] % 16/26+0.2) # unterschiedl. Geschw.
            self.stars[i] = s

    def draw(self):
        #piprint(surface, "TestScene2", (380+self.x, 10), "green")
        for i in range(len(self.stars)):
            pygame.draw.circle(screen,"white", self.stars[i], 2, 2)

class Menu(Actor):
    def __init__(self):
        super().__init__()
        self.pos = 0
        self.items = []
        pass

    def tick(self):
        # Clicked
        if controller.a == 1:
            self.clicked(self.items[self.pos])

        #Up
        if controller.down == 1:
            self.pos += 1
        if self.pos >= len(self.items):
            self.pos = 0
        #Down
        if controller.up  == 1:
            self.pos -= 1
        if self.pos == -1:
            self.pos = len(self.items)-1

    def draw(self, sf):
        x = 40
        y = 40
        yd = 15

        num = 0
        for item in self.items:
            if num == self.pos:
                piprint(">", x + 2, y, "white")
                piprint(item, x + 10, y, "white")
            else:
                piprint(item, x + 10, y, "red")
            y += yd
            num += 1
    def clicked(self, item):
        pass

class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.items = ["STORY-MODE", "MULTIPLAYER", "OPTIONS", "EDITOR", "EXIT"]

    def clicked(self, item):
        if item == "EXIT":
            sys.exit()

class OptionsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.items = ["SCENE 1", "SCENE 2", "TOGGLE FULLSCREEN", "EXIT"]
    def clicked(self, item):
        if item == "TOGGLE FULLSCREEN":
            pygame.display.toggle_fullscreen()
        if item == "EXIT":
            sys.exit()

##################################################################
# Tiles
##################################################################

class Tile:
    WALL        = 1
    STAIR       = 2
    DANGER      = 4
    ALL_FLAGS   = 255

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

    def has_flags(self,flags):
        return self.flags & flags

    def tick(self):
        if self.frame_delay > 0:
            self.frame_delay -= 1
            return
        else:
            self.frame_delay = 5

        if len(self.anim_surfaces) == 0:
            return
        else:
            self.anim_counter += 1
            self.anim_counter=self.anim_counter % len(self.anim_surfaces)
            self.surface = self.anim_surfaces[self.anim_counter]

class Tileset:
    def __init__(self):
        self.idmap = {}
        self.ids_anim = []
        self.columns = 0
        self.rows = 0
        self.tilecount = 0
        self.tileheight = 0
        self.tilewidth = 0
        self.tiles = []

    def load(self, path, first_gid=0):
        """ Tileset erzeugen über Filepath
            'firstgid' wird bei mehreren Tilesets in einer Map enthalten sind.
        """
        tileset_json = json.load(open(path))
        logging.info(f'Lade Tileset "{path}"')
        self.columns = tileset_json["columns"]
        self.rows    = math.floor(tileset_json["tilecount"]/self.columns)
        self.tilecount = tileset_json["tilecount"]
        self.tileheight = tileset_json["tileheight"]
        self.tilewidth  = tileset_json["tilewidth"]
        try:
            fname = os.path.join(os.path.dirname(path), tileset_json["image"])
            self.img = pygame.image.load(fname)
        except FileNotFoundError:
            print(f"Fehler. Datei '{fname}' nicht gefunden")
            sys.exit()
        self.img.convert_alpha()

        if "tiles" in tileset_json:
            tiles_json = tileset_json["tiles"]
        else:
            tiles_json = []

        js_anim_tiles = []
        for row in range(self.rows):
            for col in range(self.columns):
                tile_id = row * self.columns + col
                rect = pygame.Rect(self.tilewidth*col, self.tileheight*row, 16, 16)
                sf = pygame.Surface((self.tilewidth, self.tileheight), pygame.SRCALPHA)
                sf.blit(self.img, (0, 0), rect)

                # Tile finden mit der richtigen id (Nur Tiles mit type oder Anim sind in json enthalten)
                if search := [x for x in tiles_json if x["id"] == tile_id]:
                    js_tile = search[0]
                else:
                    js_tile = None

                # Animation-Tiles erstmal zurückstellen...
                if js_tile and "animation" in js_tile.keys():
                    js_anim_tiles.append(js_tile)
                    continue

                # Tiles mit Type-Flags
                flags = ""
                if js_tile and "type" in js_tile.keys():
                    flags = js_tile["type"].lower()

                t = Tile(sf, tile_id + first_gid, flags)
                self.tiles.append(t)
                self.idmap[tile_id + first_gid] = t

        # Jetzt die Animation-Tiles erstellen
        for js_tile in js_anim_tiles:
            tile_id = js_tile["id"]
            # Flags berücksichtigen
            flags = ""
            if js_tile and "type" in js_tile.keys():
                flags = js_tile["type"].lower()
            frame_ids = []
            #print(js_tile.keys())
            for frame in js_tile["animation"]:
                duration = frame["duration"]
                frame_id = frame["tileid"]
                frame_ids.append(frame_id)

            # Erste Surface
            sf = self.get(frame_ids[0]+first_gid).surface
            # Anim-Tile erstellen mit erstem Frame
            t = Tile(sf, tile_id + first_gid, flags)
            # Surface-Liste der Animation-Frames erstellen
            t.anim_surfaces = [self.get(i+first_gid).surface for i in frame_ids]
            self.tiles.append(t)
            self.idmap[tile_id + first_gid] = t
            # Tiles in ids_anim erhalten ticks
            self.ids_anim.append(t)

        logging.info(f"Tileset '{path}' loaded successfully.")
        logging.info(f"Tileset rows={self.rows}, columns={self.columns}, {len(self.tiles)} Elements")

    def get(self, tileid):
        if tileid in self.idmap.keys():
            return self.idmap[tileid]
        else:
            return None

    def tick(self):
        for _ in self.ids_anim:
            _.tick()


class Tilemap:
    def __init__(self):
        self.tileheight = 0
        self.tilewidth  = 0
        self.width = 0
        self.height = 0
        self.backgroundcolor = pygame.Color("black")
        self.mapdata = []
        self.tilesets = []

        self.last_collision_rects = []

    def load(self, filepath:str) -> None:
        """Lädt eine Tilemap im json-Format (Tiled)"""
        dirname = os.path.dirname(filepath)
        tilemap_json = json.load(open(filepath))

        self.tileheight = tilemap_json["tileheight"]
        self.tilewidth  = tilemap_json["tilewidth"]
        self.width = tilemap_json["width"]
        self.height = tilemap_json["height"]

        if "backgroundcolor" in tilemap_json:
            self.backgroundcolor = pygame.Color(tilemap_json["backgroundcolor"])

        self.mapdata = []
        self.tilesets = []

        self.last_collision_rects = []


        # Demo Git-Kommentar

        # Tilesets einlesen
        for ts in tilemap_json["tilesets"]:
            if ts:
                tileset = Tileset()
                tileset.load(os.path.join(dirname, ts["source"]), ts["firstgid"])
                self.tilesets.append(tileset)
            else:
                logging.error(f"No tileset in Tilemap..")

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
                        row.append(self.get_tile_from_id(map_temp[x+(self.width*y)]))
                        #self.mapdata.append(map_temp[self.width * y:self.width * y + self.width])
                    self.mapdata.append(row)

                logging.info(f"Tilemap-Layer '{name}' of size {self.width}*{self.height} imported..")

            #
            # Object - Layer
            #
            # elif layer["type"] == "objectgroup":
            #     for obj in layer["objects"]:
            #         if obj["type"] == "POINT":
            #             self.scene.add(PositionNode(scene, obj["name"], obj["x"], obj["y"]))
            #         elif obj["type"] == "TRIGGER_RECT":
            #             self.scene.add(TriggerRectNode(scene, obj["name"], pygame.Rect(obj["x"], obj["y"], obj["width"], obj["height"])))
            #         elif obj["type"] == "CIRCLESAW":
            #             self.scene.add(CircleSaw(scene, (obj["x"], obj["y"])))
            #         else:
            #             pass
            #             #t = layer["type"]
            #             #logging.warning(f'Unknown layer-Type: {layer["type"]}')

        logging.info(f"Tilemap {filepath} loaded successfully.")
        logging.info(f"Tilemap width={self.width} height={self.height}")

    def get(self, celx, cely):
        return int(math.floor(celx / self.tilewidth)), int(math.floor(cely / self.tileheight))

    def __get_tile_rect(self, celx, cely):
        return pygame.rect.Rect(celx * self.tilewidth, cely * self.tileheight, self.tilewidth, self.tileheight)

    def get_tiles(self, rect, flags=Tile.ALL_FLAGS) -> List[pygame.Rect]:
        """"Liefert zu einem Rechteck eine Liste aller kollidierenden Rects zurück mit gegebenen Flags"""

        collision_tiles = []
        topleft = self.get(rect.topleft[0], rect.topleft[1])
        bottomright = self.get(rect.x + rect.w - 1, rect.y + rect.h - 1)

        for y in range(topleft[1], bottomright[1]+1):
            for x in range(topleft[0], bottomright[0]+1):
                tile = self.mapdata[y][x]
                if tile and tile.has_flags(flags):  # not empty Room
                    collision_tiles.append(self.__get_tile_rect(x, y))
        self.last_collision_rects = collision_tiles
        return collision_tiles

    def get_tile_from_id(self, tid:int):
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

    def draw(self):
        first_tile_x = math.floor(camera.x/self.tilewidth)
        first_tile_y = math.floor(camera.y/self.tileheight)
        tiles2draw_hor  = math.floor((camera.w / self.tilewidth)) + 2
        tiles2draw_vert = math.floor((camera.h / self.tilewidth)) + 2

        offset_x = abs(math.fmod(camera.x, self.tilewidth))
        if camera.x < 0 and offset_x > 0:
            offset_x = self.tilewidth-offset_x

        offset_y: float = abs(math.fmod(camera.y, self.tileheight))
        if camera.y < 0 and offset_y > 0:
            offset_y = self.tileheight-offset_y

        for step_y in range(tiles2draw_vert):
            for step_x in range(tiles2draw_hor):
                tile_x = first_tile_x + step_x
                tile_y = first_tile_y + step_y
                draw_pos_x = (step_x*self.tilewidth) - offset_x
                draw_pos_y = (step_y * self.tileheight) - offset_y
                if tile_y < 0 or tile_y > (self.height-1) or tile_x < 0 or tile_x > (self.width-1):
                    # Grünes Gitter außerhalb der Map zeichnen (Debug)
                    if debug:
                        pygame.draw.rect(screen, pygame.Color("green"), (int(draw_pos_x),int(draw_pos_y), self.tilewidth, self.tileheight),1)
                else:
                    if tile := self.mapdata[tile_y][tile_x]:
                        screen.blit(tile.surface, (int(draw_pos_x), int(draw_pos_y)))
                if debug:
                     pygame.draw.line(screen, "green", (draw_pos_x, draw_pos_y), (draw_pos_x, draw_pos_y))


######################################################################
# Für Player-Sprites, Gegner, bewegliche Objekte


class TilemapActor(Actor):
    def __init__(self, x, y, w, h, tmap):
        super().__init__()
        self.r = pygame.Rect(x, y, w, h)
        self.tmap = tmap
        self.xa = 0.0
        self.ya = 0.4  # Erdbeschleunigung
        self.xs = 0.0
        self.ys = 0.0

    def move(self, xd, yd, ignore_stairs=False):
        blocked = False
        if xd:
            if not self.move2(xd, 0):
                blocked = True
                self.xs = 0.0
        if yd:
            if not self.move2(0,yd):
                blocked = True
                self.ys = 0.0
        return not blocked

    def move2(self, xd, yd):
        if xd != 0 and yd != 0:
            raise Exception("Move2 kann pro Aufruf nur 1 Achse bewegen")
        tr = self.r.move(xd, yd)  # tr=target_rect
        blocked = False
        if xd != 0 or yd != 0:
            for wall_tile in self.tmap.get_tiles(tr, Tile.WALL):

                blocked = True
                # Kollision rechts?
                if xd > 0:
                    if tr.right > wall_tile.left:
                        tr.right = wall_tile.left
                # Kollision links?
                if xd < 0:
                    if tr.left < wall_tile.right:
                        tr.left = wall_tile.right
                # Kollision Boden?
                if yd > 0:
                    if tr.bottom > wall_tile.top:
                        tr.bottom = wall_tile.top
                # Kollision mit Decke?
                if yd < 0:
                    if tr.top < wall_tile.bottom:
                        tr.top = wall_tile.bottom
            if yd > 0:
                # Fußstück für Kollision berechnen
                tr_stair = pygame.Rect(tr.x, tr.y+tr.h-4, tr.w, 4)
                for stair_tile in self.tmap.get_tiles(tr_stair, Tile.STAIR):
                    stair_tile.h = 4
                    if tr_stair.colliderect(stair_tile):
                        tr.bottom = stair_tile.top
        self.r = tr
        return not blocked

    def on_floor(self):
        """ detects ground """
        tr = pygame.Rect(self.r.x, self.r.y+self.r.h, self.r.w, 1)
        for tile_rect in self.tmap.get_tiles(tr, Tile.WALL):
            tile_rect.h = 1
            if tr.colliderect(tile_rect):
                return True
        return False
    def on_stair(self):
        """ detects ground """
        tr = pygame.Rect(self.r.x, self.r.y+self.r.h, self.r.w, 1)
        for tile_rect in self.tmap.get_tiles(tr, Tile.STAIR):
            tile_rect.h = 1
            if tr.colliderect(tile_rect):
                return True
        return False

    def tick(self):
        if not self.on_floor():
            self.ys += self.ya
        if self.ys > 7.0:
            self.ys = 7.0
        self.move(int(self.xs), int(self.ys))

    def draw(self):
        pass

class Player(TilemapActor):
    def __init__(self, tmap, x, y):
        super().__init__(x, y, 16, 32, tmap)

    def tick(self):
        on_floor = self.on_floor()
        on_stair = self.on_stair()
        if controller.left:
            self.xs = -2
        elif controller.right:
            self.xs = 2
        else:
            self.xs = 0
        # Von Treppe nach unten fallen?
        if controller.a==1 and not controller.down:
            # Berührt Boden?
            if on_stair or on_floor:
                self.ys=-7.0
        elif on_stair or on_floor:
                self.ys=0.0
        # Vom Boden Springen?
        if controller.a==1 and controller.down and on_stair:
            self.r.y += 8
        super().tick()

    def draw(self):
        pygame.draw.rect(screen, "white", self.r.move(-camera.x,-camera.y), 1, 7)
        piprint(f"x={self.r.x}  y={self.r.y}",4,4)

db_rects = []

def draw_debug():
    for r in db_rects:
        pygame.draw.rect(screen, "red", r.move(-camera.x,-camera.y), 1)
    db_rects.clear()


controller = Controller()
camera = Camera()
menu = None
debug = False
# main_scene
# tilemap
# sprite_groups
# level
# game_progress
# debug