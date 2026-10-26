from dungeon import save_manager


def test_save_and_load(tmp_path):
    path = str(tmp_path / "save.json")
    save_manager.save_game(1, 2, 30, path)
    assert save_manager.load_game(path) == {
        "level_index": 1,
        "health": 2,
        "score": 30,
    }


def test_missing_save_returns_none(tmp_path):
    assert save_manager.load_game(str(tmp_path / "nope.json")) is None


def test_corrupted_save_returns_none(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json")
    assert save_manager.load_game(str(path)) is None


def test_save_with_non_integer_value_returns_none(tmp_path):
    path = tmp_path / "bad_types.json"
    path.write_text('{"level_index": "one", "health": 3, "score": 10}')
    assert save_manager.load_game(str(path)) is None
