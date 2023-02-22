import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
}


def film(film1):
    # print()
    # Realizeaza cererea HTTP si returneaza continutul site-ului
    # film = input("Nume Film care a fost in cinema, fara seriale si filme anuntate: ")
    url = "https://www.imdb.com/find/?q=" + film1 + "&ref_=nv_sr_sm"
    # print("Caut film in baza IMDb...")
    page = requests.get(url, headers=headers)

    # Parsing HTML cu BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("div", {"class": "ipc-metadata-list-summary-item__tc"})
    link = table.find("a", {"class": "ipc-metadata-list-summary-item__t"})
    ln = link.get("href")
    # print("Am gasit film pe adresa: ", ln)
    # print("Caut informatii despre film...")
    url2 = "https://www.imdb.com" + ln
    page = requests.get(url2, headers=headers)

    # Parsing HTML cu BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Gasiti toate elementele cu eticheta "table" si selectati prima
    table = soup.find("div", {"class": "sc-b5e8e7ce-0 dZsEkQ"})
    table = table.find("div", {"class": "ipc-btn__text"})

    imdb = table.find("span", {"class": "sc-e457ee34-1 gvYTvP"}).text

    table = soup.find("section", {"data-testid": "BoxOffice"})
    table = table.find(
        "li", {"data-testid": "title-boxoffice-cumulativeworldwidegross"}
    )
    cost = table.find(
        "label", {"class": "ipc-metadata-list-item__list-content-item"}
    ).text

    # print(
    #    f"Film '{film1.upper()}' are nota {imdb} pe IMDb, acumulat {cost} in toata lumea"
    # )
    return f"Film '{film1.upper()}' are nota {imdb} pe IMDb, acumulat {cost} in toata lumea"


if __name__ == "__main__":
    print(film("Avatar 2"))
