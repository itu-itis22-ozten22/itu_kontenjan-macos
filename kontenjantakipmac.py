import mechanize
from bs4 import BeautifulSoup
import openpyxl
import time
import subprocess  # Added subprocess module for running AppleScript commands

wb = openpyxl.Workbook()
ws = wb.active

ders = input("Ders kodu giriniz:").upper()
crn = input("Crn numarası giriniz:")

def itukont(ders, crn):
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.open("https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS")
    browser.select_form(nr=0)
    browser.form["derskodu"] = [ders[:3]]

    browser.submit()
    soup_table = BeautifulSoup(browser.response().read(), 'lxml')
    table = soup_table.find('table')

    a = 0
    c = 0
    for i in table.find_all('tr'):
        b = 0
        c += 1
        if c == 1 or c == 2:
            pass
        else:
            a += 1
        for j in i.find_all('td'):
            b += 1
            if c == 1 or c == 2:
                pass
            else:
                ws.cell(column=b, row=a).value = j.get_text(strip=True)

    for row in ws.rows:
        if row[0].value == crn:
            if int(row[9].value) > int(row[10].value):
                check = "Kontenjan var"
                print(check)

                # Send a notification using AppleScript
                applescript_command = f'display notification "{check}" with title "Kontenjan Bildirimi"'
                subprocess.run(["osascript", "-e", applescript_command])
            else:
                check = "Kontenjan yok"
                print(check)

            break


while True:
    itukont(ders, crn)
    time.sleep(900)
