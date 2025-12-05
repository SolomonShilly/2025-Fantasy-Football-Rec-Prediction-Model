import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

class QBScraper:
    def __init__(self, urls, response):
        self.url = urls
        self.response = response
        self.driver = webdriver.Chrome()

    def startChrome(self):
        self.driver.get(self.url)
        title = self.driver.title
        print(f'Connected to {title} successfully')

    def Scrape(self):
        with open(f"QBstats{self.response}.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["name", 'team', "qbr", "plays", 'epa', 'sack', 'raw', 'year'])

        for n in range (1,41):
            name = self.driver.find_element(By.XPATH,
                                            f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/table/tbody/tr[{n}]/td[2]/div/a').text
            team = self.driver.find_element(By.XPATH, f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/table/tbody/tr[{n}]/td[2]/div/span').text
            qbr = self.driver.find_element(By.XPATH,
                                          f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div/div[2]/div/div[2]/table/tbody/tr[{n}]/td[1]').text
            plays = self.driver.find_element(By.XPATH,
                                           f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div/div[2]/div/div[2]/table/tbody/tr[{n}]/td[3]').text
            epa = self.driver.find_element(By.XPATH,
                                            f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div/div[2]/div/div[2]/table/tbody/tr[{n}]/td[4]').text
            sack = self.driver.find_element(By.XPATH,
                                              f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div/div[2]/div/div[2]/table/tbody/tr[{n}]/td[7]').text
            raw = self.driver.find_element(By.XPATH,
                                          f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div/div[2]/div/div[2]/table/tbody/tr[{n}]/td[9]').text

            year = self.response
            print(name, team, qbr, plays, epa, sack, raw, year)
            with open(f"QBstats{self.response}.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, team, qbr, plays, epa, sack, raw, year])
    def closeChrome(self):
        self.driver.close()

def main():
    urls = []
    responses = []
    response = input("Please enter the year you would like to scrape: ")
    while response.lower() != "no":
        responses.append(response)
        urls.append(f'https://www.espn.com/nfl/qbr/_/season/{response}/seasontype/2')
        response = input("Please enter the year you would like to scrape. When you are done, type 'no': ")

    for url, response in zip(urls,responses):
        print(url, response)
        x = QBScraper(url, response)
        x.startChrome()
        x.Scrape()
        x.closeChrome()
        sleep(5)

if __name__ == '__main__':
    main()