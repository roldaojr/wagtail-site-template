from django.utils.translation import gettext_lazy as _
from coderedcms.blocks.base_blocks import BaseLayoutBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks


class BasicBlock(BaseLayoutBlock):
    """
    Simple block to render content
    """

    class Meta:
        template = "website/blocks/div_block.html"
        icon = "placeholder"
        label = _("Block")


class SectionBlock(BaseLayoutBlock):
    """Page section layout block"""

    title = blocks.CharBlock(label=_("Title"), required=False)
    subtitle = blocks.CharBlock(label=_("Subtitle"), required=False)
    image = ImageChooserBlock(label=_("Image"), required=False)

    class Meta:
        template = "website/blocks/section_block.html"
        icon = "placeholder"
        label = _("Section")
