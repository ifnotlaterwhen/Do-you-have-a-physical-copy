#import pytest # not needed, using monkeypatch & capsys in a param
import main

# this initializes the cinefiles database and seeds it with mock data.
# not needed for these tests, which don't deal with the DB
# @pytest.fixture
# def clean_db():
#     cleanDB = FilmDB("cinefiles")
#     cleanDB.init_db()
#     cleanDB.seed_db_mock()

def test_main_menu_input_is_int(monkeypatch, capsys):
    
    user_inputs = iter(["bob","1"])

    monkeypatch.setattr(
        "builtins.input", lambda prompt: next(user_inputs)
    )

    result = main.menu()
    output = capsys.readouterr().out

    assert result == 1
    assert "Please enter a valid number" in output

def test_main_menu_number_too_low(monkeypatch, capsys):
    
    user_inputs = iter(["0","1"])

    monkeypatch.setattr(
        "builtins.input", lambda prompt: next(user_inputs)
    )

    result = main.menu()
    output = capsys.readouterr().out

    assert result == 1
    assert "Number too low. Pease enter a number on the menu (1-7)" in output

def test_main_menu_number_too_high(monkeypatch, capsys):
    
    user_inputs = iter(["8","1"])

    monkeypatch.setattr(
        "builtins.input", lambda prompt: next(user_inputs)
    )

    result = main.menu()
    output = capsys.readouterr().out

    assert result == 1
    assert "Number too high. Pease enter a number on the menu (1-7)" in output



def test_physical_menu_invalid_input_is_int(monkeypatch, capsys):
    # need to have test_ in function name, not just filename
    # monkeypatch = pytest tool, replace element
    # capsys = pytest tool, captures printed text (check error message from exception)
    
    # Pretend the user enters "hello", then 1. "hello" should give an error as not int, 1 should be fine
    user_inputs = iter(["hello", "1"])  
    monkeypatch.setattr(
        "builtins.input", lambda prompt: next(user_inputs)
    )
    # iter() > go through your fake inputs one at a time
    # builtins.input > you want pytest to supply inputs automatically
    # monkeypatch.setattr() > replace input() with replacement during test
    # lambda prompt > create small function that accepts are called prompt
    # next(user_inputs) > next prepared input from varialbe we set

    # Run the actual menu
    result = main.physical_menu()   # should return 1 (the second in user_inputs, which is valid)

    # Check the result and error message
    output = capsys.readouterr().out
    # capsys.readouterr() retrieves the print output from function being testing
    # .out selects normal printed output
    # save to output variable
    
    assert result == 1
    # check that our test does return 1 in the end as expected (in line 29)
    assert "Please enter a valid number" in output
    # check that the printed message, which only happens if there's a non-int issue, is this one

def test_physical_menu_number_too_low(monkeypatch, capsys):
    user_inputs = iter(["0", "1"])
    monkeypatch.setattr(
        "builtins.input", lambda prompt: next(user_inputs)
    )

    result = main.physical_menu()
    output = capsys.readouterr().out

    assert result == 1
    assert "Number too low. Pease enter a number on the menu (1-5)" in output

def test_physical_menu_number_too_high(monkeypatch, capsys):
    user_inputs = iter(["6", "1"])
    monkeypatch.setattr(
        "builtins.input", lambda prompt: next(user_inputs)
    )

    result = main.physical_menu()
    output = capsys.readouterr().out

    assert result == 1
    assert "Number too high. Pease enter a number on the menu (1-5)" in output

# run tests from parent folder with:
# python3 -m pytest tests/menu_input_test.py -v