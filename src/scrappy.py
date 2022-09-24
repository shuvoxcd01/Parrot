from bs4 import BeautifulSoup
import requests


def get_text_from_web(search_string: str):
    search_string = "+".join(search_string.split())
    res = requests.get("https://bing.com/search?", params={"q": search_string})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    link_elements = soup.find_all("a")
    link_to_open = min(30, len(link_elements))

    texts = []

    for i in range(link_to_open):
        try:
            link = ("https://bing.com" + link_elements[i].get("href"))
            res = requests.get(link)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            all_p = soup.find_all("p")
            for p in all_p:
                texts += [p.text]
        except:
            pass

    return texts
