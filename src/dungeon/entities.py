"""Game objects (Member 2).
Every object on the map has a position (x, y), a character and a colour.
"""


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
