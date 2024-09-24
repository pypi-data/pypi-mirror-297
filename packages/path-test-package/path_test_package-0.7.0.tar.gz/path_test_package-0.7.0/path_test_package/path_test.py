"""See where __file__ ends up resolving to after being imported."""


from pathlib import Path

path_resolves = Path(__file__)  #TODO: where will this resolve to when imported?



def get_test_path() -> str:
    return path_resolves

def do_path_tests() -> None:
    print(f"Path(__file__): {Path(__file__)}")
    print(f"Path(__name__): {Path(__name__)}")