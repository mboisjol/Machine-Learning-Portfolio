import datetime

from clint.textui import prompt, puts, colored, indent, validators

from config.qt_config import QTConfig
from database_layer import business_db
from models.Business import Business
from scrapper_helper import scrapper_helper
from scrappers import yp_scrapper


def help(args=None):
    with indent(4, quote=' >'):
        description = {'help': 'Will Show the possible commands and what they do',
                       'init': 'Initialize the configuration with paths, keywords and locations',
                       'run': 'Cleans the Database and Scraps YellowPages for new data',
                       'to-csv': 'Creates a CSV from the database',
                       'clear-db': 'Cleans the Database',
                       'exit': 'Exits program'}
        for command, description in description.items():
            puts(f"{command}    {description}")


def init(args=None):
	# Remove current config
	QTConfig.clear_config()

	path = prompt.query('Database path (defaults at same directory as exe): ', default='./',
						validators=[validators.PathValidator()]) + "db.json"
	auto_csv = prompt.yn("Would you like a CSV to be generated after each run?")

	items = prompt.query('Enter items separated by comma: ').split(",")

	for i in range(len(items)):
		items[i] = items[i].strip()

	if '' in items:
		   items = [item for item in items if item != '']

	cities = prompt.query('Enter cities with format <name> <province> separated by comma.\nIf you want all major '
						  'canadian cities, type \"all\": ')
	if cities.strip() == "all":
		cities = scrapper_helper.append_all_cities()
	else:
		cities = cities.split(",")

		for i in range(len(cities)):
			cities[i] = cities[i].strip()

		if '' in cities:
		   cities = [city for city in cities if city != '']

	obj = {"db.path": path,
		   "items": items,
		   "auto-csv": auto_csv,
		   "locations": cities}

	QTConfig.set_config(obj)

	puts(colored.red("Restart program for the changes to take into effect"))
	prompt.query("This program will restart", default="Ok")

	global _exit
	_exit = True


def run(args=None):
	# ======= COMMENTED FOR DESJARDINS =========
	# run_commands = {
	#     "yp": yp_scrapper.start,
	#     "elec": elec_scrapper.start
	# }
	#
	# if len(args) > 1:
	#     puts(colored.red(f"Command <run {args}> does not exit. Please try again"))
	#     return

	try:
		scrapper = yp_scrapper.start
	except KeyError:
		puts(colored.red(f"Command <run {args}> does not exit. Please try again"))
		return
	except IndexError:
		puts(colored.red(f"You need to specify an argument. See \"help\" to get the list. Please try again"))
		return

	puts(colored.red("Do you want to clear the Database? Otherwise, the results will be appended"))
	resp = prompt.yn("\nDo you want to clear the Database?")
	if resp:
		clear_db(_from="run")

	try:
		puts(colored.green("Starting Scraping..."))
		found = scrapper()
		puts(colored.green(f"Finished Scraping from YellowPages. Found {found} results in total"))

		if QTConfig.get_config().auto_csv:
			date = datetime.date.today().strftime("%d-%m-%y")
			print(f"date:{date}")
			#print(f"args:{args[0]}")
			to_csv(name=f"data_29dec.csv")
			#to_csv(name=f"{args[0]}_{date}.csv")

	except RuntimeError as err:
		puts(colored.red(f"{err}"))


def to_csv(args=None, name=None):
    if name is None:
        name = prompt.query('CSV name (defaults at db.csv): ', default='db.csv',
                            validators=[])
    reference_object = Business(None)

    puts(colored.green("Creating CSV file..."))
    try:
        business_db.to_csv(reference_object, name)
        puts(colored.green(f"CSV file named {name} is created"))
    except Exception as ex:
        puts(colored.red(f"Failed to create CSV file. Error occurred with message: {ex}"))


def clear_db(args=None, _from=None):
    if _from != "run":
        puts(colored.red("This will clear the Database. It is advised to create a CSV backup first using the command: "
                         "to-csv"))
        resp = prompt.yn("\nAre you sure to continue?")
        if not resp:
            return

    puts(colored.red("Deleting DB..."))
    business_db.delete_all()


def exit(args=None):
    global _exit
    _exit = True
    puts("Exiting program")


def dispatcher(command):
    switch = {
        "help": help,
        "init": init,
        "run": run,
        "to-csv": to_csv,
        "clear-db": clear_db,
        "exit": exit
    }

    args = []

    if len(command.split(" ")) > 1:
        args = command.split(" ")[1:]

    func = None

    try:
        func = switch[command.split(" ")[0]]
    except KeyError:
        puts(colored.red(f"Invalid command {command}. Please try again"))
        return

    if func is not None:
        return func(args)
    else:
        puts(colored.red('Warning: ') + 'No Commands matched\n')
        return help(args)


_exit = False


def start():
    while not _exit:
        # Get Command

        command = prompt.query(">>")
        dispatcher(command)
