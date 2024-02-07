import gettext


class Translator():
    def __init__(self) -> None:
        self.translation = gettext.translation(
            "messages",
            localedir="locales",
            languages=["en_US", "nl_NL"],
            fallback=True
        )
        self.translation.install()

    def __call__(self, message: str) -> str:
        return self.translation.gettext(message)
