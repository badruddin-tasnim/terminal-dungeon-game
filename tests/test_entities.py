from dungeon.entities import Player, Enemy


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


def test_patrol_enemy_turns_around_at_wall():
    e = Enemy(1, 1, "patrol_h")
    blocked = lambda x, y: x >= 2
    assert e.next_move(blocked, Player()) == (0, 1)


def test_chase_enemy_moves_toward_player():
    e = Enemy(1, 1, "chase")
    p = Player(5, 1)
    assert e.next_move(lambda x, y: False, p) == (2, 1)
