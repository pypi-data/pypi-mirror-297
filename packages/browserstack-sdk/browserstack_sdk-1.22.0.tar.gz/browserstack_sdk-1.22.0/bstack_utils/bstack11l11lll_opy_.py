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
import threading
import logging
import bstack_utils.bstack1l111lll11_opy_ as bstack1ll111llll_opy_
from bstack_utils.helper import bstack1ll111lll1_opy_
logger = logging.getLogger(__name__)
def bstack111ll1111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l1111l11_opy_(context, *args):
    tags = getattr(args[0], bstack1lll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪ྾"), [])
    bstack111l11lll_opy_ = bstack1ll111llll_opy_.bstack1l1l1lll11_opy_(tags)
    threading.current_thread().isA11yTest = bstack111l11lll_opy_
    try:
      bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1111_opy_(bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ྿")) else context.browser
      if bstack1111l111_opy_ and bstack1111l111_opy_.session_id and bstack111l11lll_opy_ and bstack1ll111lll1_opy_(
              threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿀"), None):
          threading.current_thread().isA11yTest = bstack1ll111llll_opy_.bstack1lllllll11_opy_(bstack1111l111_opy_, bstack111l11lll_opy_)
    except Exception as e:
       logger.debug(bstack1lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ࿁").format(str(e)))
def bstack1111l1111_opy_(bstack1111l111_opy_):
    if bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭࿂"), None) and bstack1ll111lll1_opy_(
      threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ࿃"), None) and not bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧ࿄"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll111llll_opy_.bstack1lll1l1l1l_opy_(bstack1111l111_opy_, name=bstack1lll1l_opy_ (u"ࠧࠨ࿅"), path=bstack1lll1l_opy_ (u"ࠨ࿆ࠢ"))