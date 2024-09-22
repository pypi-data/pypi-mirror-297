from colorama import Back, Fore, Style, just_fix_windows_console

just_fix_windows_console()


def colorize(color: str, message: str):
    return Style.BRIGHT + color + message + Fore.RESET + Back.RESET + Style.RESET_ALL


def main():
    print("")

    print(
        f"  You met {colorize(Fore.BLUE, "David Brownman")} at {colorize( Fore.YELLOW, "PyBay 2024")}!"
    )

    print("\n  Find him online:")
    print(f"\n    🌐 Website:  {colorize(Fore.CYAN, 'https://xavd.id')}")
    print(
        f"\n    🐘 Mastodon: {colorize(Fore.MAGENTA, "https://mastodon.social/@xavdid")}"
    )
    print(f"\n    🧑‍💻 GitHub:   {colorize(Fore.GREEN, "https://github.com/xavdid")}")

    print(f"\n  or as {colorize(Fore.CYAN, '@xavdid')} wherever you get your websites.")

    print("")
