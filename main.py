import pandas as pd
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


def count_words(df, t1, t234, titles):
    count = 0
    whole = len(df)
    # Make sure you have geckodriver set up properly
    browser = webdriver.Firefox(executable_path='C:/Users/jaked/Documents/tools/geckodriver')
    browser.set_page_load_timeout(30)

    for i in range(len(df)):
        website = df.loc[i, "Web Address (URL)"]
        website = "http://" + website.lower()
        tier = 0
        try:
            browser.get(website)
            source = browser.find_element_by_tag_name("body").get_attribute("innerText")
            str_source = str(source).lower()
            for word in t1:
                df.at[i, word] = str_source.count(word)
                if tier == 0 and str_source.count(word) > 0:
                    tier = 1
            if str_source.count("concrete"):
                for word in t234:
                    df.at[i, "concrete AND " + word] = str_source.count(word)
                    if tier == 0 and str_source.count(word) > 0:
                        tier = 2
            else:
                for word in t234:
                    df.at[i, word] = str_source.count(word)
                    if tier == 0 and str_source.count(word) > 1:
                        tier = 3
            if tier == 0:
                tier = 4
            df.at[i, "tier"] = tier
        except selenium.common.exceptions.WebDriverException or TimeoutException:
            print("DNE")
            for word in titles:
                df.at[i, word] = 0

        count += 1
        print("\n-------------------------")
        print(count, " of ", len(df), "websites visited.\n-------------------------")
        print(round(count/whole, 4) * 100, "% websites visited.")
        print("-------------------------")
    browser.close()

    return df


def counter():
    titles = ["tier", "concrete restoration", "epoxy coatings", "floot coatings", "floor demo", "floor demolition",
              "floor maintenance", "flooring maintenance", "floor restoration", "flooring restoration",
              "surface preparation", "concrete AND flooring", "concrete AND surfacing", "concrete AND restoration",
              "concrete AND coating", "concrete AND construction", "concrete AND polishing", "concrete AND painting",
              "concrete AND demolition", "concrete AND epoxy", "flooring", "surfacing", "restoration", "coating",
              "construction", "polishing", "painting", "demolition", "epoxy"]

    tier_1 = ['concrete restoration', 'epoxy coatings', 'floor coatings', 'floor demo',
              'floor demolition', 'floor maintenance', 'flooring maintenance', 'floor restoration',
              'flooring restoration', 'surface preparation']

    tier_234 = ["flooring", "surfacing", "restoration", "coating", "construction", "polishing",
                "painting", "demolition", "epoxy"]

    df = pd.read_csv("word_count.csv")

    new_df = count_words(df, tier_1, tier_234, titles)

    new_df.to_csv("counted.csv")


if __name__ == '__main__':
    counter()
