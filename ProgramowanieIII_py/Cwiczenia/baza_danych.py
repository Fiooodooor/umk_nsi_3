import sqlite3
import glob
from os import system, name


class StudentBase:
	def __init__(self):
		self.db_selected = ""

	def database(self, change_db: bool):
		db_list = [f[:-3].lower() for f in glob.glob(f"*.db")]
		if len(db_list) == 1 and change_db is False:
			self.db_selected = db_list[0] + ".db"
			print("Wybrana baza danych: " + self.db_selected)
		else:
			print("Istniejace bazy danych: ")
			if len(db_list) == 0:
				print("Brak baz danych.")
			else:
				for n, db in enumerate(db_list, 1):
					print(str(n) + ": " + str(db))
			self.db_selected = input("Podaj nazwe bazy danych: ")
			self.db_selected = self.db_selected + ".db"
			if self.db_selected.lower()[:-3] not in db_list:
				print("Tworze nowa baze danych...")
				self.__create_database()

	def __create_database(self):
		create_table_students = '''CREATE TABLE studenci (
								indeks INTEGER PRIMARY KEY,
								imie TEXT NOT NULL,
								nazwisko text NOT NULL,
								data_urodzenia date NOT NULL);'''
		self.__sql_query(create_table_students)
		create_table_subjects = '''CREATE TABLE przedmioty (
								ID INTEGER PRIMARY KEY AUTOINCREMENT,
								nazwa TEXT NOT NULL,
								prowadzacy_imie text NOT NULL,
								prowadzacy_nazwisko text NOT NULL);'''
		self.__sql_query(create_table_subjects)
		create_table_marks = '''CREATE TABLE oceny (
								ID INTEGER NOT NULL,
								indeks INTEGER NOT NULL,
								ocena INTEGER NOT NULL,		
								FOREIGN KEY(ID) REFERENCES przedmioty(ID),
								FOREIGN KEY(indeks) REFERENCES studenci(indeks)
								);'''
		self.__sql_query(create_table_marks)

	def __sql_connection(self):
		try:
			return sqlite3.connect(self.db_selected)
		except sqlite3.Error as error:
			print(error)

	def __sql_query(self, query: str) -> []:
		try:
			conn = self.__sql_connection()
			cursor = conn.cursor()
			cursor.execute(query)
			results = cursor.fetchall()
			conn.commit()
			cursor.close()
			conn.close()
			return results
		except sqlite3.Error as error:
			print(error)
			return []

	def add_student(self):
		index_list = self.__sql_query('''SELECT indeks FROM studenci;''')
		the_name = input("Podaj imie studenta: ")
		surname = input("Podaj nazwisko studenta: ")
		ur = input("Podaj date urodzenia studenta [dd.mm.rrrr]: ")
		ind = input("Podaj nr. indeksu [nnnnnn]: ")
		while len(ind) != 6 or ind in index_list:
			if ind in index_list:
				ind = input("Indeks juz istnieje! Podaj nr. indeksu [nnnnnn]: ")
			else:
				ind = input("Bledny format! Podaj nr. indeksu [nnnnnn]: ")
		add_student_str = '''INSERT INTO studenci (indeks, imie, nazwisko, data_urodzenia) 
				VALUES ( ''' + ind + ''',\'''' + the_name + '''\',\'''' + surname + '''\', \'''' + ur + '''\');'''
		self.__sql_query(add_student_str)

	def add_subject(self):
		subject = input("Podaj nazwe przedmiotu: ")
		the_name = input("Podaj imie prowadzacego: ")
		surname = input("Podaj nazwisko prowadzacego: ")
		add_subject_str = '''INSERT INTO przedmioty (nazwa, prowadzacy_imie, prowadzacy_nazwisko)
						VALUES (\'''' + subject + '''\', \'''' + the_name + '''\', \'''' + surname + '''\');'''
		self.__sql_query(add_subject_str)

	def add_mark(self):
		index = self.__choose_student()
		if index != '0':
			subject_id = self.__choose_subject()
			if subject_id != '0':
				mark = input("Podaj ocene: ")
				add_mark_string = '''INSERT INTO oceny (id, indeks, ocena) 
								VALUES (''' + subject_id + ''', ''' + index + ''',''' + mark + ''');'''
				self.__sql_query(add_mark_string)
		return

	def list_students(self) -> []:
		student_list_table = self.__sql_query('''SELECT * FROM studenci''')
		for student in student_list_table:
			print(str(student[0]) + ": " + student[1] + " " + student[2] + ", ur. " + student[3])
		if len(student_list_table) <= 0:
			print("(brak rekordow)")
		return student_list_table

	def list_subjects(self) -> []:
		subjects_list_table = self.__sql_query('''SELECT * FROM przedmioty;''')
		for subject in subjects_list_table:
			print(str(subject[0]) + ": " + subject[1] + ", prow. " + subject[2] + " " + subject[3])
		if len(subjects_list_table) <= 0:
			print("(brak rekordow)")
		return subjects_list_table

	def __choose_student(self) -> str:
		index_list = [str(f[0]) for f in self.list_students()]
		if len(index_list) <= 0:
			print("Dodaj min. 1 studenta do bazy aby kontynuować.")
			return '0'
		index = input("Wybierz studenta, podaj nr indeksu lub 0 aby wyjść: ")
		while index != '0' and index not in index_list:
			index = input("Wybierz prawidłowy nr indeksu lub 0 aby wyjść: ")
		return index

	def __choose_subject(self) -> str:
		subject_id_list = [str(f[0]) for f in self.list_subjects()]
		if len(subject_id_list) <= 0:
			print("Dodaj min. 1 przedmiot do bazy aby kontynuować.")
			return '0'
		subject_id = input("Wybierz przedmiot, podaj nr ID lub 0 aby wyjść: ")
		while subject_id != '0' and subject_id not in subject_id_list:
			subject_id = input("Wybierz prawidlowe ID lub 0 aby wyjść: ")
		return subject_id

	def student_avr(self):
		index = self.__choose_student()
		if index != '0':
			the_id = self.__choose_subject()
			if the_id != '0':
				student_avr = "SELECT AVG(ocena) FROM oceny WHERE id=" + the_id + " AND indeks=" + index + ";"
				results = self.__sql_query(student_avr)[0][0]
				if results is not None:
					print("Srednia ocen wynosi: " + "{:.2f}".format(results))
				else:
					print("Srednia ocen wynosi: (brak ocen)")
		return


class Menu:
	@staticmethod
	def main_loop():
		base = StudentBase()
		base.database(False)
		last = '-1'
		while last != '0':
			print("#################################")
			print("BAZA DANYCH: " + base.db_selected[:-3])
			print("#################################")
			print("1. Dodaj studenta")
			print("2. Dodaj przedmiot")
			print("3. Dodaj ocene")
			print("4. Wypisz wszystkich studentow")
			print("5. Wypisz wszystkie przedmioty")
			print("6. Srednia ocen studenta")
			print("9. Zmiana bazy danych")
			print("0. Wyjscie")
			print("#################################")
			last = input("Wybor: ")
			print("")
# dla okna konsoli w srodowisku graficznym:
			print("\n" * 50)
			_ = system('clear' if name != 'nt' else 'cls')
			if last == "1":
				base.add_student()
			elif last == "2":
				base.add_subject()
			elif last == "3":
				base.add_mark()
			elif last == "4":
				print("Studenci: ")
				base.list_students()
			elif last == "5":
				print("Przedmioty: ")
				base.list_subjects()
			elif last == "6":
				base.student_avr()
			elif last == "9":
				base.database(True)
			print(" ")


if __name__ == "__main__":
	Menu.main_loop()
	exit(0)
