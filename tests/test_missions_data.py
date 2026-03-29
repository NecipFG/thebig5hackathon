from person1.missions_data import MISSIONS


def test_three_missions_defined():
    assert len(MISSIONS) == 3


def test_mission_ids_are_1_2_3():
    ids = [m["id"] for m in MISSIONS]
    assert ids == [1, 2, 3]


def test_required_keys_present():
    required = {
        "id", "name", "difficulty", "objective",
        "start_lat", "start_lon", "goal_lat", "goal_lon",
        "dem_file",
    }
    for mission in MISSIONS:
        missing = required - mission.keys()
        assert not missing, f"Mission {mission['id']} missing keys: {missing}"


def test_difficulties_are_easy_medium_hard():
    difficulties = [m["difficulty"] for m in MISSIONS]
    assert difficulties == ["easy", "medium", "hard"]


def test_all_coords_in_south_pole_region():
    for m in MISSIONS:
        for lat_key in ("start_lat", "goal_lat"):
            assert -90.0 <= m[lat_key] <= -80.0, (
                f"Mission {m['id']} {lat_key}={m[lat_key]} outside south pole region"
            )


def test_all_longitudes_in_valid_range():
    for m in MISSIONS:
        for lon_key in ("start_lon", "goal_lon"):
            assert 0.0 <= m[lon_key] <= 360.0, (
                f"Mission {m['id']} {lon_key}={m[lon_key]} outside valid range [0, 360]"
            )


def test_start_and_goal_are_different():
    for m in MISSIONS:
        assert (m["start_lat"], m["start_lon"]) != (m["goal_lat"], m["goal_lon"]), (
            f"Mission {m['id']} start equals goal"
        )
