from engine import events as ev
from engine.events import EventManager
from dungeon.entities import Player, Key, Coin, Trap, Exit
from dungeon.level import Level
from dungeon import rules


def make(item):
    grid = [list("#####"), list("#   #"), list("#####")]
    level = Level(1, grid, (1, 1), [], [item])
    player = Player(item.x, item.y)
    bus, seen = EventManager(), []
    for name in (
        ev.COIN_COLLECTED,
        ev.KEY_COLLECTED,
        ev.TRAP_TRIGGERED,
        ev.EXIT_LOCKED,
        ev.LEVEL_COMPLETE,
        ev.PLAYER_DIED,
    ):
        bus.subscribe(name, lambda n=name, **kw: seen.append(n))
    return level, player, bus, seen


def test_coin_adds_score():
    level, player, bus, seen = make(Coin(2, 1))
    rules.check_tile(player, level, bus)
    assert player.score == 10 and seen == [ev.COIN_COLLECTED]


def test_key_is_collected():
    level, player, bus, seen = make(Key(2, 1))
    rules.check_tile(player, level, bus)
    assert player.has_key


def test_locked_exit_does_not_finish_level():
    level, player, bus, seen = make(Exit(2, 1))
    rules.check_tile(player, level, bus)
    assert seen == [ev.EXIT_LOCKED]


def test_exit_with_key_completes_level():
    level, player, bus, seen = make(Exit(2, 1))
    player.has_key = True
    rules.check_tile(player, level, bus)
    assert seen == [ev.LEVEL_COMPLETE]


def test_trap_hurts_and_can_kill():
    level, player, bus, seen = make(Trap(2, 1))
    player.health = 1
    rules.check_tile(player, level, bus)
    assert ev.PLAYER_DIED in seen
