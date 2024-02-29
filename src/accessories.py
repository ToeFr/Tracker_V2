import requests
from src.console import console
from rich.progress import track
import re


class Talismans:
    def __init__(self, username, profile_choice):
        self.username = username
        self.profile_choice = profile_choice

    def get_owned_talismans(self):
        owned_talismans = []
        url = f"https://sky.shiiyu.moe/api/v2/talismans/{self.username}/{self.profile_choice}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            talismans = data["accessories"]["accessories"]

            mc_symbol_pattern = r"\u00a7[a-zA-Z\d]"
            for desc in talismans:
                talisman_name = desc["tag"]["display"]["Name"]
                cleaned_talisman_name = re.sub(mc_symbol_pattern, "", talisman_name)
                owned_talismans.append(cleaned_talisman_name)

        except requests.RequestException as e:
            console.print(f"Error fetching owned talismans: {e}")

        return owned_talismans

    def get_all(self):
        all_talismans = {}
        item_url = "https://api.hypixel.net/v2/resources/skyblock/items"

        try:
            response = requests.get(item_url)
            response.raise_for_status()
            data = response.json()
            for item in data["items"]:
                try:
                    if item["category"] == "ACCESSORY":
                        all_talismans[item["name"]] = item["id"]
                except Exception:
                    continue
        except requests.RequestException as e:
            console.print(f"Error fetching all talismans: {e}")

        return all_talismans

    def get_missing(self, owned_talismans, all_talismans):
        missing_talismans = []
        for talisman in all_talismans:
            if talisman not in owned_talismans:
                missing_talismans.append(talisman)
        return missing_talismans

    def get_missing_prices(self, missing_talismans, all_talismans):
        talisman_prices = {}

        for talisman in track(missing_talismans):
            item_id = all_talismans[talisman]
            item_url = f"https://sky.coflnet.com/api/auctions/tag/{item_id}/active/bin"

            try:
                response = requests.get(item_url, headers={"accept": "text/plain"})
                response.raise_for_status()
                data = response.json()

                talisman_prices[talisman] = [
                    int(data[0]["startingBid"]),
                    data[0]["tier"],
                ]
            except (requests.RequestException, IndexError, KeyError):
                talisman_prices[talisman] = 0

        return talisman_prices
