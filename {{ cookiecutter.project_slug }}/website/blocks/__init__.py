from coderedcms.blocks import *
from coderedcms.blocks.html_blocks import *
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from .content_blocks import BasicContentBlock

CONTENT_STREAMBLOCKS += [
    ("h1", H1Block()),
    ("content", BasicContentBlock(CONTENT_STREAMBLOCKS)),
]

LAYOUT_STREAMBLOCKS = [
    (
        "hero",
        HeroBlock(
            [
                ("row", GridBlock(CONTENT_STREAMBLOCKS)),
                (
                    "cardgrid",
                    CardGridBlock(
                        [
                            ("card", CardBlock()),
                        ]
                    ),
                ),
                (
                    "html",
                    blocks.RawHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
    ("row", GridBlock(CONTENT_STREAMBLOCKS)),
    (
        "cardgrid",
        CardGridBlock(
            [
                ("card", CardBlock()),
            ]
        ),
    ),
    (
        "html",
        blocks.RawHTMLBlock(icon="code", form_classname="monospace", label=_("HTML")),
    ),
    (
        "content",
        BasicContentBlock(CONTENT_STREAMBLOCKS),
    ),
]
