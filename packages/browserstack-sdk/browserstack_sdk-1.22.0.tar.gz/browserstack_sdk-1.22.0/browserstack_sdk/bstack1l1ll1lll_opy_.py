# coding: UTF-8
import sys
bstack11l1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack1l1lll_opy_ = 7
def bstack1lll1l_opy_ (bstack11llll_opy_):
    global bstackl_opy_
    bstack1ll1lll_opy_ = ord (bstack11llll_opy_ [-1])
    bstack1l11111_opy_ = bstack11llll_opy_ [:-1]
    bstack1ll111l_opy_ = bstack1ll1lll_opy_ % len (bstack1l11111_opy_)
    bstack1llllll1_opy_ = bstack1l11111_opy_ [:bstack1ll111l_opy_] + bstack1l11111_opy_ [bstack1ll111l_opy_:]
    if bstack11l1_opy_:
        bstack11ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack1l11l11_opy_ + bstack1ll1lll_opy_) % bstack1l1lll_opy_) for bstack1l11l11_opy_, char in enumerate (bstack1llllll1_opy_)])
    else:
        bstack11ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack1l11l11_opy_ + bstack1ll1lll_opy_) % bstack1l1lll_opy_) for bstack1l11l11_opy_, char in enumerate (bstack1llllll1_opy_)])
    return eval (bstack11ll1l1_opy_)
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l1l11l11_opy_ = {}
        bstack11lllll11l_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨඞ"), bstack1lll1l_opy_ (u"ࠨࠩඟ"))
        if not bstack11lllll11l_opy_:
            return bstack1l1l11l11_opy_
        try:
            bstack11lllll111_opy_ = json.loads(bstack11lllll11l_opy_)
            if bstack1lll1l_opy_ (u"ࠤࡲࡷࠧච") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠥࡳࡸࠨඡ")] = bstack11lllll111_opy_[bstack1lll1l_opy_ (u"ࠦࡴࡹࠢජ")]
            if bstack1lll1l_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤඣ") in bstack11lllll111_opy_ or bstack1lll1l_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤඤ") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥඥ")] = bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧඦ"), bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧට")))
            if bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦඨ") in bstack11lllll111_opy_ or bstack1lll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤඩ") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥඪ")] = bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢණ"), bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧඬ")))
            if bstack1lll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥත") in bstack11lllll111_opy_ or bstack1lll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥථ") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦද")] = bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨධ"), bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨන")))
            if bstack1lll1l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨ඲") in bstack11lllll111_opy_ or bstack1lll1l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦඳ") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧප")] = bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤඵ"), bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢබ")))
            if bstack1lll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨභ") in bstack11lllll111_opy_ or bstack1lll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦම") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧඹ")] = bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤය"), bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢර")))
            if bstack1lll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ඼") in bstack11lllll111_opy_ or bstack1lll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧල") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ඾")] = bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ඿"), bstack11lllll111_opy_.get(bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣව")))
            if bstack1lll1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤශ") in bstack11lllll111_opy_:
                bstack1l1l11l11_opy_[bstack1lll1l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥෂ")] = bstack11lllll111_opy_[bstack1lll1l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦස")]
        except Exception as error:
            logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡥࡹࡧ࠺ࠡࠤහ") +  str(error))
        return bstack1l1l11l11_opy_