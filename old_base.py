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

import old_base

logging.getLogger().setLevel("INFO")

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

pygame.mixer.init()
sound_select1 = pygame.mixer.Sound("./sounds/sfx_12.wav")
sound_select2 = pygame.mixer.Sound("./sounds/sfx_7.wav")

# Globals
#screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.RESIZABLE, vsync=1)
screen = pygame.display.set_mode((480, 256), pygame.SCALED | pygame.RESIZABLE, vsync=1)
#screen = pygame.display.set_mode((480, 256), pygame.RESIZABLE, vsync=1)

draw_surface = pygame.Surface((480,256))
#draw_surface = pygame.Surface((1920,1080))

## PIPRINT
font = Font("gameengine/mago3.ttf", 16, bold=False, italic=False)
pico_colors = ["black", "darkblue", "darkred", "darkgreen",
               "brown", "darkgrey", "lightgrey", "white",
               "red", "orange", "yellow", "green",
               "blue", "grey", "pink", "lightpink"]
last_color = 7

print_map = {}

# TODO: XL: Konzept für Level-Design (Zeichnung)

# Optimierungen
# TODO: Optimierung: Zusammenführen der Elemente die ticks() erhalten..
# TODO: Optimierung: Event-Handling: Anforderungen definieren (Bullets und Player/Gegner, Trigger, Trigger f. Gegner, Türen)
# TODO: Optimierung: Surface-Handling in Viewport Klasse verschieben
# TODO: Optimierung: Alle Drawcalls mit Delta (ms)
# TODO: Optimierung: Camera: Einfache Berechnung von Screen-Positionen
# TODO: Optimierung: Player-Animation in separate Methode bzw. Animation-Manager-Klasse
# TODO: for _ in ... umsetzen

# Features
# TODO: Animationen
# TODO: Animation/Effect für Tod & Neustart
# TODO: Debug Nachrichten
# TODO: Layer
# TODO: Text-Nachrichten
# TODO: Sounds!
# TODO: Schüsse & Bullets
# TODO: Einfaches Partikel-System
# TODO: (Einfache) Explosionen
# TODO: Einfacher Gegner
# TODO: Controller-Support
# TODO: Animationen für Sprung, Stehen, Schießen
# TODO: (x,y)-Positionen als Typ float
# TODO: MovingBlock und Platform: Weichere Bewegung



def piprint(text, x, y, color="white"):
    if (text, color) in print_map.keys():
        draw_surface.blit(print_map[(text, color)], (x, y))
    else:
        s = font.render(text, False, color)
        print_map[(text, color)] = s
        draw_surface.blit(s, (x, y))

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
        self.follow_obj = None
        self.x = 0
        self.y = 0
        self.w = 480
        self.h = 256


        self.border_width = 100
        self.r = pygame.Rect(0, 0, 480, 256)

    def follow(self, fobj):
        self.follow_obj = fobj

    def tick(self):
        if self.follow_obj:
            if self.follow_obj.r.centerx - self.x < self.border_width:
                self.x = self.follow_obj.r.centerx - self.border_width
            if self.x + self.w - self.follow_obj.r.centerx < self.border_width:
                self.x = self.follow_obj.r.centerx + self.border_width - self.w

            if self.follow_obj.r.centery - self.y < self.border_width:
                self.y = self.follow_obj.r.centery - self.border_width
            if self.y + self.h - self.follow_obj.r.centery < self.border_width:
                self.y = self.follow_obj.r.centery + self.border_width - self.h

            # self.y = self.follow_obj.r.centery-128


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
                s = (s[0], s[1] + s[0] % 16 / 26 + 0.2)  # unterschiedl. Geschw.
            self.stars[i] = s

    def draw(self):
        # piprint(surface, "TestScene2", (380+self.x, 10), "green")
        for i in range(len(self.stars)):
            pygame.draw.circle(draw_surface, "white", self.stars[i], 2, 2)


class Menu(Actor):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.pos = 0
        self.items = []
        pass

    def tick(self):
        # Clicked
        if controller.a == 1:
            sound_select2.play()
            self.clicked(self.items[self.pos])
        # Up
        if controller.down == 1:
            self.pos += 1
            sound_select1.play()
        if self.pos >= len(self.items):
            self.pos = 0
        # Down
        if controller.up == 1:
            self.pos -= 1
            sound_select1.play()
        if self.pos == -1:
            self.pos = len(self.items) - 1

    def draw(self):
        x = 180
        y = 110
        yd = 15
        pygame.draw.rect(draw_surface, "black", pygame.Rect(160,80, 200,100))
        num = 0
        piprint(self.name, x, 80 +5, "white")
        for item in self.items:
            if num == self.pos:
                # Ausgewählter Menüpunkt
                piprint(">", x + 2, y, "white")
                piprint(item[0], x + 10, y, "white")
                piprint(item[1], x + 140, y, "white")
            else:
                # Nicht ausgewählte Menüpunkte
                piprint(item[0], x + 10, y, "red")
                piprint(item[1], x + 140, y, "red")
            y += yd
            num += 1

    def clicked(self, item):
        pass


class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu")
        self.items = [["TOGGLE FULLSCREEN",""], ["RESTART LEVEL",""], ["DEBUG","off"], ["EXIT",""]]

    def clicked(self, item):
        global debug, draw_surface
        if item[0] == "TOGGLE FULLSCREEN":
            pygame.display.toggle_fullscreen()
        if item[0] == "DEBUG":
            if debug:
                debug = False
                self.items[2][1] = "off"
            else:
                debug = True
                self.items[2][1] = "on"
            #pygame.display.toggle_fullscreen()
        if item[0] == "EXIT":
            sys.exit()


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
            self.frame_delay = 5

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

        # Handelt es sich um ein Tileset mit Sprites statt Tiles?
        if not "image" in tileset_json.keys():
            return  # wird nicht eingelesen
        logging.info(f'Lade Tileset "{path}"')
        self.columns = tileset_json["columns"]
        self.rows = math.floor(tileset_json["tilecount"] / self.columns)
        self.tilecount = tileset_json["tilecount"]
        self.tileheight = tileset_json["tileheight"]
        self.tilewidth = tileset_json["tilewidth"]
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
                rect = pygame.Rect(self.tilewidth * col, self.tileheight * row, 16, 16)
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
        self.tilewidth = 0
        self.width = 0
        self.height = 0
        self.backgroundcolor = pygame.Color("black")
        self.mapdata = []
        self.tilesets = []

        self.last_collision_rects = []

    def load(self, filepath: str) -> None:
        #global triggers

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
                        row.append(self.get_tile_from_id(map_temp[x + (self.width * y)]))
                        # self.mapdata.append(map_temp[self.width * y:self.width * y + self.width])
                    self.mapdata.append(row)

                logging.info(f"Tilemap-Layer '{name}' of size {self.width}*{self.height} imported..")

            #
            # Object - Layer
            #
            elif layer["type"] == "objectgroup":
                for o in layer["objects"]:
                    if o["type"] == "moving_platform":
                        triggers.append(TriggerRect(o["name"], o["x"],o["y"], o["width"], o["height"]))

                        logging.info(f"TriggerRect '{o['name']}' hinzugefügt")
                    if o["type"] == "trigger_rect":
                        triggers.append(TriggerRect(o["name"], o["x"],o["y"], o["width"], o["height"]))
                        logging.info(f"TriggerRect '{o['name']}' hinzugefügt")
                    if o["type"] == "trigger_point":
                        triggers.append(TriggerPoint(o["name"], o["x"],o["y"]))
                        logging.info(f"TriggerPoint '{o['name']}' hinzugefügt")


        logging.info(f"Tilemap {filepath} loaded successfully.")
        logging.info(f"Tilemap width={self.width} height={self.height}")

    def get(self, celx, cely):
        return int(math.floor(celx / self.tilewidth)), int(math.floor(cely / self.tileheight))

    def __get_tile_rect(self, celx, cely):
        return pygame.rect.Rect(celx * self.tilewidth, cely * self.tileheight, self.tilewidth, self.tileheight)

    def get_collision_tiles(self, rect, flags=Tile.ALL_FLAGS) -> List[pygame.Rect]:
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

    def draw(self):
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
                    # Grünes Gitter außerhalb der Map zeichnen (Debug)
                    if debug:
                        pygame.draw.rect(draw_surface, pygame.Color("green"),
                                         (int(draw_pos_x), int(draw_pos_y), self.tilewidth, self.tileheight), 1)
                else:
                    if tile := self.mapdata[tile_y][tile_x]:
                        draw_surface.blit(tile.surface, (int(draw_pos_x), int(draw_pos_y)))
                if debug:
                    pygame.draw.line(draw_surface, "green", (draw_pos_x, draw_pos_y), (draw_pos_x, draw_pos_y))




class Animation:
    def __init__(self, imgpath, width, xflip=False, repeat=True):
        if imgpath == "":
            return
        img = pygame.image.load(imgpath)
        img_count = int(math.floor(img.get_width() / width))

        self.images = []
        self.repeat = repeat
        self.actual_index = 0
        self.width = width
        self.timer = 0
        self.height = img.get_height()
        self.end = False
        for i in range(img_count):
            anim_img = pygame.Surface((width, img.get_height()), pygame.SRCALPHA)
            anim_img.blit(img, (0, 0), pygame.Rect(i * width, 0, width, img.get_height()))
            if xflip:
                anim_img = pygame.transform.flip(anim_img, True, False)
            self.images.append(anim_img)

    def draw(self, surface, pos, delta):
        self.timer += delta
        if self.timer > 100:
            self.timer = 0
            self.actual_index += 1
            if self.actual_index == len(self.images):
                self.actual_index = 0
        surface.blit(self.images[self.actual_index], pos)


################################################################################################
# Trigger-Rect
class TriggerRect(Actor):
    def __init__(self, name, x, y, w, h):
        self.name = name
        self.r = pygame.Rect(x, y, w, h)

    def tick(self):
        #print(player.r)
        if player.r.colliderect(self.r):
           print(f'Collision with {self.name}')

    def draw(self):
        if debug:
            pygame.draw.rect(draw_surface, "yellow", self.r.move(-camera.x, -camera.y), 1, 1)
            piprint(self.name, self.r.x-camera.x+2, self.r.y-camera.y+2, "gray")

class TriggerPoint(Actor):
    def __init__(self, name, x, y):
        self.name = name
        self.p = [x,y]
    def draw(self):
        if debug:
            pygame.draw.circle(draw_surface, "yellow", (self.p[0] - camera.x, self.p[1] - camera.y), 1)
            piprint(self.name, self.p[0]-camera.x, self.p[1]-camera.y, "gray")


################################################################################################
# Für Player-Sprites, Gegner, bewegliche Objekte

class Node2D(Actor):
    def __init__(self, x, y, w, h, tilemap):
        super().__init__()
        self.r = pygame.Rect(x, y, w, h)
        self.tilemap = tilemap
        self.xa = 0.0  # Acceleration
        self.ya = 0.4
        self.xs = 0.0  # speed
        self.ys = 0.0

    @property
    def x(self):
        return self.r.x

    @property
    def y(self):
        return self.r.y

    @property
    def w(self):
        return self.r.w

    @property
    def h(self):
        return self.r.h

    @property
    def centerx(self):
        return self.r.centerx

    @property
    def centery(self):
        return self.r.centery


    def move_soft(self, xd, yd, ignore_stairs=False):
        blocked = False
        if xd:
            if not self.move2(xd, 0):
                blocked = True
                self.xs = 0.0
        if yd:
            if not self.move2(0, yd):
                blocked = True
                self.ys = 0.0
        return not blocked

    def move2(self, xd, yd):
        if xd != 0 and yd != 0:
            raise Exception("Move2 kann pro Aufruf nur 1 Achse bewegen")
        tr = self.r.move(xd, yd)  # tr=target_rect
        blocked = False
        if xd != 0 or yd != 0:

            collision_rects = []
            if self.tilemap:
                collision_rects = self.tilemap.get_collision_tiles(tr, Tile.WALL)
            collision_rects += ([w.r for w in moving_blocks if w.r.colliderect(tr)])

            for collider in collision_rects:

                blocked = True
                # Kollision rechts?
                if xd > 0:
                    if tr.right > collider.left:
                        tr.right = collider.left
                # Kollision links?
                if xd < 0:
                    if tr.left < collider.right:
                        tr.left = collider.right
                # Kollision Boden?
                if yd > 0:
                    if tr.bottom > collider.top:
                        tr.bottom = collider.top
                # Kollision mit Decke?
                if yd < 0:
                    if tr.top < collider.bottom:
                        tr.top = collider.bottom
            if yd > 0:
                for stair_tile in self.tilemap.get_collision_tiles(tr, Tile.STAIR) + [x.r for x in moving_platforms]:
                    # wenn mit treppe kollidiert und im letzten Frame vollständig oberhalb des Tiles war
                    if tr.colliderect(stair_tile) and tr.bottom - yd <= stair_tile.top:
                        tr.bottom = stair_tile.top
        self.r = tr
        return not blocked

    def move_hard(self, xd, yd) -> None:
        # hard_move: moves by force, colliding elements were moved or squashed
        rect_dest = self.r.move(xd, yd)
        for pe in physics_elements:
            # Kollidierende Objekte verschieben
            if pe.r.colliderect(rect_dest):
                if not pe.move2(xd, yd):
                    vp.shake()  # Zerquetscht
            # Darauf stehende Objekte verschieben
            if not pe.r.colliderect(rect_dest) and pe.r.move(0, 1).colliderect(rect_dest):
                pe.move2(xd, yd)
        self.r = rect_dest

    def on_floor(self):
        """ detects ground """
        tr = pygame.Rect(self.r.x, self.r.y + self.r.h, self.r.w, 1)
        collision_rects = self.tilemap.get_collision_tiles(tr, Tile.WALL)
        collision_rects += ([w.r for w in moving_platforms if w.r.colliderect(tr)])
        for tile_rect in collision_rects:
            tile_rect.h = 1
            if tr.colliderect(tile_rect):
                return True
        return False

    def on_stair(self):
        """ detects ground """
        tr = pygame.Rect(self.r.x, self.r.y + self.r.h, self.r.w, 1)
        collision_rects = self.tilemap.get_collision_tiles(tr, Tile.STAIR)
        collision_rects += ([w.r for w in moving_platforms if w.r.colliderect(tr)])
        collision_rects += ([w.r for w in moving_blocks if w.r.colliderect(tr)])
        for tile_rect in collision_rects:
            tile_rect.copy().h = 1
            if tr.colliderect(tile_rect):
                return True
        return False

    def tick(self):
        # Schwerkraft simulieren
        if not self.on_floor():
            self.ys += self.ya
        if self.ys > 7.0:
            self.ys = 7.0

        self.move_soft(self.xs, self.ys)

    def draw(self):
        pass

    def collides_with(self, other) -> bool:
        return self.r.colliderect(other.r)

    def stands_on(self, other) -> bool:
        pass

    def draw(self):
        pass

################################################################################################


class MovingBlock(Node2D):
    def __init__(self, x, y, w, h, map, xstart, xend):
        super().__init__(x,y,w,h,map)
        self.start_rect = pygame.Rect(x, y, w, h)
        self.r = self.start_rect.copy()
        self.direction = "RIGHT"
        self.x_start = xstart
        self.x_end = xend

    def tick(self):
        if self.direction == "RIGHT":
            self.move_hard(1, 0)
            if self.x >= self.x_end:
                self.direction = "LEFT"
        else:
            self.move_hard(-1, 0)
            if self.x <= self.x_start:
                self.direction = "RIGHT"

    def draw(self):
        pygame.draw.rect(draw_surface, "red", self.r.move(-camera.x, -camera.y), 1)



class MovingPlatform(Node2D):
    def __init__(self, x, y, w, h, map, xstart, xend):
        super().__init__(x,y,w,h,map)
        self.img = pygame.image.load("img/moving_platform.png")
        self.start_rect = pygame.Rect(x, y, w, h)
        self.r = self.start_rect.copy()
        self.direction = "RIGHT"
        self.x_start = xstart
        self.x_end = xend

    def tick(self):
        if self.direction == "RIGHT":
            self.r.x += 1
            if self.r.x >= self.x_end:
                self.direction = "LEFT"
            for pe in physics_elements:
                if not pe.r.colliderect(self.r) and pe.r.move(0, 1).colliderect(self.r):
                    pe.move2(1, 0)
        else:
            self.r.x -= 1
            if self.r.x <= self.x_start:
                self.direction = "RIGHT"
            for pe in physics_elements:
                if not pe.r.colliderect(self.r) and pe.r.move(0, 1).colliderect(self.r):
                    pe.move2(-1, 0)

    def draw(self):
        draw_surface.blit(self.img, self.r.move(-camera.x, -camera.y).topleft)


class Player(Node2D):
    def __init__(self, tilemap, x, y):
        super().__init__(x, y, 8, 48, tilemap)
        self.anim_right = Animation("./img/player.png", 24, False)
        self.anim_left  = Animation("./img/player.png", 24, True)

    def tick(self, delta):
        on_floor = self.on_floor()  # wird mehrmals benötigt
        on_stair = self.on_stair()  # wird mehrmals benötigt

        if controller.left:
            self.xs = -2
        elif controller.right:
            self.xs = 2
        else:
            self.xs = 0
        # Springen
        if controller.a == 1 and not controller.down and (on_stair or on_floor):
            self.ys = -6.7

        # Von Treppe fallen lassen
        if controller.a == 1 and controller.down and on_stair:
            self.r.y += 1

        if controller.a == 0 and (on_stair or on_floor) and self.ys >= 0:
            self.ys = 0.0
        super().tick()

    def draw(self, delta):
        #pygame.draw.rect(draw_surface, "red", self.r.move(-camera.x, -camera.y), 1, 7)
        if controller.left:
            self.anim_left.draw(draw_surface, (self.r.x - camera.x-6, self.r.y - camera.y), delta)
        else:
            self.anim_right.draw(draw_surface, (self.r.x - camera.x-6, self.r.y - camera.y), delta)

class Viewport(Actor):
    def __init__(self):
        self.rotation_degree = 0.0
        self.scale = 1.0
        self.alpha = 255
        self.bg_color = pygame.Color("black")

        self.timer_shake = 99999
        self.timer_fade_in = 99999
        self.timer_fade_out = 99999

    def shake(self):
        self.timer_shake = 1


    def fade_out(self):
        if self.timer_fade_in >= 500 and self.timer_fade_out >= 500:
            self.timer_fade_out = 0
            self.alpha = 255

    def fade_in(self):
        if self.timer_fade_in >= 500  and self.timer_fade_out >= 500:
            self.timer_fade_in = 0
            self.alpha = 0

    def tick(self, delta):

        if self.timer_shake < 700:
            self.rotation_degree = math.sin(self.timer_shake / 25) * 1.2 * (1 - (self.timer_shake/700))
            self.timer_shake += delta
        else:
            self.rotation_degree = 0

        if self.timer_fade_out < 500:
            self.timer_fade_out += delta
            self.alpha = 255 * (self.timer_fade_out/500)

        if self.timer_fade_in < 500:
            self.timer_fade_in += delta
            self.alpha = 255 * ((500-self.timer_fade_in)/500)

vp=Viewport()

controller = Controller()
camera = Camera()
menu = None
debug = False

message = "sdf"
messagecounter = 0

moving_platforms = []
moving_blocks = []
physics_elements = []
triggers = []

map = Tilemap()
map.load("./img/test_map.json")
player = Player(map, 300, 190)

physics_elements.append(player)


