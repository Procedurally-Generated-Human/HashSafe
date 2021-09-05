import sys
import functions
import db_conn

first_time = True
quit = False


def main():
	db_conn.create_database()
	functions.draw_logo()
	if db_conn.check_if_first_time():
		functions.first_time_event()
	functions.verify_user()
	functions.main_menu_event()


if __name__ == "__main__":
	main()