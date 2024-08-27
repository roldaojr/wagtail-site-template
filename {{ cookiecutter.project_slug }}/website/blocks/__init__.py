from coderedcms.blocks import (
    HTML_STREAMBLOCKS,
    AccordionBlock,
    CardBlock,
    CarouselBlock,
    FilmStripBlock,
    GridBlock,
    ImageGalleryBlock,
    ReusableContentBlock,
)

from .content_blocks import BasicBlock, SectionBlock

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + [
    ("accordion", AccordionBlock()),
    ("card", CardBlock(template="cepedi/blocks/card.html")),
    ("carousel", CarouselBlock()),
    ("film_strip", FilmStripBlock()),
    ("image_gallery", ImageGalleryBlock()),
    ("reusable_content", ReusableContentBlock()),
]

CONTENT_STREAMBLOCKS += [
    ("basicblock", BasicBlock(CONTENT_STREAMBLOCKS)),
]

LAYOUT_STREAMBLOCKS = [
    ("pagesectionblock", SectionBlock(CONTENT_STREAMBLOCKS)),
    ("basicblock", BasicBlock(CONTENT_STREAMBLOCKS)),
    ("row", GridBlock(CONTENT_STREAMBLOCKS)),
]
