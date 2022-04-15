import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_url(path="", url="https://habr.com/ru/hub/python/"):    # Проверка на наличие переменной path и формирование url
    u = urlparse(url)
    try:
        if len(path) > 0:
            p = urlparse(path)
            if p.netloc == "":
                our_url = p._replace(scheme=u.scheme, netloc=u.netloc).geturl()
                return our_url
            return p.geturl()
    except TypeError:
        pass
    else:
        return u.geturl()


def demo_soup_href_list(url: str):    # Вывод ссылок с возможностью выбора способа вывода
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    external = soup.find_all("a")
    href_list = []
    for elem in external:
        href_list.append(elem.get("href"))
    condition = input("Print T/F if you want to output data to the terminal/file: ")
    if condition == "T":
        for href in href_list:
            print(href)
    elif condition == "F":
        urlfile = open("Url List.txt", "w")
        for href in href_list:
            urlfile.write(str(href) + "\n")
        urlfile.close()
    return href_list


def url_href(href_list: list):   # Применение предыдущней функции на ссылках из первого вывода
    url_list = []
    for href in href_list:
        if type(href) is str:
            url_list.append(get_url(href))
    for url in url_list:
        try:
            demo_soup_href_list(url)
        except Exception as ex:
            print("Отсутствует ссылка.", ex)
            continue


def main():
    url = get_url()
    url_list = demo_soup_href_list(url)
    url_href(url_list)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        pass
