from src.console import console

import requests


class Account:
    def __init__(self, username):
        self.username = username

    def get_profile(self):
        cute_profiles = []
        url = f"https://sky.shiiyu.moe/api/v2/talismans/{self.username}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an error for bad responses
            data = response.json()
            profiles = data.get("profiles", {})

            for _, profile_info in profiles.items():
                profile_name = profile_info.get("cute_name", "Unknown Profile")
                cute_profiles.append(profile_name)
        except requests.RequestException as e:
            console.print(
                f"[bold red]Error fetching profiles for {self.username}: {e}[/bold red]"
            )

        return cute_profiles
