from django.utils.translation import gettext_lazy as _
from coderedcms.blocks.base_blocks import BaseLayoutBlock


class BasicContentBlock(BaseLayoutBlock):
    """
    Simple block to render content
    """

    class Meta:
        template = "coderedcms/blocks/base_block.html"
        icon = "placeholder"
        label = _("Basic block")
