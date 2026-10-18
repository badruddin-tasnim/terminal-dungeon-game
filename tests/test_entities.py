from dungeon.entities import Player


def test_player_cooldown_prevents_double_damage():
    p = Player()
    assert p.take_damage() is True
    assert p.take_damage() is False
    assert p.health == 2


def test_cooldown_counts_down():
    p = Player()
    p.take_damage()
    for _ in range(10):
        p.tick()
    assert p.take_damage() is True


def test_heal_is_capped():
    p = Player()
    p.heal(5)
    assert p.health == Player.MAX_HEALTH
