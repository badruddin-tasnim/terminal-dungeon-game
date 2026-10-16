COORDINATES   Everywhere in the game we use (x, y): x = column, y = row.
              Only renderer.py converts to curses (row, column).

MAP FILES     levels/levelN.txt, plain text. Characters:
              #  wall            @  player start
              K  key             X  exit
              T  trap            $  coin
              E  enemy patrolling left-right
              V  enemy patrolling up-down
              R  enemy moving randomly
              C  enemy that chases the player
              (space) floor

LEVEL OBJECT  level.number, level.grid (list of rows, each row a list of
              characters, only '#' or ' '), level.width, level.height,
              level.player_start = (x, y), level.enemies (list of Enemy),
              level.items (list of Key, Coin, Trap, Exit)

ENTITY        every entity has: x, y, char, color (a name such as 'enemy'),
              alive (True/False) and kind ('player','enemy','key','coin',
              'trap','exit')

PLAYER        player.health, player.max health = Player.MAX_HEALTH,
              player.score, player.has_key, player.take_damage(),
              player.tick(), player.heal()

RULES API     rules.check_tile(player, level, bus)      after player moves
(Member 2)    rules.update_enemies(level, player, bus)  every few frames

EVENTS        PLAYER_MOVED, COIN_COLLECTED, KEY_COLLECTED, TRAP_TRIGGERED,
(Member 1)    ENEMY_HIT, EXIT_LOCKED, LEVEL_COMPLETE, PLAYER_DIED
              bus.emit(NAME, **data)   bus.subscribe(NAME, function)

INPUT ACTIONS UP, DOWN, LEFT, RIGHT, PAUSE, QUIT, ENTER, 1, 2, 3

SAVE FILE     saves/savegame.json = {level_index, health, score}