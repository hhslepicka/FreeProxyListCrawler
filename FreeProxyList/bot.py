import os
import itertools
from botcity.base import BaseBot
from botcity.plugins.crawler import BotCrawlerPlugin


class Bot(BaseBot):
    def action(self, execution=None):
        url = "https://free-proxy-list.net/"

        html = BotCrawlerPlugin().request(url)
        # Generator for all rows in table
        rows = html.query_selector("table > tbody").query_selector_iter_all("tr")
        proxies = []
        while next(rows, False):
            # Generator for all cols in each row
            cols = html.query_selector_iter_all("td")
            # Get first two columns (IP and Port) and join them into a string
            proxy = ":".join([c.value() for c in itertools.islice(cols, 2)])
            # Append to the list of proxies
            proxies.append(proxy)

        # Write proxies to proxies.txt file
        with open("proxies.txt", "w") as f:
            f.write(os.linesep.join(proxies))

        # Print statistics
        print(f"Fetched {len(proxies)} proxies.")

if __name__ == '__main__':
    Bot.main()
