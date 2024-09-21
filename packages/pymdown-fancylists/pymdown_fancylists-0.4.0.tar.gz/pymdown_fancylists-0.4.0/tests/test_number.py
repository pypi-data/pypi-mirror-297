import markdown

class TestNumberedList:
    md = markdown.Markdown(extensions=['fancylists'])

    def test_start_default(self):
        text = (
            '1. List item\n'
            '2. List item\n'
        )
        expected = (
            '<ol type="1">\n'
            '<li>List item</li>\n'
            '<li>List item</li>\n'
            '</ol>'
        )

        result = self.md.convert(text)
        assert result == expected


    def test_start_2(self):
        text = (
            '2. List item\n'
            '3. List item\n'
        )
        expected = (
            '<ol start="2" type="1">\n'
            '<li>List item</li>\n'
            '<li>List item</li>\n'
            '</ol>'
        )

        result = self.md.convert(text)
        assert result == expected


    def test_all_1(self):
        text = (
            '1. List item\n'
            '1. List item\n'
            '1. List item\n'
        )
        expected = (
            '<ol type="1">\n'
            '<li>List item</li>\n'
            '<li>List item</li>\n'
            '<li>List item</li>\n'
            '</ol>'
        )

        result = self.md.convert(text)

        assert result == expected
