import requests
from bs4 import BeautifulSoup


def get_curs():
    url = "https://www.curs.md/ro/office/micb"
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table", class_="table table-hover")

    data = []

    for row in table.tbody.find_all("tr"):
        columns = row.find_all("td")
        if columns != []:
            valuta = columns[0].text.strip()
            cump = columns[3].text.strip()[:-2]
            vanz = columns[4].text.strip()[:-2]
            data.append({"Valuta": valuta, "cump.": cump, "vanz.": vanz})
            if valuta == "EUR":
                break
    return data


def tabela_valuta():
    data = get_curs()
    return f"""
    cump {data[0]['cump.']}; vanz {data[0]['vanz.']} - {data[0]['Valuta']}
    cump {data[1]['cump.']}; vanz {data[1]['vanz.']} - {data[1]['Valuta']}
    """


def get_exchange_rate(currency, rate_type):
    data = get_curs()
    currency_dict = next((item for item in data if item["Valuta"] == currency), None)
    if rate_type == "cump":
        return float(currency_dict["cump."].replace(",", "."))
    elif rate_type == "vanz":
        return float(currency_dict["vanz."].replace(",", "."))
    else:
        print("Error! Doar 'cump' sau 'vanz'")
        return "Error!"


def convert_to(input_str):
    rate_type, amount, currency = input_str.split()

    currency = currency.upper()

    if not currency in str("USD EUR"):
        return "Error! Doar 'USD' sau 'EUR'"

    try:
        if float(amount) > 0:
            pass
    except ValueError:
        print("Error! Sa fie numar mai mare ca zero")
        return "Error! Sa fie numar mai mare ca zero"
    exchange_rate = get_exchange_rate(currency, rate_type)
    if "Error" in str(exchange_rate):
        return "Error! Doar 'cump' sau 'vanz'"
    return (
        f"{amount} {currency} * {exchange_rate} = {float(amount) * exchange_rate} lei"
    )


if __name__ == "__main__":
    print("Scimb valutar USD si EUR")
    print("mod de utilizare:")
    print("cump 20 USD, vanz 35 EUR")

    # da erorare
    # gresit 'comp' in loc de 'cump'
    # '2y0' in loc de '20'
    # si 'uyD' in loc de 'USD'
    print(convert_to("comp 2y0 uyD"), "lei")

    # corect
    print(convert_to("vanz 35 EUR"), "lei")
