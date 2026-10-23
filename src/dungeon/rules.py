"""Gameplay rules (Member 2). Rules announce what happened using events."""
from engine import collision
from engine import events as ev


def check_tile(player, level, bus):
    """Called after the player moves: coin, key, trap, exit."""
    for item in level.items:
        if not item.alive or (item.x, item.y) != (player.x, player.y):
            continue
        if item.kind == "coin":
            item.alive = False
            player.score += 10
            bus.emit(ev.COIN_COLLECTED, score=player.score)
        elif item.kind == "key":
            item.alive = False
            player.has_key = True
            bus.emit(ev.KEY_COLLECTED)
        elif item.kind == "trap":
            if player.take_damage():
                bus.emit(ev.TRAP_TRIGGERED, health=player.health)
        elif item.kind == "exit":
            if player.has_key:
                bus.emit(ev.LEVEL_COMPLETE)
            else:
                bus.emit(ev.EXIT_LOCKED)
    check_enemy_contact(player, level, bus)


def check_enemy_contact(player, level, bus):
    for enemy in level.enemies:
        if enemy.alive and (enemy.x, enemy.y) == (player.x, player.y):
            if player.take_damage():
                bus.emit(ev.ENEMY_HIT, health=player.health)
    check_death(player, bus)


def check_death(player, bus):
    if player.health <= 0 and player.alive:
        player.alive = False
        bus.emit(ev.PLAYER_DIED)


def update_enemies(level, player, bus):
    """Move every enemy one step, then see if one touched the player."""
    def is_blocked(x, y):
        return collision.is_wall(level.grid, x, y)

    for enemy in level.enemies:
        new_x, new_y = enemy.next_move(is_blocked, player)
        if not is_blocked(new_x, new_y):  # compute -> validate -> commit
            enemy.x, enemy.y = new_x, new_y
    check_enemy_contact(player, level, bus)
