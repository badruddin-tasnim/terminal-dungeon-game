"""Game objects (Member 2).
Every object on the map has a position (x, y), a character and a colour.
"""
import random
from engine.utils import sign


class Entity:
    kind = "entity"

    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.alive = True


class Player(Entity):
    kind = "player"
    MAX_HEALTH = 3

    def __init__(self, x=0, y=0):
        super().__init__(x, y, "@", "player")
        self.health = self.MAX_HEALTH
        self.score = 0
        self.has_key = False
        self.hit_cooldown = 0  # frames of "invulnerability" after a hit

    def take_damage(self, amount=1):
        """Lose health unless we were hit very recently. True if damage was applied."""
        if self.hit_cooldown > 0:
            return False
        self.health -= amount
        self.hit_cooldown = 10  # about 1 second at 10 FPS
        return True

    def tick(self):
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def heal(self, amount=1):
        self.health = min(self.MAX_HEALTH, self.health + amount)


class Enemy(Entity):
    kind = "enemy"

    def __init__(self, x, y, behavior="patrol_h"):
        super().__init__(x, y, "E", "enemy")
        self.behavior = behavior  # patrol_h, patrol_v, random, chase
        self.dx, self.dy = (0, 1) if behavior == "patrol_v" else (1, 0)

    def next_move(self, is_blocked, player):
        """Return the tile the enemy WANTS to move to. The game validates it."""
        if self.behavior in ("patrol_h", "patrol_v"):
            if is_blocked(self.x + self.dx, self.y + self.dy):
                self.dx, self.dy = -self.dx, -self.dy  # turn around
            return self.x + self.dx, self.y + self.dy

        if self.behavior == "random":
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
            return self.x + dx, self.y + dy

        if self.behavior == "chase":
            dx, dy = player.x - self.x, player.y - self.y
            # try the longer axis first, then the other one
            if abs(dx) >= abs(dy):
                options = [(sign(dx), 0), (0, sign(dy))]
            else:
                options = [(0, sign(dy)), (sign(dx), 0)]
            for step_x, step_y in options:
                if (step_x, step_y) != (0, 0) and not is_blocked(self.x + step_x, self.y + step_y):
                    return self.x + step_x, self.y + step_y
            return self.x, self.y


class Key(Entity):
    kind = "key"

    def __init__(self, x, y):
        super().__init__(x, y, "K", "key")


class Coin(Entity):
    kind = "coin"

    def __init__(self, x, y):
        super().__init__(x, y, "$", "coin")


class Trap(Entity):
    kind = "trap"

    def __init__(self, x, y):
        super().__init__(x, y, "^", "trap")


class Exit(Entity):
    kind = "exit"

    def __init__(self, x, y):
        super().__init__(x, y, "X", "exit")
