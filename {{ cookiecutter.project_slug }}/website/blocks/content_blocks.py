from django.utils.translation import gettext_lazy as _
from coderedcms.blocks.base_blocks import BaseLayoutBlock


class BasicBlock(BaseLayoutBlock):
    """
    Simple block to render content
    """

    class Meta:
        template = "website/blocks/basic_block.html"
        icon = "placeholder"
        label = _("Basic block")
