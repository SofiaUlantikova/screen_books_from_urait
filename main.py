# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import cv2
import numpy as np
from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
from tkinter import ttk
window = Tk()
first_page = 1
last_page = ''
name_for_pdf = ''
delay = 10
url_of_book = ''
def get_data_and_start():
    global first_page, last_page, name_for_pdf, delay, url_of_book
    if cb.get() != "all":
        first_page = int(txtfld_first_page.get())
        last_page = int(txtfld_last_page.get())
    name_for_pdf = txtfld_pdf.get()
    if txtfld_delay.get() != '':
        delay = txtfld_delay.get()
    url_of_book = txtfld_url.get()
btn = Button(window, text="Отправить и запустить", fg='blue', command=get_data_and_start)
btn.place(x=80, y=100)
lbl_pdf = Label(window, text="Как назвать пдф-файл?", fg='red', font=("Helvetica", 12))
lbl_pdf.place(x=60, y=50)
txtfld_pdf = Entry(window, text="Имя пдф-файла", bd=5)
txtfld_pdf.place(x=80, y=150)

lbl_url = Label(window, text="Введите URL книги без последнего символа - номера страницы", fg='red', font=("Helvetica", 12))
lbl_url.place(x=80, y=200)
txtfld_url = Entry(window, text="Адрес книги (https://.../#page)", bd=5)
txtfld_url.place(x=80, y=250)

pages_selection = StringVar()
pages_selection.set("all")
data = ("all", "задать диапазон вручную")
cb = ttk.Combobox(window, values=data)
cb.place(x=60, y=300)

lbl_delay = Label(window, text="Сколько ждать загрузки следующей страницы?", fg='red', font=("Helvetica", 12))
lbl_delay.place(x=10, y=350)
txtfld_delay = Entry(window, text="Время загрузки (опционально, 10 с по умолчанию", bd=5)
txtfld_delay.place(x=120, y=400)

lbl_pages = Label(window, text="Задать вручную диапазон страниц:", fg='red', font=("Helvetica", 12))
lbl_pages.place(x=10, y=450)
txtfld_first_page = Entry(window, text="Первая страница", bd=5)
txtfld_first_page.place(x=60, y=500)
txtfld_last_page = Entry(window, text="Последняя страница", bd=5)
txtfld_last_page.place(x=120, y=500)

window.title('Параметры книги для сохранения')
window.geometry("300x550+10+10")
window.mainloop()
list_ims = list()
# Create point matrix get coordinates of mouse click on image
point_matrix = np.zeros((2, 2), dtype=int)
point_matrix_temporal = np.zeros((2, 2), dtype=int)
counter = 0

'''[first_page, last_page, name_for_pdf, delay, url_of_book] - input'''

def mousePoints(event, x, y, flags, params):
    global counter
    # Left button mouse click event opencv
    if counter == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            point_matrix[counter] = x, y
            point_matrix_temporal[counter] = x, y
            counter += 1
            print(point_matrix)
    elif counter == 1:
        if event == cv2.EVENT_LBUTTONUP:
            point_matrix[counter] = x, y
            counter += 1
            print(point_matrix)
            print(counter)
        elif event == cv2.EVENT_MOUSEMOVE:
            point_matrix_temporal[counter] = x, y
            temp = img.copy()
            cv2.rectangle(temp, (point_matrix_temporal[0][0], point_matrix_temporal[0][1]), (point_matrix_temporal[1][0], point_matrix_temporal[1][1]), (255,155,0),2,8)
            cv2.imshow("page", temp)


def screen_page(num_page, url_of_book, time_delay=10):
    driver.get(url_of_book + str(num_page))
    time.sleep(time_delay)
    driver.save_screenshot('./page' + str(i) + '.png')

# Read image
img = cv2.imread('page'+str(first_page)+'.png')
k = 0
while counter < 2: # not press q

    cv2.imshow("pag", img)
    # Mouse click event on original image
    cv2.setMouseCallback("pag", mousePoints)
    cv2.waitKey(1)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

cv2.destroyAllWindows()
starting_x = point_matrix[0][0]
starting_y = point_matrix[0][1]
ending_x = point_matrix[1][0]
ending_y = point_matrix[1][1]

i = first_page
if isinstance(last_page):
    page_existence = (i <= last_page)
else:
    page_existence = True # if the user skipped to define page list (chose all pages)
while page_existence:
    try:
        screen_page(i, delay) # make screenshot of current page
    except WebDriverException: # the page is out of range
        break
    im_screen = cv2.imread('page'+str(i)+'.png')
    screenshot_cropped = im_screen[starting_y:ending_y, starting_x:ending_x] # crop rectangle as a user selected
    os.remove("page"+str(i)+".png")
    cv2.imwrite('cropped'+str(i)+'.png', screenshot_cropped)
    im_cropped = Image.open('cropped' + str(i) + '.png')
    pdf_cropped = im_cropped.convert('RGB')
    if i > first_page:
        list_ims.append(pdf_cropped)
    else:
        image_to_start = pdf_cropped
image_to_start.save(name_for_pdf + '.pdf', save_all=True, append_images=list_ims)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
