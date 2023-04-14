#	test_project.py
#	written by Maksims Bogatirjovs

import os, sqlite3, pytest, project
#from os import system, name
#from time import sleep, time


""" MOCK DATABASE 
"""
MOCK_DB_FILE = "mock.db"
TICKET_FILE = "tickets.txt"

""" Remove mock database if exists."""
if os.path.isfile(MOCK_DB_FILE):
		os.remove(MOCK_DB_FILE)

def mock_db():
	CONN = sqlite3.connect(MOCK_DB_FILE)
	CURSOR = CONN.cursor()
	"""creating tables if not exist"""
	CURSOR.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT NOT NULL UNIQUE, user_password TEXT NOT NULL)")
	CURSOR.execute("CREATE TABLE IF NOT EXISTS problems (id INTEGER PRIMARY KEY, problem TEXT NOT NULL)")
	CURSOR.execute("CREATE TABLE IF NOT EXISTS assignments (user_id INTEGER NOT NULL, ticket_id INTEGER NOT NULL, duration INTEGER NOT NULL, passed INTEGER NOT NULL, timestamp TEXT DEFAULT (datetime('now', 'localtime')))")
	""" If no data in 'problems' table, process data import."""
	CURSOR.execute(f"SELECT count(*) FROM problems")
	if not CURSOR.fetchone()[0]:
		with open(TICKET_FILE) as file:
			""" Only first 20 lines need for tests."""
			partial_file = [next(file) for _ in range(20)]
			for line in partial_file:
				CURSOR.execute(f"INSERT INTO problems VALUES (NULL, '{line.strip()}')")
	CONN.commit()
	return (CONN, CURSOR)

""" Replace database connection and cursor 
for testing purposes."""
(project.CONN, project.CURSOR) = mock_db()

def test_sql_auth():
	project.UNAME = "testerbunny"
	assert project.sql_auth("does_user_exist") == False
	project.sql_auth("register", "abcd1234")
	assert project.sql_auth("does_user_exist") == True
	assert project.sql_auth("login", "wrongpassword") == False
	assert project.sql_auth("login", "abcd1234") == True

def test_asker(monkeypatch):
	monkeypatch.setattr("builtins.input", lambda _: "n")
	assert project.asker("start") == "n"
	monkeypatch.setattr("builtins.input", lambda _: "N")
	assert project.asker("start") == "n"
	monkeypatch.setattr("builtins.input", lambda _: "l")
	assert project.asker("start") == "l"
	monkeypatch.setattr("builtins.input", lambda _: "L")
	assert project.asker("start") == "l"
	monkeypatch.setattr("builtins.input", lambda _: "e")
	assert project.asker("start") == "e"
	monkeypatch.setattr("builtins.input", lambda _: "E")
	assert project.asker("start") == "e"
	monkeypatch.setattr("builtins.input", lambda _: "testerbunny")
	assert project.asker("get_user_name") == "testerbunny"
	monkeypatch.setattr("builtins.input", lambda _: "passbun2")
	assert project.asker("get_user_password") == "passbun2"
	monkeypatch.setattr("builtins.input", lambda _: "t")
	assert project.asker("try_again") == "t"
	monkeypatch.setattr("builtins.input", lambda _: "e")
	assert project.asker("try_again") == "e"
	monkeypatch.setattr("builtins.input", lambda _: "")
	assert project.asker("try_again") == ""

	inputs = []
	def mock_input(prompt):
		inputs.append(prompt)
		return "tester1"

	monkeypatch.setattr("builtins.input", mock_input)
	project.asker("get_user_name", True)
	assert inputs == [project.INDENT_TEXT + "New Username      :    "]
	inputs.clear()
	monkeypatch.setattr("builtins.input", mock_input)
	project.asker("get_user_name", False)
	assert inputs == [project.INDENT_TEXT + "Username          :    "]
	inputs.clear()
	monkeypatch.setattr("builtins.input", mock_input)
	project.asker("get_user_password", False)
	assert inputs == [project.INDENT_TEXT + "Password          :    "]

	monkeypatch.setattr("builtins.input", lambda _: "10")
	assert project.asker("get_answer", "2+8") == "10"

	inputs2 = []
	def mock_input2(prompt):
		inputs2.append(prompt)
		return "102"

	monkeypatch.setattr("builtins.input", mock_input2)
	project.asker("get_answer", "2+8")
	assert inputs2 == [project.INDENT_TEXT + "2 + 8 = "]

	inputs2.clear()
	monkeypatch.setattr("builtins.input", mock_input2)
	project.asker("try_again")
	assert inputs2 == [project.INDENT_TEXT + "Enter: ' ⏎ ' to continue or ' E ⏎ ' to exit : "]


def test_doer(monkeypatch):
	monkeypatch.setattr("builtins.input", lambda _: "n")
	assert project.doer("start") == ("new", False)
	monkeypatch.setattr("builtins.input", lambda _: "l")
	assert project.doer("start") == ("login", False)
	monkeypatch.setattr("builtins.input", lambda _: "e")
	assert project.doer("start") == ("", True)

	expected_input_1 = "newuser"
	expected_input_2 = "newpass2"
	user_input = [expected_input_1, expected_input_2]
	monkeypatch.setattr("builtins.input", lambda x: user_input.pop(0))
	result = project.doer("new")
	assert result == ("practice", False)

	expected_input_1 = "testerbunny"
	expected_input_2 = "abcd1234"
	user_input = [expected_input_1, expected_input_2]
	monkeypatch.setattr("builtins.input", lambda x: user_input.pop(0))
	result = project.doer("login")
	assert result == ("practice", False)

	user_input = ["1", "2", "1", "0", "-3", "-8", "2", "8", "9", "10", "e"]
	monkeypatch.setattr("builtins.input", lambda x: user_input.pop(0))
	result = project.doer("practice")
	assert result == ("", True)

	with pytest.raises(SystemExit):
		project.doer("finished")


def test_do_ticket(monkeypatch):
	user_input = ["3", "3", "4", "2", "4", "4", "12", "13", "14", "6", "e"]
	monkeypatch.setattr("builtins.input", lambda x: user_input.pop(0))
	project.do_ticket()
	user_input = ["11", "7", "12", "8", "13", "9", "14", "6", "7", "8", "e"]
	monkeypatch.setattr("builtins.input", lambda x: user_input.pop(0))
	project.do_ticket()
	assert project.do_ticket()
	
	""" Remove mock database."""
	if os.path.isfile(MOCK_DB_FILE):
		os.remove(MOCK_DB_FILE)
