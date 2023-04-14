# Soroban Practice Assistant

#### _About_
_I wrote this Python code as my Final Project for CS50P course. The idea came from teaching my daughter Soroban. I would time her work and count scores every day by hand. Now, I have a script to automate this._

<img src="https://developers.google.com/static/site-assets/logo-youtube.svg" width="27" height="20" style="vertical-align:bottom"> _[Demo video](https://youtu.be/GK2SokOlwS4)_

#### How it works
It's a very basic, text view based program. On the first screen you can:
- make a new user registration: press **`'n'`** followed by **`⏎ Enter`**. It will ask for username and password;
- login as registered user: press **`'l'`** followed by **`⏎ Enter`**. You'll get prompted for username and password;
- for exit: press **`'e'`** followed by **`⏎ Enter`**.

After registration or succesful login you will be taken to solve a set of 10 maths problems, called a ticket. To pass a ticket you have to solve all 10 problems in 2 minutes time. 

Once a ticket has been done, press **`⏎ Enter`** to carry on with other tickets, or exit via **`'e'`**, **`⏎ Enter`**. If you fail a ticket, you will work on it again. There are 100 tickets in total. Once all done, congrats! You've completed the course!

<br>

### Under the hood

#### Modules in `project.py` file
- **`re`** for input validation and math problem formatting
- **`sqlite3`** for database (DB file gets stored on disk)
- from **`os`**: `system` and `name` for clearing screen
- from **`time`**: `sleep` and `time` for *`countdown()`* function and visual effect in *`banner()`* function
	
#### Modules in `test_project.py` file
- **`os`** to remove mock database file
- **`sqlite3`** for mock database
- **`pytest`** to execute unit tests
- **`project`** is the testing object

<sub>_**Quick note:**<br/>the `test_project.py` file is not required for the script to run. It's just for unit testing._</sub>

<br>

#### Main files
- **`project.py`** is the main script to run
- **`tickets.txt`** contains math problems
- **`banner.txt`** ASCII art for presentable look
- **`finished.txt`** ASCII art for when all tickets are done

#### Other files

- **`soroban.db`** is the database file. It's created the first time the program is run. It stores username / password data, imported math problems and user progress data
- **`test_project.py`** for Pytest unit tests

<br>

#### Customization
There are 4 variables in the **`project.py`** file you may want to alter to suit your pace:

```
TICKET_TIME_LIMIT = 120
TICKET_PASS_REQUIREMENT = 10
TICKET_FILE = "tickets.txt"
DB_FILE = "soroban.db"

```

- **`TICKET_TIME_LIMIT`** is time in seconds that user has to finish all 10 math problems, for the ticket to be considered completed
- **`TICKET_PASS_REQUIREMENT`** is how many problems out of 10 need to be correct, for the ticket to be considered completed
- **`TICKET_FILE`**: here you can set another file of your choice for tickets
- **`DB_FILE`**:  you may change the database file

Take note: if you want to import data from your own **`TICKET_FILE`** - only way to do it via **`project.py`** script is either by deleting **`soroban.db`**, or switching to another database by changing value of **`DB_FILE`** variable. Either way you will loose user progress data and login credentials.

When you make your own tickets file, there are certain limitations the script can parse:
- keep the number of problems in multiples of 10
- no blank lines and no spaces
- no other symbols than +-*/
- no more than one operation per line
- the first operand can be a negative integer

Also keep in mind the script won't accept any fractions for an answer (in the user input) - therefore don't include a division (such as `3/2`), that returns a fraction.


<br>

#### Design choices
_I started writing using classes. It was more challanging, but I wanted to write a proper object oriented code. However, one of the requirements on my CS50P final project was to implement at least 3 functions outside of classes for the unit tests. Given the size of this project, I couldn't have both. So, this version became functions only._

Each function is documented inline the code in the ```project.py``` file.

<br>

#### Future developments
After rewriting the code using classes, the following is on my wishlist.

##### Categories
Here is an example of a few:
- addition up to 100, without carry over 5 and 10
- addition up to 100, with carry over 5
- addition up to 100, with carry over 5 and 10
I yet ought to define first draft of categories. 

##### Ticket generation
With a given criteria (per category), script will use an algorythm to generate all tickets instead of importing from a file.

##### Test mode
This will require more than two operations per problem. After completing all tickets from one category user needs to pass a test.

##### Flash anzan mode
A system where users mentally visualize an abacus to carry out arithmetical calculations. No physical abacus is used.

##### GUI with a virtual Soroban
Instead of using physical abacus, users get to use abacus in the APP.

<br>

#### Final notes
_Everything except the intro video was done using an Android smartphone. I used Termux emulator to run Python. It took me 3 weeks to complete all tasks (1-2 hours a day on average). Plus 2 weeks on the final project. And 2 days on video and sound edits. ChatGPT helped where Google, Stack Overflow and Reddit didn't._

_I'm very grateful to [Professor David J. Malan](https://cs.harvard.edu/malan/) for this experience. And I highly recommend [CS50P course](https://www.edx.org/course/cs50s-introduction-to-programming-with-python) to anyone who wants to learn Python._