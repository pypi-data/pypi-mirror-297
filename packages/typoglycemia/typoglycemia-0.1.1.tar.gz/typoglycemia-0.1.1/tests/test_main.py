import random
from src.typoglycemia.main import shuffle, make_typoglycemia
import subprocess
import sys
import pytest
@pytest.fixture(autouse=True)
def set_seed():
    random.seed(100)
    
@pytest.mark.parametrize("input_word, expected_output", [
    ("hello", "hello"),
    ("hi", "hi"),
    ("__init__.py", "__init__.py")
])
def test_shuffle(input_word, expected_output):
    assert shuffle(input_word) == expected_output

@pytest.mark.parametrize("input_sentence, expected_output", [
    ("hello world", "hello world"),
    ("hi world", "hi world"),
    ("__init__.py", "__init__.py")
])
def test_make_typoglycemia(input_sentence, expected_output):
    assert make_typoglycemia(input_sentence) == expected_output

# def test_cli():
#     args = [sys.executable, "-m", "typoglycemia", "-t", "test"]
#     process = subprocess.run(args, capture_output=True, text=True, check=True)
        
#     assert process.stdout