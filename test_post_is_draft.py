import main
import pytest

@pytest.mark.parametrize("draft_input, expected", [
("""---
draft: false
title: "a title"
---
text""", main.PostStatus.IS_NOT_DRAFT),
#('', ''),

("""---
title: "a title"
draft: true
---
text""", main.PostStatus.IS_DRAFT),

("""---
title: "a title"
---
draft: true""", main.PostStatus.DRAFT_YAML_KEY_DOESNT_EXIST),
])

def test_if_post_is_a_draft(draft_input, expected):
    obsidian_to_hugo = main.Obsidian_to_Hugo()
    assert expected == obsidian_to_hugo._is_post_a_draft(draft_input)
