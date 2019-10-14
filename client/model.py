import math, random
import pygame.math as gmath

from game_time import frame_time

class Game:
    def __init__(self, width, height):
        self.winner = None
        self.victory_time = 0

        self.width = width
        self.height = height

        self.players = []
        self.bullets = []


class WorldItem:
    def __init__(self):
        self.location = gmath.Vector2(100, 100)
        self.rotation = 0
        self.radius = 50

    def hit(self, other):
        v = self.location - other.location
        return v.length() <= self.radius + other.radius

    def __str__(self):
        return "Location: {}, Rotation: {}".format(self.location, self.rotation)


class Player(WorldItem):
    def __init__(self, index, own):
        super().__init__()
        self.player_index = index
        self.own = own
        self.last_shot = 0

        self.dead = False
        self.death_time = 0

        self.kills = 0

    def die(self, time):
        self.dead = True
        self.death_time = time

    def __str__(self):
        return super().__str__() + ", Index: {}, Dead: {}, Kills: {}".format(self.player_index, self.dead, self.kills)


class Bullet(WorldItem):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.radius = 10
        self.to_destroy = False
        self.direction = gmath.Vector2(0,0)


def new_game(player_amount, width, height):
    game = Game(width, height)

    for i in range(0, player_amount):
        player = Player(i, i == 0)
        set_random_location(player, game)
        game.players.append(player)

    return game

speed = 1
bullet_speed = 3
shoot_cooldown = 200
respawn_cooldown = 1000
victory_condition = 3
rematch_time = 2000

def update_rotation(player, character_input):
    direction = character_input.look_direction - player.location

    player.rotation = (90 + math.atan2(direction.y, direction.x)*180/math.pi) * -1


def update_location(player, character_input):
    player.location += character_input.movement * speed


def shoot(game, player):
    player.last_shot = frame_time()
    
    real_rotation = player.rotation * math.pi / -180

    bullet = Bullet(player)

    dx = -1 * math.sin(real_rotation)
    dy = 1 * math.cos(real_rotation)
    bullet_direction = gmath.Vector2(dx, dy) * -1

    bullet.location = player.location + bullet_direction * 70
    bullet.rotation = player.rotation
    bullet.direction = bullet_direction

    game.bullets.append(bullet)


def update_shooting(game, player, character_input):
    dt = frame_time() - player.last_shot
    if character_input.shooting and dt >= shoot_cooldown: shoot(game, player)


def set_random_location(player, game):
    x = random.random() * (game.width - player.radius * 2) + player.radius
    y = random.random() * (game.height - player.radius * 2) + player.radius

    player.location = gmath.Vector2(x, y)


def revive(player, game):
    player.dead = False

    set_random_location(player,game)


def update_character(game, player, character_input):
    if player.dead and frame_time() - player.death_time >= respawn_cooldown:
        revive(player, game)

    if player.dead: return

    update_location(player, character_input)
    update_rotation(player, character_input)
    update_shooting(game, player, character_input)


def update_characters(game, character_inputs):
    for player in game.players:
        update_character(game, player, character_inputs[player.player_index])


def update_bullets(game):
    for bullet in game.bullets:
        bullet.location = bullet.location + bullet.direction * bullet_speed


def location_in_limits(location, radius, max_limit):
    return location - radius >= 0 and location + radius <= max_limit


def location_to_limits(location, radius, max_limit):
    if location - radius < 0:
        return radius
    elif location + radius > max_limit:
        return max_limit - radius

    return location

def destroy_bullet(game, bullet):
    game.bullets.remove(bullet)


def detect_walls(game):
    for player in game.players:
        player.location.x = location_to_limits(player.location.x, player.radius, game.width)
        player.location.y = location_to_limits(player.location.y, player.radius, game.height)

    for bullet in game.bullets:
        in_limits = location_in_limits(bullet.location.x, bullet.radius, game.width) and location_in_limits(bullet.location.y, bullet.radius, game.height)
        bullet.to_destroy = not in_limits


def hit(bullet, player):
    bullet.to_destroy = True
    bullet.owner.kills += 1 if bullet.owner != player else 0
    player.die(frame_time())


def detect_bullet_hits(game):
    for bullet in game.bullets:
        for player in game.players:
            if player.dead or not bullet.hit(player): continue

            hit(bullet, player)


def collision_detection(game):
    detect_walls(game)
    detect_bullet_hits(game)


def delete_bullets(game):
    to_destroy = []

    for bullet in game.bullets:
        if bullet.to_destroy: to_destroy.append(bullet)

    for d in to_destroy:
        destroy_bullet(game, d)


def check_victory(game):
    for player in game.players:
        if player.kills < victory_condition: continue
        game.winner = player
        game.victory_time = frame_time()
        return


def reset_game(game):
    game.winner = None

    for player in game.players:
        player.dead = False
        player.kills = 0
        player.last_shot = 0
        set_random_location(player, game)

    game.bullets = []


def check_is_playing(game):
    if game.winner == None: return True

    elapsed = frame_time() - game.victory_time

    if elapsed < rematch_time: return False
    
    reset_game(game)
    return True


def update_world(game, character_inputs):
    if not check_is_playing(game): return

    update_bullets(game)
    update_characters(game, character_inputs)

    collision_detection(game)
    delete_bullets(game)

    check_victory(game)