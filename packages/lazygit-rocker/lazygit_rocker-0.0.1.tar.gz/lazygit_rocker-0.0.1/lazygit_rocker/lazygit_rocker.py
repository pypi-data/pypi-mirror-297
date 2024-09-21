import pkgutil
from rocker.extensions import RockerExtension


class LazygitExtension(RockerExtension):
    @staticmethod
    def get_name():
        return "lazygit"

    def __init__(self):
        self.name = LazygitExtension.get_name()

    # TODO Investigate why this does not work
    # These snippets do not work as I would expect, I still need to apt install git as part of this extension for lazydocker to work
    # def invoke_after(self, cliargs) -> typing.Set[str]:
    #     """
    #     This extension should be loaded after the extensions in the returned
    #     set. These extensions are not required to be present, but if they are,
    #     they will be loaded before this extension.
    #     """
    #     return set(["git"])

    # def required(self, cliargs) -> typing.Set[str]:
    #     """
    #     Ensures the specified extensions are present and combined with
    #     this extension. If the required extension should be loaded before
    #     this extension, it should also be added to the `invoke_after` set.
    #     """
    #     return set(["git"])

    def get_snippet(self, cliargs):
        return pkgutil.get_data(
            "lazygit_rocker", "templates/{}_snippet.Dockerfile".format(self.name)
        ).decode("utf-8")

    @staticmethod
    def register_arguments(parser, defaults=None):
        if defaults is None:
            defaults = {}
        parser.add_argument(
            f"--{LazygitExtension.get_name()}",
            action="store_true",
            default=defaults.get("lazygit"),
            help="add lazygit to your environment",
        )
