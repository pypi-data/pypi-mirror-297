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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1l111lll11_opy_ as bstack1ll111llll_opy_
from browserstack_sdk.bstack1ll1lll11l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11l1111_opy_
class bstack1111l11l_opy_:
    def __init__(self, args, logger, bstack11l1l1l1l1_opy_, bstack11l1l111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1l1l1l1_opy_ = bstack11l1l1l1l1_opy_
        self.bstack11l1l111ll_opy_ = bstack11l1l111ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1l1lll1_opy_ = []
        self.bstack11l1l11111_opy_ = None
        self.bstack1l1l1l1lll_opy_ = []
        self.bstack11l1l1ll11_opy_ = self.bstack11111llll_opy_()
        self.bstack11l1ll11l_opy_ = -1
    def bstack1l1lll1l1_opy_(self, bstack11l1l1l11l_opy_):
        self.parse_args()
        self.bstack11l1l1l1ll_opy_()
        self.bstack11l11lll11_opy_(bstack11l1l1l11l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l1l11lll_opy_():
        import importlib
        if getattr(importlib, bstack1lll1l_opy_ (u"࠭ࡦࡪࡰࡧࡣࡱࡵࡡࡥࡧࡵࠫ໘"), False):
            bstack11l1l11l11_opy_ = importlib.find_loader(bstack1lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ໙"))
        else:
            bstack11l1l11l11_opy_ = importlib.util.find_spec(bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ໚"))
    def bstack11l1l11l1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l1ll11l_opy_ = -1
        if self.bstack11l1l111ll_opy_ and bstack1lll1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໛") in self.bstack11l1l1l1l1_opy_:
            self.bstack11l1ll11l_opy_ = int(self.bstack11l1l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪໜ")])
        try:
            bstack11l11lllll_opy_ = [bstack1lll1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ໝ"), bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨໞ"), bstack1lll1l_opy_ (u"࠭࠭ࡱࠩໟ")]
            if self.bstack11l1ll11l_opy_ >= 0:
                bstack11l11lllll_opy_.extend([bstack1lll1l_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ໠"), bstack1lll1l_opy_ (u"ࠨ࠯ࡱࠫ໡")])
            for arg in bstack11l11lllll_opy_:
                self.bstack11l1l11l1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l1l1l1ll_opy_(self):
        bstack11l1l11111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
        return bstack11l1l11111_opy_
    def bstack11111ll1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l1l11lll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11l1111_opy_)
    def bstack11l11lll11_opy_(self, bstack11l1l1l11l_opy_):
        bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
        if bstack11l1l1l11l_opy_:
            self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭໢"))
            self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"ࠪࡘࡷࡻࡥࠨ໣"))
        if bstack1l1l111l_opy_.bstack11l1l111l1_opy_():
            self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ໤"))
            self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"࡚ࠬࡲࡶࡧࠪ໥"))
        self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"࠭࠭ࡱࠩ໦"))
        self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬ໧"))
        self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ໨"))
        self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ໩"))
        if self.bstack11l1ll11l_opy_ > 1:
            self.bstack11l1l11111_opy_.append(bstack1lll1l_opy_ (u"ࠪ࠱ࡳ࠭໪"))
            self.bstack11l1l11111_opy_.append(str(self.bstack11l1ll11l_opy_))
    def bstack11l1l1l111_opy_(self):
        bstack1l1l1l1lll_opy_ = []
        for spec in self.bstack1ll1l1lll1_opy_:
            bstack1111llll_opy_ = [spec]
            bstack1111llll_opy_ += self.bstack11l1l11111_opy_
            bstack1l1l1l1lll_opy_.append(bstack1111llll_opy_)
        self.bstack1l1l1l1lll_opy_ = bstack1l1l1l1lll_opy_
        return bstack1l1l1l1lll_opy_
    def bstack11111llll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11l1l1ll11_opy_ = True
            return True
        except Exception as e:
            self.bstack11l1l1ll11_opy_ = False
        return self.bstack11l1l1ll11_opy_
    def bstack1l1llll1ll_opy_(self, bstack11l1l11ll1_opy_, bstack1l1lll1l1_opy_):
        bstack1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ໫")] = self.bstack11l1l1l1l1_opy_
        multiprocessing.set_start_method(bstack1lll1l_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫ໬"))
        bstack11111l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1ll11111_opy_ = manager.list()
        if bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ໭") in self.bstack11l1l1l1l1_opy_:
            for index, platform in enumerate(self.bstack11l1l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ໮")]):
                bstack11111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l1l11ll1_opy_,
                                                            args=(self.bstack11l1l11111_opy_, bstack1l1lll1l1_opy_, bstack1l1ll11111_opy_)))
            bstack11l1l1111l_opy_ = len(self.bstack11l1l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ໯")])
        else:
            bstack11111l11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l1l11ll1_opy_,
                                                        args=(self.bstack11l1l11111_opy_, bstack1l1lll1l1_opy_, bstack1l1ll11111_opy_)))
            bstack11l1l1111l_opy_ = 1
        i = 0
        for t in bstack11111l11_opy_:
            os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ໰")] = str(i)
            if bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭໱") in self.bstack11l1l1l1l1_opy_:
                os.environ[bstack1lll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ໲")] = json.dumps(self.bstack11l1l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ໳")][i % bstack11l1l1111l_opy_])
            i += 1
            t.start()
        for t in bstack11111l11_opy_:
            t.join()
        return list(bstack1l1ll11111_opy_)
    @staticmethod
    def bstack1lllllll1l_opy_(driver, bstack11l11lll1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ໴"), None)
        if item and getattr(item, bstack1lll1l_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩ໵"), None) and not getattr(item, bstack1lll1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪ໶"), False):
            logger.info(
                bstack1lll1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣ໷"))
            bstack11l11llll1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll111llll_opy_.bstack1lll1l1l1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)