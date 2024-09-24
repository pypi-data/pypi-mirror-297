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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l111lll1_opy_, bstack111llllll1_opy_, bstack1l1l11l1_opy_, bstack11ll1l1lll_opy_, bstack1111l11l1l_opy_, bstack111l1111l1_opy_, bstack1111ll111l_opy_, bstack11l111ll1_opy_
from bstack_utils.bstack1lll1111lll_opy_ import bstack1lll111l1ll_opy_
import bstack_utils.bstack11l1lll1l_opy_ as bstack1llllllll1_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11l111l1l_opy_
import bstack_utils.bstack1l111lll11_opy_ as bstack1ll111llll_opy_
from bstack_utils.bstack1l111111l1_opy_ import bstack1l111111l1_opy_
from bstack_utils.bstack11lll1l11l_opy_ import bstack11ll11l1ll_opy_
bstack1ll1l1ll1ll_opy_ = bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᙠ")
logger = logging.getLogger(__name__)
class bstack1111ll111_opy_:
    bstack1lll1111lll_opy_ = None
    bs_config = None
    bstack1l11ll111l_opy_ = None
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l11ll111l_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11ll111l_opy_ = bstack1l11ll111l_opy_
        try:
            cls.bstack1ll1l1ll1l1_opy_()
            bstack111llll11l_opy_ = bstack11l111lll1_opy_(bs_config)
            bstack11l11l11ll_opy_ = bstack111llllll1_opy_(bs_config)
            data = bstack1llllllll1_opy_.bstack1ll1l11ll1l_opy_(bs_config, bstack1l11ll111l_opy_)
            config = {
                bstack1lll1l_opy_ (u"ࠪࡥࡺࡺࡨࠨᙡ"): (bstack111llll11l_opy_, bstack11l11l11ll_opy_),
                bstack1lll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᙢ"): cls.default_headers()
            }
            response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪᙣ"), cls.request_url(bstack1lll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠷࠵ࡢࡶ࡫࡯ࡨࡸ࠭ᙤ")), data, config)
            if response.status_code != 200:
                bstack1ll1l11l11l_opy_ = response.json()
                if bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᙥ")] == False:
                    cls.bstack1ll1ll11111_opy_(bstack1ll1l11l11l_opy_)
                    return
                cls.bstack1ll1l1lll11_opy_(bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᙦ")])
                cls.bstack1ll1l11l111_opy_(bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᙧ")])
                return None
            bstack1ll1l1ll11l_opy_ = cls.bstack1ll1ll111ll_opy_(response)
            return bstack1ll1l1ll11l_opy_
        except Exception as error:
            logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣᙨ").format(str(error)))
            return None
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def stop(cls, bstack1ll1l1lllll_opy_=None):
        if not bstack11l111l1l_opy_.on() and not bstack1ll111llll_opy_.on():
            return
        if os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᙩ")) == bstack1lll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᙪ") or os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᙫ")) == bstack1lll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᙬ"):
            logger.error(bstack1lll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ᙭"))
            return {
                bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᙮"): bstack1lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᙯ"),
                bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙰ"): bstack1lll1l_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪᙱ")
            }
        try:
            cls.bstack1lll1111lll_opy_.shutdown()
            data = {
                bstack1lll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᙲ"): bstack11l111ll1_opy_()
            }
            if not bstack1ll1l1lllll_opy_ is None:
                data[bstack1lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫᙳ")] = [{
                    bstack1lll1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᙴ"): bstack1lll1l_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧᙵ"),
                    bstack1lll1l_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪᙶ"): bstack1ll1l1lllll_opy_
                }]
            config = {
                bstack1lll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᙷ"): cls.default_headers()
            }
            bstack111l1ll111_opy_ = bstack1lll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭ᙸ").format(os.environ[bstack1lll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦᙹ")])
            bstack1ll1ll11l11_opy_ = cls.request_url(bstack111l1ll111_opy_)
            response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"ࠧࡑࡗࡗࠫᙺ"), bstack1ll1ll11l11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lll1l_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢᙻ"))
        except Exception as error:
            logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽࠾ࠥࠨᙼ") + str(error))
            return {
                bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙽ"): bstack1lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᙾ"),
                bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙿ"): str(error)
            }
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def bstack1ll1ll111ll_opy_(cls, response):
        bstack1ll1l11l11l_opy_ = response.json()
        bstack1ll1l1ll11l_opy_ = {}
        if bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"࠭ࡪࡸࡶࠪ ")) is None:
            os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᚁ")] = bstack1lll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᚂ")
        else:
            os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᚃ")] = bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"ࠪ࡮ࡼࡺࠧᚄ"), bstack1lll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᚅ"))
        os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᚆ")] = bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚇ"), bstack1lll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᚈ"))
        if bstack11l111l1l_opy_.bstack1ll1l1llll1_opy_(cls.bs_config, cls.bstack1l11ll111l_opy_.get(bstack1lll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩᚉ"), bstack1lll1l_opy_ (u"ࠩࠪᚊ"))) is True:
            bstack1ll1l11l1ll_opy_, bstack1ll1l1ll111_opy_, bstack1ll1l11llll_opy_ = cls.bstack1ll1l111l1l_opy_(bstack1ll1l11l11l_opy_)
            if bstack1ll1l11l1ll_opy_ != None and bstack1ll1l1ll111_opy_ != None:
                bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᚋ")] = {
                    bstack1lll1l_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧᚌ"): bstack1ll1l11l1ll_opy_,
                    bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᚍ"): bstack1ll1l1ll111_opy_,
                    bstack1lll1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᚎ"): bstack1ll1l11llll_opy_
                }
            else:
                bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚏ")] = {}
        else:
            bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᚐ")] = {}
        if bstack1ll111llll_opy_.bstack111llll1l1_opy_(cls.bs_config) is True:
            bstack1ll1l1l111l_opy_, bstack1ll1l1ll111_opy_ = cls.bstack1ll1l1l1l11_opy_(bstack1ll1l11l11l_opy_)
            if bstack1ll1l1l111l_opy_ != None and bstack1ll1l1ll111_opy_ != None:
                bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚑ")] = {
                    bstack1lll1l_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧᚒ"): bstack1ll1l1l111l_opy_,
                    bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚓ"): bstack1ll1l1ll111_opy_,
                }
            else:
                bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚔ")] = {}
        else:
            bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚕ")] = {}
        if bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚖ")].get(bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᚗ")) != None or bstack1ll1l1ll11l_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚘ")].get(bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᚙ")) != None:
            cls.bstack1ll1l1l11l1_opy_(bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"ࠫ࡯ࡽࡴࠨᚚ")), bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ᚛")))
        return bstack1ll1l1ll11l_opy_
    @classmethod
    def bstack1ll1l111l1l_opy_(cls, bstack1ll1l11l11l_opy_):
        if bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᚜")) == None:
            cls.bstack1ll1l1lll11_opy_()
            return [None, None, None]
        if bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᚝")][bstack1lll1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ᚞")] != True:
            cls.bstack1ll1l1lll11_opy_(bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᚟")])
            return [None, None, None]
        logger.debug(bstack1lll1l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧᚠ"))
        os.environ[bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᚡ")] = bstack1lll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᚢ")
        if bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"࠭ࡪࡸࡶࠪᚣ")):
            os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᚤ")] = bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠨ࡬ࡺࡸࠬᚥ")]
            os.environ[bstack1lll1l_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ᚦ")] = json.dumps({
                bstack1lll1l_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬᚧ"): bstack11l111lll1_opy_(cls.bs_config),
                bstack1lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ᚨ"): bstack111llllll1_opy_(cls.bs_config)
            })
        if bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᚩ")):
            os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᚪ")] = bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᚫ")]
        if bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᚬ")].get(bstack1lll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᚭ"), {}).get(bstack1lll1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᚮ")):
            os.environ[bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᚯ")] = str(bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚰ")][bstack1lll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚱ")][bstack1lll1l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᚲ")])
        return [bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠨ࡬ࡺࡸࠬᚳ")], bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚴ")], os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᚵ")]]
    @classmethod
    def bstack1ll1l1l1l11_opy_(cls, bstack1ll1l11l11l_opy_):
        if bstack1ll1l11l11l_opy_.get(bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚶ")) == None:
            cls.bstack1ll1l11l111_opy_()
            return [None, None]
        if bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚷ")][bstack1lll1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᚸ")] != True:
            cls.bstack1ll1l11l111_opy_(bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚹ")])
            return [None, None]
        if bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚺ")].get(bstack1lll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᚻ")):
            logger.debug(bstack1lll1l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧᚼ"))
            parsed = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᚽ"), bstack1lll1l_opy_ (u"ࠬࢁࡽࠨᚾ")))
            capabilities = bstack1llllllll1_opy_.bstack1ll1ll111l1_opy_(bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚿ")][bstack1lll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᛀ")][bstack1lll1l_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᛁ")], bstack1lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᛂ"), bstack1lll1l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩᛃ"))
            bstack1ll1l1l111l_opy_ = capabilities[bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᛄ")]
            os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᛅ")] = bstack1ll1l1l111l_opy_
            parsed[bstack1lll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᛆ")] = capabilities[bstack1lll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᛇ")]
            os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᛈ")] = json.dumps(parsed)
            scripts = bstack1llllllll1_opy_.bstack1ll1ll111l1_opy_(bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᛉ")][bstack1lll1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᛊ")][bstack1lll1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᛋ")], bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᛌ"), bstack1lll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧᛍ"))
            bstack1l111111l1_opy_.bstack11l11l11l1_opy_(scripts)
            commands = bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛎ")][bstack1lll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᛏ")][bstack1lll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪᛐ")].get(bstack1lll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᛑ"))
            bstack1l111111l1_opy_.bstack11l111l1l1_opy_(commands)
            bstack1l111111l1_opy_.store()
        return [bstack1ll1l1l111l_opy_, bstack1ll1l11l11l_opy_[bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᛒ")]]
    @classmethod
    def bstack1ll1l1lll11_opy_(cls, response=None):
        os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᛓ")] = bstack1lll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛔ")
        os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᛕ")] = bstack1lll1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᛖ")
        os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᛗ")] = bstack1lll1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛘ")
        os.environ[bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᛙ")] = bstack1lll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᛚ")
        os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᛛ")] = bstack1lll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᛜ")
        os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᛝ")] = bstack1lll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᛞ")
        cls.bstack1ll1ll11111_opy_(response, bstack1lll1l_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥᛟ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l11l111_opy_(cls, response=None):
        os.environ[bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᛠ")] = bstack1lll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᛡ")
        os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᛢ")] = bstack1lll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛣ")
        os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛤ")] = bstack1lll1l_opy_ (u"ࠩࡱࡹࡱࡲࠧᛥ")
        cls.bstack1ll1ll11111_opy_(response, bstack1lll1l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᛦ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1l11l1_opy_(cls, bstack1ll1l11l1l1_opy_, bstack1ll1l1ll111_opy_):
        os.environ[bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᛧ")] = bstack1ll1l11l1l1_opy_
        os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᛨ")] = bstack1ll1l1ll111_opy_
    @classmethod
    def bstack1ll1ll11111_opy_(cls, response=None, product=bstack1lll1l_opy_ (u"ࠨࠢᛩ")):
        if response == None:
            logger.error(product + bstack1lll1l_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤᛪ"))
        for error in response[bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ᛫")]:
            bstack1111ll11l1_opy_ = error[bstack1lll1l_opy_ (u"ࠩ࡮ࡩࡾ࠭᛬")]
            error_message = error[bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᛭")]
            if error_message:
                if bstack1111ll11l1_opy_ == bstack1lll1l_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥᛮ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1lll1l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨᛯ") + product + bstack1lll1l_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᛰ"))
    @classmethod
    def bstack1ll1l1ll1l1_opy_(cls):
        if cls.bstack1lll1111lll_opy_ is not None:
            return
        cls.bstack1lll1111lll_opy_ = bstack1lll111l1ll_opy_(cls.bstack1ll1l11lll1_opy_)
        cls.bstack1lll1111lll_opy_.start()
    @classmethod
    def bstack11l1ll1l11_opy_(cls):
        if cls.bstack1lll1111lll_opy_ is None:
            return
        cls.bstack1lll1111lll_opy_.shutdown()
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def bstack1ll1l11lll1_opy_(cls, bstack11ll111l1l_opy_, bstack1ll1l1l1lll_opy_=bstack1lll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᛱ")):
        config = {
            bstack1lll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᛲ"): cls.default_headers()
        }
        response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᛳ"), cls.request_url(bstack1ll1l1l1lll_opy_), bstack11ll111l1l_opy_, config)
        bstack11l11111ll_opy_ = response.json()
    @classmethod
    def bstack11ll1ll111_opy_(cls, bstack11ll111l1l_opy_, bstack1ll1l1l1lll_opy_=bstack1lll1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᛴ")):
        if not bstack1llllllll1_opy_.bstack1ll1l111ll1_opy_(bstack11ll111l1l_opy_[bstack1lll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᛵ")]):
            return
        bstack1l1ll1lll1_opy_ = bstack1llllllll1_opy_.bstack1ll1l1l1111_opy_(bstack11ll111l1l_opy_[bstack1lll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᛶ")], bstack11ll111l1l_opy_.get(bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᛷ")))
        if bstack1l1ll1lll1_opy_ != None:
            bstack11ll111l1l_opy_[bstack1lll1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᛸ")] = bstack1l1ll1lll1_opy_
        if bstack1ll1l1l1lll_opy_ == bstack1lll1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ᛹"):
            cls.bstack1ll1l1ll1l1_opy_()
            cls.bstack1lll1111lll_opy_.add(bstack11ll111l1l_opy_)
        elif bstack1ll1l1l1lll_opy_ == bstack1lll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ᛺"):
            cls.bstack1ll1l11lll1_opy_([bstack11ll111l1l_opy_], bstack1ll1l1l1lll_opy_)
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def bstack1l11llll_opy_(cls, bstack11l1llll11_opy_):
        bstack1ll1l111lll_opy_ = []
        for log in bstack11l1llll11_opy_:
            bstack1ll1l1l1l1l_opy_ = {
                bstack1lll1l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ᛻"): bstack1lll1l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭᛼"),
                bstack1lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ᛽"): log[bstack1lll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ᛾")],
                bstack1lll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᛿"): log[bstack1lll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᜀ")],
                bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩᜁ"): {},
                bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᜂ"): log[bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᜃ")],
            }
            if bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᜄ") in log:
                bstack1ll1l1l1l1l_opy_[bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜅ")] = log[bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜆ")]
            elif bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜇ") in log:
                bstack1ll1l1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜈ")] = log[bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜉ")]
            bstack1ll1l111lll_opy_.append(bstack1ll1l1l1l1l_opy_)
        cls.bstack11ll1ll111_opy_({
            bstack1lll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜊ"): bstack1lll1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᜋ"),
            bstack1lll1l_opy_ (u"࠭࡬ࡰࡩࡶࠫᜌ"): bstack1ll1l111lll_opy_
        })
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def bstack1ll1l11ll11_opy_(cls, steps):
        bstack1ll1l1l11ll_opy_ = []
        for step in steps:
            bstack1ll1ll1111l_opy_ = {
                bstack1lll1l_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᜍ"): bstack1lll1l_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫᜎ"),
                bstack1lll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᜏ"): step[bstack1lll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᜐ")],
                bstack1lll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᜑ"): step[bstack1lll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᜒ")],
                bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜓ"): step[bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᜔")],
                bstack1lll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰ᜕ࠪ"): step[bstack1lll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ᜖")]
            }
            if bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᜗") in step:
                bstack1ll1ll1111l_opy_[bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᜘")] = step[bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᜙")]
            elif bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᜚") in step:
                bstack1ll1ll1111l_opy_[bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᜛")] = step[bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᜜")]
            bstack1ll1l1l11ll_opy_.append(bstack1ll1ll1111l_opy_)
        cls.bstack11ll1ll111_opy_({
            bstack1lll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜝"): bstack1lll1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ᜞"),
            bstack1lll1l_opy_ (u"ࠫࡱࡵࡧࡴࠩᜟ"): bstack1ll1l1l11ll_opy_
        })
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def bstack1lll11ll1l_opy_(cls, screenshot):
        cls.bstack11ll1ll111_opy_({
            bstack1lll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᜠ"): bstack1lll1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᜡ"),
            bstack1lll1l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᜢ"): [{
                bstack1lll1l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᜣ"): bstack1lll1l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫᜤ"),
                bstack1lll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᜥ"): datetime.datetime.utcnow().isoformat() + bstack1lll1l_opy_ (u"ࠫ࡟࠭ᜦ"),
                bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᜧ"): screenshot[bstack1lll1l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᜨ")],
                bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜩ"): screenshot[bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜪ")]
            }]
        }, bstack1ll1l1l1lll_opy_=bstack1lll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᜫ"))
    @classmethod
    @bstack11ll1l1lll_opy_(class_method=True)
    def bstack111l1l1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll1ll111_opy_({
            bstack1lll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᜬ"): bstack1lll1l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᜭ"),
            bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᜮ"): {
                bstack1lll1l_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᜯ"): cls.current_test_uuid(),
                bstack1lll1l_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨᜰ"): cls.bstack11ll1llll1_opy_(driver)
            }
        })
    @classmethod
    def bstack11lll11lll_opy_(cls, event: str, bstack11ll111l1l_opy_: bstack11ll11l1ll_opy_):
        bstack11ll111111_opy_ = {
            bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜱ"): event,
            bstack11ll111l1l_opy_.bstack11ll1l11l1_opy_(): bstack11ll111l1l_opy_.bstack11ll111l11_opy_(event)
        }
        cls.bstack11ll1ll111_opy_(bstack11ll111111_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᜲ"), None) is None or os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᜳ")] == bstack1lll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᜴")) and (os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᜵"), None) is None or os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᜶")] == bstack1lll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ᜷")):
            return False
        return True
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1111ll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1lll1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ᜸"): bstack1lll1l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ᜹"),
            bstack1lll1l_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭᜺"): bstack1lll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ᜻")
        }
        if os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᜼"), None):
            headers[bstack1lll1l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᜽")] = bstack1lll1l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ᜾").format(os.environ[bstack1lll1l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ᜿")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1lll1l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᝀ").format(bstack1ll1l1ll1ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᝁ"), None)
    @staticmethod
    def bstack11ll1llll1_opy_(driver):
        return {
            bstack1111l11l1l_opy_(): bstack111l1111l1_opy_(driver)
        }
    @staticmethod
    def bstack1ll1l1lll1l_opy_(exception_info, report):
        return [{bstack1lll1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᝂ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11l11ll111_opy_(typename):
        if bstack1lll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᝃ") in typename:
            return bstack1lll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᝄ")
        return bstack1lll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᝅ")