import pygame, os
import pygame.math as gmath

black = 0, 0, 0
white = 255, 255, 255

screen = None
resources = {}

def init_output(width, height):
    global screen
    
    resource_path = os.path.join(os.path.dirname(__file__),"resources")

    player_path = os.path.join(resource_path, "player.png")
    bullet_path = os.path.join(resource_path, "bullet.png")
    other_path = os.path.join(resource_path, "other.png")
    font_path = os.path.join(resource_path, "font.ttf")

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Online multiplayer shooter")

    resources["player"] = pygame.image.load(player_path)
    resources["other"] = pygame.image.load(other_path)
    resources["bullet"] = pygame.image.load(bullet_path)

    resources["font"] = pygame.font.Font(font_path, 16)


def draw_item(item, image_name):
    image = resources[image_name]

    rotated_image = pygame.transform.rotate(image, item.rotation)
    rotated_rect = rotated_image.get_rect()
    height, width = rotated_rect.height, rotated_rect.width

    screen.blit(rotated_image, gmath.Vector2(item.x, item.y) - gmath.Vector2(width / 2, height / 2))


def draw_text(text, x, y, centered = False):
    font = resources["font"]

    textrender = font.render(text, True, white)

    rect = textrender.get_rect()
    if centered:
        rect.centerx = x
        rect.centery = y
    else:
        rect.x = x
        rect.y = y

    screen.blit(textrender, rect)


def draw_scores(info, game):
    players = game.players.copy()
    players.sort(key = lambda x: x.kills, reverse=True)

    texts = ["Scores:"]
    texts.extend(map(lambda x: "Player {}: {}".format(x.player_index, x.kills), players))

    x = info.width - 90
    y = 0
    y_increase = 20
    for text in texts:
        draw_text(text, x, y)

        y += y_increase


def normal_mode(info, game):
    for player in game.players:
        if player.dead: continue
        draw_item(player, "player" if player.own else "other")

    for bullet in game.bullets:
        draw_item(bullet, "bullet")

    draw_scores(info, game)


def victory_mode(info, game):
    x = info.width / 2
    y = info.height / 2
    draw_text("Winner: Player {}".format(game.winner), x, y, True)


def update_screen(info, game):
    screen.fill(black)

    if game == None:
        pygame.display.flip()
        return

    if game.winner == None:
        normal_mode(info, game)
    else:
        victory_mode(info, game)

    pygame.display.flip()