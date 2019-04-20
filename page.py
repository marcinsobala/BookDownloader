import requests
from selenium import webdriver
from pathlib import Path
import os
import time
import img2pdf


def download_book():
    options = webdriver.ChromeOptions ()
    options.add_argument ("--ignore-certificate-errors")
    options.add_argument ("--test-type")

    driver = webdriver.Chrome (options=options)
    driver.get ('https://campus.difusion.com/')
    driver.find_element_by_name ('identifier').send_keys ('armando.dumbledore@gmail.com')
    driver.find_element_by_name ('password').send_keys ('123456789')
    driver.find_element_by_xpath ("//button[text()='Conéctate']").click ()

    while True:
        try:
            book_name = input("Open your new book, then type its name and press ENTER: ")
            os.mkdir (Path (f'..\{book_name}'))
            break
        except(OSError):
            print("Your book name can't contain special characters! Give me a better name")

    driver.switch_to.window (driver.window_handles [1])
    driver.switch_to.frame (driver.find_element_by_xpath ("//iframe"))
    driver.find_element_by_xpath ("//input[@title='Insertar número de página']").send_keys ('-1')
    driver.find_element_by_xpath ("//input[@value='Go page']").click()

    img_src = ''
    page_num = 1

    while True:
        img = driver.find_element_by_tag_name('img').get_attribute ('src')
        if img == img_src:
            break
        else:
            img_src = img
            with open(Path(f'..\{book_name}\{str(page_num).zfill(3)}.jpg'), 'wb') as f:
                f.write (requests.get (img).content)

        driver.find_element_by_xpath ("//button[@class='btn go-next']").click()
        page_num += 1

    print ("Your book has been downloaded succesfully!\n")
    driver.quit()

def convert_img_to_pdf():
    def page_num(file_name):
        if file_name.endswith(".jpg"):
            return int(file_name[:-4].lstrip("0"))
        else:
            return

    book_name = input("Type the name of your book and press enter: ")
    book_path = Path(f"..\{book_name}")

    try:
        os.chdir(book_path)
    except(OSError):
        print ("No book of that name exists in program's folder. Check the folder's name and try again\n")
        return

    first = int(input("First page: ").strip())
    last = int(input("Last page: ").strip())
    with open((f"{book_path}.pdf"), "wb") as f:
        f.write(img2pdf.convert([i for i in os.listdir(os.getcwd())
                                 if page_num(i) in range(first, last + 1)]))
    print(f"Pages {first} to {last} of book '{book_name}' have been converted succesfully\n")


prompt_str = ("What you wanna do?\n"
              "1. Download a book\n"
              "2. Convert jpgs to pdf\n"
              "3. Quit\n"
              "Choose: ")

while True:
    question = int(input(prompt_str))
    print('\n')
    if question == 1:
        download_book()
    elif question == 2:
        convert_img_to_pdf()
    elif question == 3:
        print ("Goodbye!")
        time.sleep(5)
        break
    else:
        print("No such option. You need to give me proper input!")




