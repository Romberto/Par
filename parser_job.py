"""
парсер скрипт который собирает email почту соискателей ,которые выложили
свою анкету на сайт https://rabota.sakh.com/
складывает данные в resume.csv ,
логи записывает в passer.log


"""
from time import sleep
from logging import getLogger, FileHandler, Formatter, DEBUG, INFO
from selenium import webdriver
import csv

log = getLogger('parser')


def log_config():
    file_handler = FileHandler(filename='parser.log', encoding='utf8')
    file_handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M:%S'))
    file_handler.setLevel(INFO)
    log.addHandler(file_handler)

    log.setLevel(DEBUG)


def main():
    log_config()
    parser()


def save(row):
    with open('resume.csv', 'a', newline='', encoding='utf8') as out_csv:
        writer = csv.writer(out_csv)  # <_csv.writer object at 0x03B0AD80>
        writer.writerow(row)


def parser():
    for page in range(1, 11):
        draver_path = 'C:\PythonExample\webdraverChrome\chromedriver'
        draver = webdriver.Chrome(draver_path)
        draver.get(f'https://rabota.sakh.com/resume?page={page}')
        vacancy = draver.find_elements_by_xpath("//div[@class='resume-item__title-row']//a")
        resume = []
        for i in vacancy:
            href = i.get_attribute('href')
            ufl = {
                'href': href
            }
            resume.append(ufl)

        for i in resume:
            try:
                if i['href'] == 'https://rabota.sakh.com/rules#terms-rules-resume':
                    continue
                draver.get(i['href'])
                draver.find_element_by_id('show-contact-info-mobile').click()
                sleep(0.5)
                mail = draver.find_element_by_xpath("//div[@class='single-entry__contact-piece']//a").get_attribute(
                    'text')
                special = draver.find_element_by_class_name('single-entry__title').text
                row = [special, mail, i['href']]
                save(row=row)

            except Exception as ex:
                log.info(f'{special} {i["href"]} предпочитает чтобы с ним связывались через сайт')
    draver.quit()


if __name__ == '__main__':
    main()
