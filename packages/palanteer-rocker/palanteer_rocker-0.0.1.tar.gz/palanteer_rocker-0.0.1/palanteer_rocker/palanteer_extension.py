import pkgutil
from rocker.extensions import RockerExtension


class PalanteerExtension(RockerExtension):
    @staticmethod
    def get_name():
        return "palanteer"

    def __init__(self):
        self.name = PalanteerExtension.get_name()

    def get_snippet(self, cliargs):
        return pkgutil.get_data(
            "palanteer_rocker", "templates/{}_snippet.Dockerfile".format(self.name)
        ).decode("utf-8")

    @staticmethod
    def register_arguments(parser, defaults=None):
        if defaults is None:
            defaults = {}
        parser.add_argument(
            f"--{PalanteerExtension.get_name()}",
            action="store_true",
            default=defaults.get("palanteer"),
            help="add palanteer to your docker image",
        )
