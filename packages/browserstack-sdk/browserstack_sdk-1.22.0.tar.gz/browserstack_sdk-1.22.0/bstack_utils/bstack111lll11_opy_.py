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
from browserstack_sdk.bstack1ll1llll11_opy_ import bstack1111l11l_opy_
from browserstack_sdk.bstack11ll11111l_opy_ import RobotHandler
def bstack11ll1ll1_opy_(framework):
    if framework.lower() == bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫኸ"):
        return bstack1111l11l_opy_.version()
    elif framework.lower() == bstack1lll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫኹ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1lll1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ኺ"):
        import behave
        return behave.__version__
    else:
        return bstack1lll1l_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨኻ")