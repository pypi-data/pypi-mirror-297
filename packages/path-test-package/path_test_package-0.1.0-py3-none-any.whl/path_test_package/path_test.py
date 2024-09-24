"""See where __file__ ends up resolving to after being imported."""


from pathlib import Path

path_resolves = Path(__file__)  #TODO: where will this resolve to when imported?



def get_test_path() -> str:
    return path_resolves
