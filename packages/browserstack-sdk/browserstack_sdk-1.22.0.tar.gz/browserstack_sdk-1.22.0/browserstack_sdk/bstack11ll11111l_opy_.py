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
class RobotHandler():
    def __init__(self, args, logger, bstack11l1l1l1l1_opy_, bstack11l1l111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1l1l1l1_opy_ = bstack11l1l1l1l1_opy_
        self.bstack11l1l111ll_opy_ = bstack11l1l111ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1ll1l1l_opy_(bstack11l11ll11l_opy_):
        bstack11l11ll1ll_opy_ = []
        if bstack11l11ll11l_opy_:
            tokens = str(os.path.basename(bstack11l11ll11l_opy_)).split(bstack1lll1l_opy_ (u"ࠥࡣࠧ໸"))
            camelcase_name = bstack1lll1l_opy_ (u"ࠦࠥࠨ໹").join(t.title() for t in tokens)
            suite_name, bstack11l11ll1l1_opy_ = os.path.splitext(camelcase_name)
            bstack11l11ll1ll_opy_.append(suite_name)
        return bstack11l11ll1ll_opy_
    @staticmethod
    def bstack11l11ll111_opy_(typename):
        if bstack1lll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ໺") in typename:
            return bstack1lll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ໻")
        return bstack1lll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ໼")