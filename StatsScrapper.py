# Goal: Rank WRs for the 2025-2026 NFL season based on where I think they will finish
# Scrape WR stats
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

class WRScraper:
    def __init__(self, urls, response):
        self.url = urls
        self.response = response
        self.driver = webdriver.Chrome()

    def startChrome(self):
        self.driver.get(self.url)
        title = self.driver.title
        print(f'Connected to {title} successfully')

    def Scrape(self):
        with open(f"WRstats{self.response}.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["name", 'team', "gp", "rec", 'tgts', 'recYds', "recTD", "recYdsPer", "yac", "firstDowns", "avgPerRec"])

        for n in range (1,201):
            if n == 50 or n == 100 or n == 150:
                button = self.driver.find_element(By.XPATH, f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[2]/a')
                button.click()

            name = self.driver.find_element(By.XPATH,
                                            f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/table/tbody/tr[{n}]/td[2]/div/a').text
            team = self.driver.find_element(By.XPATH, f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/table/tbody/tr[{n}]/td[2]/div/span').text
            gp = self.driver.find_element(By.XPATH,
                                          f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[2]').text
            rec = self.driver.find_element(By.XPATH,
                                           f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[3]').text
            tgts = self.driver.find_element(By.XPATH,
                                            f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[4]').text
            recYds = self.driver.find_element(By.XPATH,
                                              f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[5]').text
            td = self.driver.find_element(By.XPATH,
                                          f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[7]').text
            recYdsPer = self.driver.find_element(By.XPATH,
                                                 f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[10]').text
            yac = self.driver.find_element(By.XPATH,
                                           f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[13]').text
            firstDowns = self.driver.find_element(By.XPATH,
                                                  f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[14]').text
            avgPerRec = self.driver.find_element(By.XPATH, f'//*[@id="fittPageContainer"]/div[2]/div[2]/div/div/section/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr[{n}]/td[6]').text

            print(name, team, gp, rec, tgts, recYds, td, recYdsPer, yac, firstDowns, avgPerRec)
            with open(f"WRstats{self.response}.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, team, gp, rec, tgts, recYds, td, recYdsPer, yac, firstDowns, avgPerRec])
    def closeChrome(self):
        self.driver.close()

def main():
    urls = []
    responses = []
    response = input("Please enter the year you would like to scrape: ")
    while response.lower() != "no":
        responses.append(response)
        urls.append(f'https://www.espn.com/nfl/stats/player/_/stat/receiving/season/{response}/seasontype/2/table/receiving/sort/receivingYards/dir/desc')
        response = input("Please enter the year you would like to scrape. When you are done, type 'no': ")

    for url, response in zip(urls,responses):
        print(url, response)
        x = WRScraper(url, response)
        x.startChrome()
        x.Scrape()
        x.closeChrome()
        sleep(5)

if __name__ == '__main__':
    main()