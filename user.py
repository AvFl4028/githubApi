import requests
from bs4 import BeautifulSoup


class User:
    def __init__(self) -> None:
        self.__url: str = "https://github.com/"
        self.__username: str = ""
        self.__reposUrl: str = ""
        self.__yearlyContributions: str = ""
        self.__repos: list = []

    def __makeRq(self, url: str | None = None):
        if url is None:
            return requests.get(self.__url).content
        else:
            return requests.get(url).content

    def rq(self):
        print(self.__makeRq())

    def setUser(self, user: str):
        self.__username = user
        self.__reposUrl = f"{self.__url}{self.__username}/?tab=repositories"

    def __getRepositories(self):
        if self.__username == None or self.__username == "":
            return {"title": "No username"}

        if len(self.__repos) != 0:
            return self.__repos

        rq = self.__makeRq(self.__reposUrl)
        repos = BeautifulSoup(rq, features="html.parser")

        for item in repos.find_all("a", "next_page"):
            # print(f"{self.__url}{item.attrs["href"]}")

            repos.append(
                BeautifulSoup(
                    self.__makeRq(f"{self.__url}{item.attrs["href"]}"),
                    features="html.parser",
                )
            )
            # print(repos)

        for item in repos.find_all(id="user-repositories-list"):
            for sub_item in item.find_all("li"):
                self.__repos.append(self.__get_content_repo(sub_item))

    def __get_content_repo(self, rq: BeautifulSoup) -> dict:
        results = {}
        card: BeautifulSoup = rq.div
        title: str = card.div.h3.a.text

        def filter_pg_lg(tag) -> bool:
            return (
                tag.has_attr("itemprop")
                and not tag.has_attr("class")
                and tag.name == "span"
            )

        pg_lg: str = ""
        for item in card.find_all(filter_pg_lg):
            pg_lg = item.text

        time: str = ""
        for item in card.find_all("relative-time"):
            time = item.text

        results["title"] = title.strip()
        results["pg_lang"] = pg_lg
        results["time"] = time

        return results

    def get_repository(self, index: int):
        if len(self.__repos) == 0:
            self.__getRepositories()

        print(len(self.__repos))

        if index >= len(self.__repos) or index < 1:
            return None

        return self.__repos[index]

    def get_all_repositorys(self):
        if len(self.__repos) == 0:
            self.__getRepositories()
        return self.__repos

    def search_repo(self, name: str):
        if len(self.__repos) <= 0:
            self.__getRepositories()
            if len(self.__repos) <= 0:
                return {}

        if not name == None or not name == "":
            for item in self.__repos:
                if item["title"] == name:
                    return item

        return {}
