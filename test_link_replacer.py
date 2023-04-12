import main
import pytest

@pytest.mark.parametrize("test_input, expected", [
    ('basic string', 'basic string'),
    ('test [[1 link]] more text [[1.2 another link]] text text', 'test {{< ref "1 link" >}} more text {{< ref "1.2 another link" >}} text text'),
    ('text [[2 link]] text', 'text {{< ref "2 link" >}} text'),
    ('text [[3 link|this is the text for the link]] text', 'text [this is the text for the link]({{< ref "3 link" >}}) text'),
    ('```print("[[hello world]]")```', '```print("[[hello world]]")```'),
    ('[[]]', '[[]]'),
    ('test [[link | custom name of link]]', 'test [custom name of link]({{< ref "link" >}})'),
])

def test_the_link_replacer(test_input, expected):
    assert expected == main.replace_links(test_input)
