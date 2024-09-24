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
class bstack111lll1l_opy_:
    def __init__(self, handler):
        self._1ll1llllll1_opy_ = None
        self.handler = handler
        self._1ll1lllll1l_opy_ = self.bstack1ll1lllllll_opy_()
        self.patch()
    def patch(self):
        self._1ll1llllll1_opy_ = self._1ll1lllll1l_opy_.execute
        self._1ll1lllll1l_opy_.execute = self.bstack1ll1lllll11_opy_()
    def bstack1ll1lllll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1lll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦᗫ"), driver_command, None, this, args)
            response = self._1ll1llllll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1lll1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦᗬ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1lllll1l_opy_.execute = self._1ll1llllll1_opy_
    @staticmethod
    def bstack1ll1lllllll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver