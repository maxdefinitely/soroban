#	project.py
#	Soroban Practice Assistant
#	written by Maksims Bogatirjovs

""" IMPORTING LIBRARIES: """
import re, sqlite3, random
from os import system, name
from time import sleep, time

""" CONSTANT VARIABLES: """
BANNER_FILE = ("banner.txt", "finished.txt")
INDENT_TEXT = "    "
TICKET_TIME_LIMIT = 120
TICKET_PASS_REQUIREMENT = 10
TICKET_FILE = "tickets.txt"
DB_FILE = "soroban.db"

""" DATABASE SETUP:
"""
CONN = sqlite3.connect(DB_FILE)
CURSOR = CONN.cursor()
"""creating tables if not exist"""
CURSOR.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT NOT NULL UNIQUE, user_password TEXT NOT NULL)")
CURSOR.execute("CREATE TABLE IF NOT EXISTS problems (id INTEGER PRIMARY KEY, problem TEXT NOT NULL)")
CURSOR.execute("CREATE TABLE IF NOT EXISTS assignments (user_id INTEGER NOT NULL, ticket_id INTEGER NOT NULL, duration INTEGER NOT NULL, passed INTEGER NOT NULL, timestamp TEXT DEFAULT (datetime('now', 'localtime')))")
""" If no data in 'problems' table, process data import."""
CURSOR.execute(f"SELECT count(*) FROM problems")
if not CURSOR.fetchone()[0]:
	with open(TICKET_FILE) as file:
		for line in file:
			CURSOR.execute(f"INSERT INTO problems VALUES (NULL, '{line.strip()}')")
CONN.commit()


"""
FUNCTION DEFINITIONS:
"""

#
#
def clear():
	"""
	Call clear screen command, depending on os."""
	if name == "nt":	_ = system("cls")
	else:	_ = system("clear")

#
#
def countdown(i, arg=0):
	"""
	Countdown starting from i.

	: param i     :  number to start counting down from
	: type i        :  int
	: param arg :  message trigger
	: type arg    :  int, default: 0
	: return        :  print a message and count down from 'i'' in same line in 1 second intervals
	: rtype         :  str
	"""
	txt = "Get ready! Starting in: " if arg else "Restarting in: "
	for _ in range(i):	print (INDENT_TEXT + txt + str(i-int(_)), end="\r", flush=True);	sleep(1)

#
#
def banner(x=0, y=0):
	"""
	Clear screen and print a banner.
	y=0 prints default banner: 'Welcome to practice Soroban'
	y=1 prints banner: 'Congrats. You have finished Sofoban BA100'

	: param x                      :  pause lenght and printing speed (default: 0 fastest/instant)
	: type x                         :  int
	: param y                      :  banner trigger
	: type y                         :  int
	: param BANNER_FILE  :  file name of the banner
	: type BANNER_FILE     :  GLOBAL tuple
	: return                          :  clear screen and print a banner one line at a time
	                                         or instantly (depending on 'x' speed)
	"""
	""" Clear screen and pause x seconds."""
	clear();	sleep(x)
	""" Import banner file. """
	with open(BANNER_FILE[y]) as file:
		for line in file:
			""" Print line by line with or without a pause."""
			print (line.rstrip());	sleep(x/10*1.5)

#
#
def sql_auth(do, upass=""):
	""" Authentication operations:
		* check if username exists (Return: True/False)
		* register a new user
		* check if username matches password (Return: True/False)

	: param do         :  case trigger
	: type do            :  str
	: param upass     :  password
	: type upass        :  str (Default: "")
	: param UNAME  :  username
	: type UNAME     :  GLOBAL str
	: return                :  True / False / Insert into database
	"""

	""" Start match on do."""
	match do:

		case "does_user_exist":
			""" Return True if user exists, False if doesn't."""
			CURSOR.execute(f"SELECT count(*) FROM users WHERE user_name='{UNAME}'")
			return(CURSOR.fetchone()[0])

		case "register":
			""" Save new username and password."""
			CURSOR.execute(f"INSERT INTO users VALUES (NULL, '{UNAME}', '{upass}')")
			CONN.commit()

		case "login":
			""" Return True if user name and password match, False if don't.."""
			CURSOR.execute(f"SELECT count(*) FROM users WHERE user_name='{UNAME}' AND user_password='{upass}'")
			return(CURSOR.fetchone()[0])

	""" /End of match."""

#
#
def do_ticket():
	"""
	* If all tickets already done: return True
	* Prepare a ticket (10 problems).
	* Save user's progress.
	"""

	""" Select one ticket, meeting ALL of these conditions:
		  * ONLY for the current user
		  * either 'duration', 'passed' or both are outside set limits, ONLY IF:
		  	  * no record of that ticket_id exists that has both 'duration' and 'passed' within limits
		  """
	CURSOR.execute(f"SELECT t1.ticket_id FROM assignments t1 WHERE t1.user_id = (SELECT id FROM users WHERE user_name = '{UNAME}') AND (t1.duration > {TICKET_TIME_LIMIT} OR t1.passed < {TICKET_PASS_REQUIREMENT}) AND NOT EXISTS (SELECT * from assignments t2 WHERE t2.ticket_id = t1.ticket_id AND t2.duration <= {TICKET_TIME_LIMIT} AND t2.passed >= {TICKET_PASS_REQUIREMENT} AND t2.user_id = (SELECT id FROM users WHERE user_name = '{UNAME}'));")
	""" Try to fetch unfinished ticket."""
	try:
		""" Get unfinished ticket ID"""
		ticket_todo = CURSOR.fetchone()[0]
	except TypeError:
		""" No unfinished tickets found.
		Select one ticket with highest ID for the current user."""
		CURSOR.execute(f"SELECT max(ticket_id) FROM assignments WHERE user_id = (SELECT id FROM users WHERE user_name = '{UNAME}')")
		""" If such ticket exists... """
		if ticket_todo := CURSOR.fetchone()[0]:
			""" ...assign the next ticket."""
			ticket_todo += 1
		else:
			""" Assign the first ticket, since none done so far."""
			ticket_todo = 1
	""" Select total problems count."""
	CURSOR.execute("SELECT COUNT(id) FROM problems")
	""" If all tickets done: return True."""
	if (CURSOR.fetchone()[0]/10 < ticket_todo):
		return(True)
	""" Initialize starting time."""
	start_time = time();
	""" Initialize answer counter."""
	passed=0
	""" Print ticket number."""
	print(INDENT_TEXT + f"TICKET NUMBER: {ticket_todo}")
	""" Initialize 10 problems one at a time:"""
	# used to be this
	# for i in range(10):
	# now it's random:⬇↓
	for i in random.sample(range(10), 10):
		CURSOR.execute(f"SELECT problem FROM problems WHERE id = {ticket_todo*10+i-9}")
		problem = CURSOR.fetchall()[0][0]
		""" Take user input for each problem..."""
		if int(asker("get_answer", problem)) == eval(problem):
			"""...and count correct answers."""
			passed+=1
	""" Calculate duration it took to finish all 10 problems."""
	duration = int(time() - start_time)
	""" Print results."""
	print("\n-----------------------------------------------------")
	print(INDENT_TEXT + f"DONE: {passed} / 10, in {duration} seconds ", end="")
	if duration <= TICKET_TIME_LIMIT and passed > 9:
		print("😊")
	else:
		print("😔")
	""" Save time it took and number of correct answers."""
	CURSOR.execute(f"INSERT INTO assignments (user_id, ticket_id, duration, passed) VALUES ((SELECT id FROM users WHERE user_name = '{UNAME}'), {ticket_todo}, {duration}, {passed})")
	CONN.commit()

#
#
def asker(do, arg=True):
	"""
	Input retrieval and validation.

	: param do                     :  case trigger
	: type do                        :  str
	: param arg                    :  in 'get_user_name' case: message trigger
	:                                     :  in 'get_answer' case: carries value of a 'problem' to the user input
	: type arg                       :  bool / str (Default: True)
	: param INDENT_TEXT  :  indentation for output messages
	: type INDENT_TEXT     :  GLOBAL str
	: if EOFError                  :  print exit message and stop the script
	: return                           :  varied, depending on a case
	: rtype                            :  str
	"""

	""" Initialize return variable r """
	r = ""
	""" Try to see if Ctrl+D is pressed."""
	try:
		""" Start match on do: """
		match do:

			case "start":
				""" Only valid inputs accepted: N, L or E (case-insensitively)"""
				print(INDENT_TEXT + "    ➨ New user    :    N ⏎\n" + INDENT_TEXT + "    ➨ Login       :    L ⏎\n" + INDENT_TEXT + "    ➨ Exit        :    E ⏎\n")
				while r not in ["n", "l", "e"]:
					r =input(INDENT_TEXT + "Enter your choice :    ").strip().lower()

			case "get_user_name":
				""" Username can contain letters and numbers. First has to be a letter."""
				while not re.search(r"^[a-z]+\w*$", r):
					r = input(INDENT_TEXT + ("New Username      :    " if arg else "Username          :    ")).strip().lower()

			case "get_user_password":
				""" Password has four or more characters, at least one digit."""
				while not re.search(r"^(?=.*\d).{4,}$", r):
					r = input(INDENT_TEXT + "Password          :    ")

			case "get_answer":
				""" Math problems need space before and after operator."""
				arg = re.sub(r"([-+*/])", r" \1 ", arg).lstrip()
				""" Answer can only be a digit."""
				while not re.search(r"^-?\d+$", r):
					r = input(INDENT_TEXT + arg + " = ")

			case "try_again":
				""" E or e for exit. Any other input for continue practicing."""
				r = input(INDENT_TEXT + "Enter: ' ⏎ ' to continue or ' E ⏎ ' to exit : ").strip().lower()

		""" All cases done. Return user input."""
		return (r)
		""" /End of match."""
	except EOFError:
		""" Ctrl+D pressed: print exit message... """
		print("\n" + INDENT_TEXT + "See you next time! Bye, bye!\n")
		""" ...and stop the script."""
		exit()

#
#
def doer(do):
	""" The main operations and routing to screens.
		  Works with function main() in a loop.
		  Returns two values to function main()

	: param do            :  match trigger: go to screen...
	: type do               :  str
	: variable UNAME  :  gets declared global and initialized
	: type UNAME       :  str
	: return                  :  value1, value2
	: value1                  :  where to go
	: type value1          :  str
	: value2                  :  whether to exit (True), or stay (False)
	: type value2          :  bool
	"""

	""" Declare global UNAME variable for username."""
	global UNAME

	""" Start match on do: """
	match do:

		case "start":
			""" CASE: Start screen."""
			""" Clear screen. Print banner slowly."""
			banner(0.5)
			""" Retrieve validated user input."""
			q = asker("start")
			if q == "n":
				""" Go to registration screen."""
				return ("new", False)
			elif q=="l":
				""" Go to login screen."""
				return ("login", False)
			""" Go to exit screen."""
			return ("", True)

		case "new":
			""" CASE: registration screen."""
			""" Initialize loop trigger q."""
			q = True
			while q:
				""" Ask for username."""
				UNAME = asker("get_user_name")
				""" Check whether username exists."""
				q = sql_auth("does_user_exist")
				""" If exists print to try another username (goes back in a loop)."""
				print("" if not q else f"{INDENT_TEXT}{UNAME} already exists, try another\n", end = "")
			""" Ask password. Save username and password."""
			sql_auth("register", asker("get_user_password"))
			print(INDENT_TEXT + "Registration complete!")
			""" Go to practice screen."""
			return ("practice", False)

		case "login":
			""" CASE: login screen."""
			""" Ask for username."""
			UNAME = asker("get_user_name", False)
			""" If username doesn't exist:"""
			if not sql_auth("does_user_exist"):
				""" Print it doesn't exist."""
				print(INDENT_TEXT + f"User '{UNAME}' doesn't exist")
				""" Count down from 5, so user can read the message."""
				countdown(5)
				""" Go to start screen."""
				return ("start", False)
			""" Ask for password and check if it matches username."""
			if sql_auth("login", asker("get_user_password")):
				""" They match: go to practice screen."""
				return ("practice", False)
			""" Print username doesn't match password."""
			print(INDENT_TEXT + "Username doesn't match password!")
			""" Count down from 5, so user can read the message."""
			countdown(5)
			""" Go to start screen."""
			return ("start", False)

		case "practice":
			""" CASE: practice screen."""
			""" Count down from 5, before clearing the screen."""
			countdown(5, 1)
			""" Clear screen. Print banner instantly."""
			banner()
			""" Go to do one ticket."""
			if do_ticket():
				""" If return value is True: it means all tickets are done
				Go to finished screen."""
				return("finished", False)
			""" Ask continue or exit?"""
			if asker("try_again") == "e":
				""" User chose exit: return True to main() for exit."""
				return ("", True)
			""" User chose to continue: go to practice screen."""
			return ("practice", False)

		case "finished":
			""" CASE: finished screen."""
			""" Clear screen. Print (congrats) banner instantly."""
			banner(0, 1)
			""" Stop the script."""
			exit()
	""" /End of match."""

#
#
def main():
	""" The main logic is achieved in a loop with
		  the function doer(do):
		      * main() functions as a router
		      * doer(do) executes the logic

	: variable do    :  to be passed to doer(do)
	: type do         :  str
	: variable x_it  :  whether to exit script (True), or stay (False)
	: type x_it       :  bool
	: return           :  value1, value2
	: value1           :  where to go
	: type value1   :  str
	: value2           :  whether to exit (True), or stay (False)
	: type value2   :  bool
	"""

	""" Set to go to start screen first."""
	do = "start"
	""" Initialize x_it to False (for the loop to continue)."""
	x_it = False
	""" Start looping."""
	while x_it == False:
		""" Retrieves new instruction and whether to stay or exit."""
		do, x_it = doer(do)
	""" Since stopped from looping, close the database."""
	CONN.close()
	""" Print goodbye message."""
	print(INDENT_TEXT + "See you next time! Bye, bye!\n")

""" Nothing left to do. Script stops here."""


""" Call main()
if being run as the main program.
"""
if __name__ == "__main__":
	main()
