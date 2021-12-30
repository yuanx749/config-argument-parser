from args import args


class TestConfigArgumentParser:

    conf_str = """
    [DEFAULT]
    # Help message of the first argument. Help is optional.
    a_string = 'abc'
    a_float = 1.23  # inline comments are omitted
    # Help can span multiple lines.
    # This is another line.
    a_boolean = False
    an_integer = 0
    """

    parser = args.ConfigArgumentParser()

    def setup_method(self):
        self.parser.read_string(self.conf_str)

    def teardown_method(self):
        self.parser._init_parser()

    def test_parse_comments(self):
        assert (
            self.parser.help["a_string"]
            == " Help message of the first argument. Help is optional."
        )
        assert self.parser.help["a_float"] is None
        assert (
            self.parser.help["a_boolean"]
            == " Help can span multiple lines. This is another line."
        )

    def test_parse_args_default(self):
        self.parser.add_arguments()
        self.parser.parse_args([])
        assert (
            self.parser.defaults
            == self.parser.args
            == {"a_string": "abc", "a_float": 1.23, "a_boolean": False, "an_integer": 0}
        )

    def test_parse_args(self):
        self.parser.add_arguments()
        self.parser.parse_args("--a_float 1".split())
        assert self.parser.args["a_float"] == 1.0
        self.parser.parse_args(["--a_boolean"])
        assert self.parser.args["a_boolean"]

    def test_parse_args_short(self):
        self.parser.add_arguments(shorts="sfb")
        self.parser.parse_args("-b -f 1".split())
        assert self.parser.args["a_float"] == 1.0
        assert self.parser.args["a_boolean"]
