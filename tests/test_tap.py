from dataclasses import dataclass

from configargparser import tap


@dataclass
class Args:
    # Help message of the first argument. Help is optional.
    a_string: str = "abc"
    a_float: float = 1.23  # inline comments are omitted
    # Help can span multiple lines.
    # This is another line.
    a_boolean: bool = False
    an_integer: int = 0


class TestConfigArgumentParser:
    def setup_method(self):
        self.args = Args()
        self.parser = tap.TypeArgumentParser()
        self.parser._read_obj(self.args)

    def teardown_method(self):
        self.args = Args()
        self.parser = tap.TypeArgumentParser()

    def test_read_obj(self):
        assert self.parser.defaults == self.args.__dict__

    def test_parse_comments(self):
        assert (
            self.parser.help["a_string"]
            == "Help message of the first argument. Help is optional."
        )
        assert self.parser.help["a_float"] == " "
        assert (
            self.parser.help["a_boolean"]
            == "Help can span multiple lines. This is another line."
        )

    def test_parse_args_default(self):
        self.parser._add_arguments()
        self.parser._parse_args([])
        assert self.parser.args == self.args.__dict__

    def test_parse_args_separate(self):
        self.parser._add_arguments()
        self.parser._parse_args("--a-float 1".split())
        assert self.parser.args["a_float"] == 1.0
        self.parser._parse_args(["--a-boolean"])
        assert self.parser.args["a_boolean"]

    def test_parse_args_short(self):
        self.parser._add_arguments(shorts="sfb")
        self.parser._parse_args("-b -f 1".split())
        assert self.parser.args["a_float"] == 1.0
        assert self.parser.args["a_boolean"]

    def test_update_obj(self):
        self.parser.parse_obj(self.args, "-b -f 1".split(), shorts="sfb")
        assert self.args.__dict__ == {
            "a_string": "abc",
            "a_float": 1.0,
            "a_boolean": True,
            "an_integer": 0,
        }
