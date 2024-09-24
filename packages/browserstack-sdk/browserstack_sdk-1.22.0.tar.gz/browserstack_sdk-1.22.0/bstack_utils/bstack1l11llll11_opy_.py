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
import logging
import os
import threading
from bstack_utils.helper import bstack1l1lllll1l_opy_
from bstack_utils.constants import bstack111l1lllll_opy_
logger = logging.getLogger(__name__)
class bstack11l111l1l_opy_:
    bstack1lll1111lll_opy_ = None
    @classmethod
    def bstack1l11l1lll_opy_(cls):
        if cls.on():
            logger.info(
                bstack1lll1l_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨគ").format(os.environ[bstack1lll1l_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧឃ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨង"), None) is None or os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩច")] == bstack1lll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢឆ"):
            return False
        return True
    @classmethod
    def bstack1ll1l1111ll_opy_(cls, bs_config, framework=bstack1lll1l_opy_ (u"ࠥࠦជ")):
        if framework == bstack1lll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫឈ"):
            return bstack1l1lllll1l_opy_(bs_config.get(bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩញ")))
        bstack1ll11lll11l_opy_ = framework in bstack111l1lllll_opy_
        return bstack1l1lllll1l_opy_(bs_config.get(bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪដ"), bstack1ll11lll11l_opy_))
    @classmethod
    def bstack1ll11ll1l1l_opy_(cls, framework):
        return framework in bstack111l1lllll_opy_
    @classmethod
    def bstack1ll1l1llll1_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l1111ll_opy_(bs_config, framework) is True and cls.bstack1ll11ll1l1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫឋ"), None)
    @staticmethod
    def bstack11lll11111_opy_():
        if getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬឌ"), None):
            return {
                bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧឍ"): bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࠨណ"),
                bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫត"): getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩថ"), None)
            }
        if getattr(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪទ"), None):
            return {
                bstack1lll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬធ"): bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ន"),
                bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩប"): getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧផ"), None)
            }
        return None
    @staticmethod
    def bstack1ll11lll111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l111l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1ll1l1l_opy_(test, hook_name=None):
        bstack1ll11ll1lll_opy_ = test.parent
        if hook_name in [bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩព"), bstack1lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ភ"), bstack1lll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬម"), bstack1lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩយ")]:
            bstack1ll11ll1lll_opy_ = test
        scope = []
        while bstack1ll11ll1lll_opy_ is not None:
            scope.append(bstack1ll11ll1lll_opy_.name)
            bstack1ll11ll1lll_opy_ = bstack1ll11ll1lll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll11ll1ll1_opy_(hook_type):
        if hook_type == bstack1lll1l_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨរ"):
            return bstack1lll1l_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨល")
        elif hook_type == bstack1lll1l_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢវ"):
            return bstack1lll1l_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦឝ")
    @staticmethod
    def bstack1ll11lll1l1_opy_(bstack1ll1l1lll1_opy_):
        try:
            if not bstack11l111l1l_opy_.on():
                return bstack1ll1l1lll1_opy_
            if os.environ.get(bstack1lll1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥឞ"), None) == bstack1lll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦស"):
                tests = os.environ.get(bstack1lll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦហ"), None)
                if tests is None or tests == bstack1lll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨឡ"):
                    return bstack1ll1l1lll1_opy_
                bstack1ll1l1lll1_opy_ = tests.split(bstack1lll1l_opy_ (u"ࠩ࠯ࠫអ"))
                return bstack1ll1l1lll1_opy_
        except Exception as exc:
            print(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦឣ"), str(exc))
        return bstack1ll1l1lll1_opy_