import requests
from requests.exceptions import RequestException

from bs4 import BeautifulSoup

if __name__ == "__main__":
	site_url = input("Podaj adres url do strony na wikipedii: ")

	try:
		site = requests.get(site_url)
		if site is None:
			print("Error!")
			exit(-1)

		if site.status_code == 200:
			parsed = BeautifulSoup(site.text, 'html.parser')

			print("Pierwszy akapit: ")
			akapit = parsed.find("p")
			if akapit is not None:
				print(akapit.text)
			else:
				print("Nie znaleziono zadnego akapitu.")

			navigation = parsed.find(role="navigation")
			if navigation is not None:
				print("Lista wszystkich sekcji: ")
				for li in navigation.select('li'):
					if li is not None:
						print(li.text)
					else:
						print("Pusta wartosc li.")
			else:
				print("Nie znaleziono listy sekcji!")

			lista_img = parsed.select('img')
			if lista_img is not None:
				print("Lista adresów url do zdjęć i grafik: ")
				for href in lista_img:
					if href is not None:
						if href.has_attr("src") == True:
							if href["src"][1] == '/':
								print("https:" + href["src"])
							else:
								print("https://pl.wikipedia.org" + href["src"])
						else:
							print("Brak parametru src!")
					else:
						print("Pusta wartosc href! ")

		else:
			print("Error " + site.status_code)

	except RequestException as e:
		print('Error dla podanego url {0} : {1}'.format(site_url, str(e)))
		exit(-2)

	exit(0)
