from scraping import scrape_page
from find_sqli import find_sqli_vulnerabilities

# https://sqli1.comp6841.quoccabank.com/
# https://sqli2.comp6841.quoccabank.com/
# https://sqli3.comp6841.quoccabank.com/
# https://demo.owasp-juice.shop/#
# https://redtiger.labs.overthewire.org/level1.php?cat=1+OR+1=7
# https://nlangford-vulnerable-webapp-7f65a6cee144.herokuapp.com/sqli1/login

# https://xss1.comp6841.quoccabank.com/
# https://xss2.comp6841.quoccabank.com/
# https://xss4.comp6841.quoccabank.com/login
# https://docs.google.com/
# https://circles.csesoc.app/
# https://xss-game.appspot.com/level1/frame
# https://xss-game.appspot.com/level2/frame
# https://xss-game.appspot.com/level3/frame

main_url = input("Please paste URL: ")

scrape_page(main_url, 10)

print("Now Checking recursively for SQLi vulnerabilities... plz be patient again, I am even slower :')...")

output, _ = find_sqli_vulnerabilities(main_url)
the_good_stuff = output.split("---", 2)
if len(the_good_stuff) == 1:
    print("No SQLi vulnerabilities found")
else:
    print("Found the following vulnerabilities:")
    print(the_good_stuff[1])

