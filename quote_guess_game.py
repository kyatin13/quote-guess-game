from bs4 import BeautifulSoup
import requests
from random import randint

def Extract():
	global pagenumber

	page = pagenumber.pop(randint(0,len(pagenumber)-1))
	req = requests.get(f"http://quotes.toscrape.com/page/{page}/")
	site = BeautifulSoup(req.text , "html.parser")
	spans = site.find_all(class_="quote")
	info = [{
			"quote" : span.find(class_="text").get_text() ,
			"author": span.find(class_="author").get_text(),
			"link" : span.find("a")["href"]
			}
			for span in spans
			]
	return info

def start_game():
	global tries,a,q,a_info1,a_info2,info,pagenumber

	tries = 4
	if len(info) == 0:
		info = Extract()
	c = randint(0,(len(info)-1))
	instance = info.pop(c)
	a = instance.get("author")
	q = instance.get("quote")
	l = instance.get("link")
	about = requests.get(f"http://quotes.toscrape.com{l}")
	about_site = BeautifulSoup(about.text , "html.parser")
	a_info1 = about_site.find(class_="author-born-date").get_text()
	a_info2 = about_site.find(class_="author-born-location").get_text()

def Hints():
	global tries,a

	if tries==3:	
		print(f"\n\n\n his first name if from letter : {a[0]}")		
	
	elif tries==2:
		ln = a.split(" ")[1][0] 
		print(f"\n\n\n his last name if from letter : {ln}")	
	
	elif tries==1:
		print(f"\n\n\n the author was born on {a_info1} \n birth place if {a_info2}")

def main():
	global info,tries,a,q,pagenumber
	info = Extract()
	start_game()
	while tries>=1:	
		print(f"who said: \n {q} \n you have {tries} tries\n")
		answer = input("enter the author's name :")
		
		if answer!=a:
			tries-=1	
			
			if tries==0:
				print(f"mmm u were not able to guess it ..... it was said by {a}\n" )
				b = input("would u like to play again: ")
				
				if b[0].lower()=="y":
					
					if len(pagenumber)==0:
						print("thats enough for the day")
						break
					start_game()

				else: break

			else:
				Hints()

		else:
			print("you are right about that one\n\n\n")
			b = input("would u like to play again: ")
			
			if b[0].lower()=="y":
				if len(pagenumber)==0:
					print("thats enough for the day")
					break
				start_game()			

			else: break

if __name__ == "__main__":
	pagenumber = list(range(1,11))
	main()
