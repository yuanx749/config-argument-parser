from configargparser import gap

a_string = "abc"
a_float = 1.23
a_boolean = False
an_integer = 0


class TestConfigArgumentParser:
    def setup_method(self):
        self.args = {
            "a_string": a_string,
            "a_float": a_float,
            "a_boolean": a_boolean,
            "an_integer": an_integer,
        }
        self.parser = gap.GlobalArgumentParser()
        self.parser._read_globals(stack=1)

    def teardown_method(self):
        self.args = {
            "a_string": a_string,
            "a_float": a_float,
            "a_boolean": a_boolean,
            "an_integer": an_integer,
        }
        self.parser = gap.GlobalArgumentParser()

    def test_read_globals(self):
        assert self.parser.defaults == self.args

    def test_parse_args_default(self):
        self.parser._add_arguments()
        self.parser._parse_args([])
        assert self.parser.args == self.args

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

    def test_update_globals(self):
        self.parser.parse_globals("-b -f 1".split(), shorts="sfb")
        assert a_string == "abc"
        assert a_float == 1.0
        assert a_boolean
        assert an_integer == 0
