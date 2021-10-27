import pandas as pd
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup as bs

TITLES = ["tier", "concrete restoration", "epoxy coatings", "floor coatings", "floor demo", "floor demolition",
          "floor maintenance", "flooring maintenance", "floor restoration", "flooring restoration",
          "surface preparation", "flooring", "surfacing", "restoration", "coating",
          "construction", "polishing", "painting", "demolition", "epoxy", "concrete"]

TIER_1 = ['concrete restoration', 'epoxy coatings', 'floor coatings', 'floor demo',
          'floor demolition', 'floor maintenance', 'flooring maintenance', 'floor restoration',
          'flooring restoration', 'surface preparation']

TIER_234 = ["flooring", "surfacing", "restoration", "coating", "construction", "polishing",
            "painting", "demolition", "epoxy", "concrete"]


def count_words(df):
    count = 0
    whole = len(df)
    # Make sure you have geckodriver set up properly
    browser = webdriver.Firefox(executable_path='C:/Users/jaked/Documents/tools/geckodriver')
    browser.set_page_load_timeout(30)

    for i in range(len(df)):
        website = df.loc[i, "Web Address (URL)"]
        website = "http://" + website.lower()
        tier = 0
        tier_sum = 0
        try:
            browser.get(website)
            source = browser.find_element_by_tag_name("body").get_attribute("innerText")
            str_source = str(source).lower()

            for word in TIER_1:
                df.at[i, word] = str_source.count(word)
                if tier == 0 and str_source.count(word) > 0:
                    tier = 1
            for word in TIER_234:
                df.at[i, word] = str_source.count(word)
                tier_sum += str_source.count(word)
                if tier == 0 and tier_sum > 1 and str_source.count(word) > 1:
                    tier = 2
                elif tier == 0 and tier_sum > 1:
                    tier = 3
                else:
                    tier = 4
            df.at[i, "tier"] = tier
        except selenium.common.exceptions.WebDriverException or TimeoutException:
            print("DNE")
            for word in TITLES:
                df.at[i, word] = 0

        if count % 1000 == 0:
            df.to_csv("counted.csv")

        count += 1
        print("\n-------------------------")
        print(count, " of ", len(df), "websites visited.\n-------------------------")
        print(round(count/whole, 4) * 100, "% websites visited.")
        print("-------------------------")

    df.to_csv("counted.csv")
    browser.close()


def counter():

    df = pd.read_csv("word_count.csv")

    count_words(df)


if __name__ == '__main__':
    counter()
