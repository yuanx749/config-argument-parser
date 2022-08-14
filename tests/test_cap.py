import os
from tempfile import mkstemp

from configargparser import cap

conf_str = """[DEFAULT]
# Help message of the first argument. Help is optional.
a_string = 'abc'
a_float = 1.23  # inline comments are omitted
# Help can span multiple lines.
# This is another line.
a_boolean = False
an_integer = 0
"""


class Args:
    # Help message of the first argument. Help is optional.
    a_string = "abc"
    a_float = 1.23  # inline comments are omitted
    # Help can span multiple lines.
    # This is another line.
    a_boolean = False
    an_integer = 0


class TestConfigArgumentParser:

    parser = cap.ConfigArgumentParser()

    def setup_method(self):
        self.parser.read_string(conf_str)

    def teardown_method(self):
        self.parser._init_parser()

    def test_read_file(self):
        fd, fname = mkstemp()
        with open(fname, "w") as fp:
            fp.write(conf_str)
        parser = cap.ConfigArgumentParser()
        parser.read(fname)
        assert parser.defaults == self.parser.defaults
        assert parser.help == self.parser.help
        os.close(fd)
        os.remove(fname)

    def test_read_py(self):
        fd, fname = mkstemp(suffix=".py")
        with open(fname, "w") as fp:
            fp.write("# " + conf_str)
        parser = cap.ConfigArgumentParser()
        parser.read_py(fname)
        assert parser.defaults == self.parser.defaults
        assert parser.help == self.parser.help
        os.close(fd)
        os.remove(fname)

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
        assert (
            self.parser.defaults
            == self.parser.args
            == {"a_string": "abc", "a_float": 1.23, "a_boolean": False, "an_integer": 0}
        )

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

    def test_parse_args(self):
        self.parser.parse_args("-b -f 1".split(), shorts="sfb")
        assert self.parser.args["a_string"] == "abc"
        assert self.parser.args["a_float"] == 1.0
        assert self.parser.args["a_boolean"]
        assert self.parser.args["an_integer"] == 0

    def test_read_obj(self):
        args = Args()
        parser = cap.ConfigArgumentParser()
        parser._read_obj(args)
        assert parser.defaults == self.parser.defaults
        assert parser.help == self.parser.help

    def test_parse_obj(self):
        args = Args()
        self.parser.parse_obj(args, "-b -f 1".split(), shorts="sfb")
        assert args.__dict__ == {
            "a_string": "abc",
            "a_float": 1.0,
            "a_boolean": True,
            "an_integer": 0,
        }
