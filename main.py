from src.profile import Account
from src.constants import colors, rarity_order, rarity_color
from src.accessories import Talismans
from src.console import console

from rich.table import Table
from rich.text import Text
from rich.panel import Panel
import time
from rich.terminal_theme import MONOKAI


def show_profiles(username):
    with console.status("[bold green]Fetching profile..."):
        user_profile = Account(username)
        cute_profiles = user_profile.get_profile()
        time.sleep(1)
    if cute_profiles:
        console.print(f"[bold cyan]Active profiles for {username}[/bold cyan]: ")
        for i, profile in enumerate(cute_profiles):
            console.print(f"{colors[profile][0]}{i+1} - {profile}{colors[profile][1]}")
        return cute_profiles
    else:
        console.print(f"[bold red]No profiles found for {username}[/bold red]")


def get_profile_talismans(talismans):
    with console.status("[bold green]Fetching owned talismans..."):
        owned_talismans = talismans.get_owned_talismans()
        time.sleep(1)
    return owned_talismans


def get_all_talismans(talismans):
    with console.status("[bold green]Fetching all possible talismans..."):
        all_talismans = talismans.get_all()
        time.sleep(1)
    return all_talismans


def get_missing_talismans(owned_talismans, all_talismans, talismans):
    with console.status("[bold green]Fetching missing talismans..."):
        missing_talismans = talismans.get_missing(owned_talismans, all_talismans)
        time.sleep(1)
    return missing_talismans


def results(prices_final, missing):
    console.rule("[bold cyan]Results")

    table = Table(title=missing, show_lines=True)
    table.add_column("Name", justify="left", no_wrap=True)
    table.add_column("Rarity")
    table.add_column("Cost", justify="right")

    for talisman in prices_final:
        table.add_row(
            talisman,
            prices_final[talisman][1],
            (
                f"{prices_final[talisman][0]} coins"
                if prices_final[talisman][0] != 0
                else "Not available"
            ),
            style=rarity_color[prices_final[talisman][1]],
        )

    console.print(table)
    console.save_svg("./svg/missing_talismans.svg", theme=MONOKAI)


def condense_price(price):

    if price < 1000:
        return f"{price}"  # No need to condense
    elif price < 1000000:
        return f"{price / 1000:.2f}k"
    elif price < 1000000000:
        return f"{price / 1000000:.2f}m"
    else:
        return f"{price / 1000000000:.2f}b"


def main():
    with open("./src/logo.txt", "r") as f:
        data = f.read()
    logo = Panel(Text(data, justify="center", style="bold red"))
    console.print(logo)
    console.rule("[bold cyan]Welcome to Talisman Tracker[/bold cyan]")

    username = console.input("\n[bold magenta]Enter username: [/bold magenta]")

    cute_profiles = show_profiles(username)

    profile_choice = (
        int(console.input("\n[bold magenta]Enter the profile number: [/bold magenta]"))
        - 1
    )

    talismans = Talismans(username, cute_profiles[profile_choice])

    owned_talismans = get_profile_talismans(talismans)
    all_talismans = get_all_talismans(talismans)

    missing_talismans = get_missing_talismans(owned_talismans, all_talismans, talismans)
    prices = talismans.get_missing_prices(missing_talismans, all_talismans)

    for item in prices:
        if not isinstance(prices[item], list):
            prices[item] = [0, "N/A"]

    try:
        prices_sorted = dict(
            sorted(
                prices.items(),
                key=lambda item: (
                    item[1][0] if isinstance(item[1], list) and len(item[1]) > 0 else 0
                ),
            )
        )
    except TypeError as e:
        print(f"Error during sorting: {e}")

    prices_final = dict(
        sorted(
            prices_sorted.items(),
            key=lambda item: (rarity_order.index(item[1][1])),
        )
    )

    for item, details in prices_final.items():
        prices_final[item][0] = condense_price(details[0])

    missing = f"[bold cyan]Currently collected {len(owned_talismans)}/{len(all_talismans)}[/bold cyan]"
    results(prices_final, missing)


if __name__ == "__main__":
    main()
