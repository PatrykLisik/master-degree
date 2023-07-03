from src.web.api.mobile_app_usecase import pair_iterator


def test_pair_iterator():
    numbers = [1, 2, 3, 4, 5]
    pairs = pair_iterator(numbers)
    assert pairs
