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
import sys
class bstack11lll1l1ll_opy_:
    def __init__(self, handler):
        self._111ll1llll_opy_ = sys.stdout.write
        self._111ll1lll1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack111lll1111_opy_
        sys.stdout.error = self.bstack111lll111l_opy_
    def bstack111lll1111_opy_(self, _str):
        self._111ll1llll_opy_(_str)
        if self.handler:
            self.handler({bstack1lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭࿇"): bstack1lll1l_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿈"), bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿉"): _str})
    def bstack111lll111l_opy_(self, _str):
        self._111ll1lll1_opy_(_str)
        if self.handler:
            self.handler({bstack1lll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿊"): bstack1lll1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ࿋"), bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿌"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._111ll1llll_opy_
        sys.stderr.write = self._111ll1lll1_opy_