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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11ll11111l_opy_ import RobotHandler
from bstack_utils.capture import bstack11lll1l1ll_opy_
from bstack_utils.bstack11lll1l11l_opy_ import bstack11ll11l1ll_opy_, bstack11lll111ll_opy_, bstack11lll1l111_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11l111l1l_opy_
from bstack_utils.bstack11lll1l1_opy_ import bstack1111ll111_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll111lll1_opy_, bstack11l111ll1_opy_, Result, \
    bstack11ll1l1lll_opy_, bstack11ll1ll1ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩฌ"): [],
        bstack1lll1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬญ"): [],
        bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫฎ"): []
    }
    bstack11ll11l1l1_opy_ = []
    bstack11l1lll1l1_opy_ = []
    @staticmethod
    def bstack11lll1ll11_opy_(log):
        if not (log[bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩฏ")] and log[bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪฐ")].strip()):
            return
        active = bstack11l111l1l_opy_.bstack11lll11111_opy_()
        log = {
            bstack1lll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩฑ"): log[bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪฒ")],
            bstack1lll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨณ"): bstack11ll1ll1ll_opy_().isoformat() + bstack1lll1l_opy_ (u"࡚࠭ࠨด"),
            bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨต"): log[bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩถ")],
        }
        if active:
            if active[bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧท")] == bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨธ"):
                log[bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫน")] = active[bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬบ")]
            elif active[bstack1lll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫป")] == bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬผ"):
                log[bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨฝ")] = active[bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩพ")]
        bstack1111ll111_opy_.bstack1l11llll_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11ll11llll_opy_ = None
        self._11ll1lll11_opy_ = None
        self._11ll1111ll_opy_ = OrderedDict()
        self.bstack11lll11ll1_opy_ = bstack11lll1l1ll_opy_(self.bstack11lll1ll11_opy_)
    @bstack11ll1l1lll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11ll1l11ll_opy_()
        if not self._11ll1111ll_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭ฟ")), None):
            self._11ll1111ll_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧภ"))] = {}
        bstack11l1l1lll1_opy_ = bstack11lll1l111_opy_(
                bstack11l1ll11ll_opy_=attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨม")),
                name=name,
                bstack11llll1111_opy_=bstack11l111ll1_opy_(),
                file_path=os.path.relpath(attrs[bstack1lll1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ย")], start=os.getcwd()) if attrs.get(bstack1lll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧร")) != bstack1lll1l_opy_ (u"ࠨࠩฤ") else bstack1lll1l_opy_ (u"ࠩࠪล"),
                framework=bstack1lll1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩฦ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧว"), None)
        self._11ll1111ll_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨศ"))][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩษ")] = bstack11l1l1lll1_opy_
    @bstack11ll1l1lll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11ll11ll1l_opy_()
        self._11ll1ll1l1_opy_(messages)
        for bstack11l1llllll_opy_ in self.bstack11ll11l1l1_opy_:
            bstack11l1llllll_opy_[bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩส")][bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧห")].extend(self.store[bstack1lll1l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨฬ")])
            bstack1111ll111_opy_.bstack11ll1ll111_opy_(bstack11l1llllll_opy_)
        self.bstack11ll11l1l1_opy_ = []
        self.store[bstack1lll1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩอ")] = []
    @bstack11ll1l1lll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11lll11ll1_opy_.start()
        if not self._11ll1111ll_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧฮ")), None):
            self._11ll1111ll_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨฯ"))] = {}
        driver = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬะ"), None)
        bstack11lll1l11l_opy_ = bstack11lll1l111_opy_(
            bstack11l1ll11ll_opy_=attrs.get(bstack1lll1l_opy_ (u"ࠧࡪࡦࠪั")),
            name=name,
            bstack11llll1111_opy_=bstack11l111ll1_opy_(),
            file_path=os.path.relpath(attrs[bstack1lll1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨา")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1ll1l1l_opy_(attrs.get(bstack1lll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩำ"), None)),
            framework=bstack1lll1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩิ"),
            tags=attrs[bstack1lll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩี")],
            hooks=self.store[bstack1lll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫึ")],
            bstack11ll1l1111_opy_=bstack1111ll111_opy_.bstack11ll1llll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1lll1l_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣื").format(bstack1lll1l_opy_ (u"ࠢࠡࠤุ").join(attrs[bstack1lll1l_opy_ (u"ࠨࡶࡤ࡫ࡸู࠭")]), name) if attrs[bstack1lll1l_opy_ (u"ࠩࡷࡥ࡬ࡹฺࠧ")] else name
        )
        self._11ll1111ll_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭฻"))][bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ฼")] = bstack11lll1l11l_opy_
        threading.current_thread().current_test_uuid = bstack11lll1l11l_opy_.bstack11ll1ll11l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨ฽"), None)
        self.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ฾"), bstack11lll1l11l_opy_)
    @bstack11ll1l1lll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11lll11ll1_opy_.reset()
        bstack11ll1111l1_opy_ = bstack11ll11ll11_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ฿")), bstack1lll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩเ"))
        self._11ll1111ll_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬแ"))][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭โ")].stop(time=bstack11l111ll1_opy_(), duration=int(attrs.get(bstack1lll1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩใ"), bstack1lll1l_opy_ (u"ࠬ࠶ࠧไ"))), result=Result(result=bstack11ll1111l1_opy_, exception=attrs.get(bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧๅ")), bstack11llll1l1l_opy_=[attrs.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨๆ"))]))
        self.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ็"), self._11ll1111ll_opy_[attrs.get(bstack1lll1l_opy_ (u"ࠩ࡬ࡨ่ࠬ"))][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ้࠭")], True)
        self.store[bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ๊")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11ll1l1lll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11ll1l11ll_opy_()
        current_test_id = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪ๋ࠧ"), None)
        bstack11ll111lll_opy_ = current_test_id if bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ์"), None) else bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪํ"), None)
        if attrs.get(bstack1lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭๎"), bstack1lll1l_opy_ (u"ࠩࠪ๏")).lower() in [bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ๐"), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭๑")]:
            hook_type = bstack11ll1l1l1l_opy_(attrs.get(bstack1lll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ๒")), bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ๓"), None))
            hook_name = bstack1lll1l_opy_ (u"ࠧࡼࡿࠪ๔").format(attrs.get(bstack1lll1l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ๕"), bstack1lll1l_opy_ (u"ࠩࠪ๖")))
            if hook_type in [bstack1lll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ๗"), bstack1lll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ๘")]:
                hook_name = bstack1lll1l_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭๙").format(bstack11l1ll1ll1_opy_.get(hook_type), attrs.get(bstack1lll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭๚"), bstack1lll1l_opy_ (u"ࠧࠨ๛")))
            bstack11l1ll11l1_opy_ = bstack11lll111ll_opy_(
                bstack11l1ll11ll_opy_=bstack11ll111lll_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࠪ๜") + attrs.get(bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๝"), bstack1lll1l_opy_ (u"ࠪࠫ๞")).lower(),
                name=hook_name,
                bstack11llll1111_opy_=bstack11l111ll1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1lll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ๟")), start=os.getcwd()),
                framework=bstack1lll1l_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ๠"),
                tags=attrs[bstack1lll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫ๡")],
                scope=RobotHandler.bstack11l1ll1l1l_opy_(attrs.get(bstack1lll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ๢"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11l1ll11l1_opy_.bstack11ll1ll11l_opy_()
            threading.current_thread().current_hook_id = bstack11ll111lll_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࠪ๣") + attrs.get(bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๤"), bstack1lll1l_opy_ (u"ࠪࠫ๥")).lower()
            self.store[bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ๦")] = [bstack11l1ll11l1_opy_.bstack11ll1ll11l_opy_()]
            if bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ๧"), None):
                self.store[bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ๨")].append(bstack11l1ll11l1_opy_.bstack11ll1ll11l_opy_())
            else:
                self.store[bstack1lll1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭๩")].append(bstack11l1ll11l1_opy_.bstack11ll1ll11l_opy_())
            if bstack11ll111lll_opy_:
                self._11ll1111ll_opy_[bstack11ll111lll_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࠪ๪") + attrs.get(bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๫"), bstack1lll1l_opy_ (u"ࠪࠫ๬")).lower()] = { bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๭"): bstack11l1ll11l1_opy_ }
            bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭๮"), bstack11l1ll11l1_opy_)
        else:
            bstack11lll11l1l_opy_ = {
                bstack1lll1l_opy_ (u"࠭ࡩࡥࠩ๯"): uuid4().__str__(),
                bstack1lll1l_opy_ (u"ࠧࡵࡧࡻࡸࠬ๰"): bstack1lll1l_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧ๱").format(attrs.get(bstack1lll1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ๲")), attrs.get(bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ๳"), bstack1lll1l_opy_ (u"ࠫࠬ๴"))) if attrs.get(bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ๵"), []) else attrs.get(bstack1lll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭๶")),
                bstack1lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧ๷"): attrs.get(bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭๸"), []),
                bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭๹"): bstack11l111ll1_opy_(),
                bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ๺"): bstack1lll1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ๻"),
                bstack1lll1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ๼"): attrs.get(bstack1lll1l_opy_ (u"࠭ࡤࡰࡥࠪ๽"), bstack1lll1l_opy_ (u"ࠧࠨ๾"))
            }
            if attrs.get(bstack1lll1l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ๿"), bstack1lll1l_opy_ (u"ࠩࠪ຀")) != bstack1lll1l_opy_ (u"ࠪࠫກ"):
                bstack11lll11l1l_opy_[bstack1lll1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬຂ")] = attrs.get(bstack1lll1l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭຃"))
            if not self.bstack11l1lll1l1_opy_:
                self._11ll1111ll_opy_[self._11ll11l11l_opy_()][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩຄ")].add_step(bstack11lll11l1l_opy_)
                threading.current_thread().current_step_uuid = bstack11lll11l1l_opy_[bstack1lll1l_opy_ (u"ࠧࡪࡦࠪ຅")]
            self.bstack11l1lll1l1_opy_.append(bstack11lll11l1l_opy_)
    @bstack11ll1l1lll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11ll11ll1l_opy_()
        self._11ll1ll1l1_opy_(messages)
        current_test_id = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪຆ"), None)
        bstack11ll111lll_opy_ = current_test_id if current_test_id else bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬງ"), None)
        bstack11l1l1llll_opy_ = bstack11ll11ll11_opy_.get(attrs.get(bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪຈ")), bstack1lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬຉ"))
        bstack11l1lll111_opy_ = attrs.get(bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຊ"))
        if bstack11l1l1llll_opy_ != bstack1lll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ຋") and not attrs.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຌ")) and self._11ll11llll_opy_:
            bstack11l1lll111_opy_ = self._11ll11llll_opy_
        bstack11lll1111l_opy_ = Result(result=bstack11l1l1llll_opy_, exception=bstack11l1lll111_opy_, bstack11llll1l1l_opy_=[bstack11l1lll111_opy_])
        if attrs.get(bstack1lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ຍ"), bstack1lll1l_opy_ (u"ࠩࠪຎ")).lower() in [bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩຏ"), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ຐ")]:
            bstack11ll111lll_opy_ = current_test_id if current_test_id else bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨຑ"), None)
            if bstack11ll111lll_opy_:
                bstack11llll111l_opy_ = bstack11ll111lll_opy_ + bstack1lll1l_opy_ (u"ࠨ࠭ࠣຒ") + attrs.get(bstack1lll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬຓ"), bstack1lll1l_opy_ (u"ࠨࠩດ")).lower()
                self._11ll1111ll_opy_[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຕ")].stop(time=bstack11l111ll1_opy_(), duration=int(attrs.get(bstack1lll1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨຖ"), bstack1lll1l_opy_ (u"ࠫ࠵࠭ທ"))), result=bstack11lll1111l_opy_)
                bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧຘ"), self._11ll1111ll_opy_[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩນ")])
        else:
            bstack11ll111lll_opy_ = current_test_id if current_test_id else bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩບ"), None)
            if bstack11ll111lll_opy_ and len(self.bstack11l1lll1l1_opy_) == 1:
                current_step_uuid = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬປ"), None)
                self._11ll1111ll_opy_[bstack11ll111lll_opy_][bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຜ")].bstack11lll111l1_opy_(current_step_uuid, duration=int(attrs.get(bstack1lll1l_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨຝ"), bstack1lll1l_opy_ (u"ࠫ࠵࠭ພ"))), result=bstack11lll1111l_opy_)
            else:
                self.bstack11l1lllll1_opy_(attrs)
            self.bstack11l1lll1l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1lll1l_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪຟ"), bstack1lll1l_opy_ (u"࠭࡮ࡰࠩຠ")) == bstack1lll1l_opy_ (u"ࠧࡺࡧࡶࠫມ"):
                return
            self.messages.push(message)
            bstack11l1llll11_opy_ = []
            if bstack11l111l1l_opy_.bstack11lll11111_opy_():
                bstack11l1llll11_opy_.append({
                    bstack1lll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫຢ"): bstack11l111ll1_opy_(),
                    bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪຣ"): message.get(bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ຤")),
                    bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪລ"): message.get(bstack1lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ຦")),
                    **bstack11l111l1l_opy_.bstack11lll11111_opy_()
                })
                if len(bstack11l1llll11_opy_) > 0:
                    bstack1111ll111_opy_.bstack1l11llll_opy_(bstack11l1llll11_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1111ll111_opy_.bstack11l1ll1l11_opy_()
    def bstack11l1lllll1_opy_(self, bstack11l1l1ll1l_opy_):
        if not bstack11l111l1l_opy_.bstack11lll11111_opy_():
            return
        kwname = bstack1lll1l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬວ").format(bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧຨ")), bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ຩ"), bstack1lll1l_opy_ (u"ࠩࠪສ"))) if bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨຫ"), []) else bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫຬ"))
        error_message = bstack1lll1l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦອ").format(kwname, bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ຮ")), str(bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຯ"))))
        bstack11l1ll1lll_opy_ = bstack1lll1l_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢະ").format(kwname, bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩັ")))
        bstack11ll11l111_opy_ = error_message if bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫາ")) else bstack11l1ll1lll_opy_
        bstack11l1llll1l_opy_ = {
            bstack1lll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧຳ"): self.bstack11l1lll1l1_opy_[-1].get(bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩິ"), bstack11l111ll1_opy_()),
            bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧີ"): bstack11ll11l111_opy_,
            bstack1lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຶ"): bstack1lll1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧື") if bstack11l1l1ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴຸࠩ")) == bstack1lll1l_opy_ (u"ࠪࡊࡆࡏࡌࠨູ") else bstack1lll1l_opy_ (u"ࠫࡎࡔࡆࡐ຺ࠩ"),
            **bstack11l111l1l_opy_.bstack11lll11111_opy_()
        }
        bstack1111ll111_opy_.bstack1l11llll_opy_([bstack11l1llll1l_opy_])
    def _11ll11l11l_opy_(self):
        for bstack11l1ll11ll_opy_ in reversed(self._11ll1111ll_opy_):
            bstack11l1lll11l_opy_ = bstack11l1ll11ll_opy_
            data = self._11ll1111ll_opy_[bstack11l1ll11ll_opy_][bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨົ")]
            if isinstance(data, bstack11lll111ll_opy_):
                if not bstack1lll1l_opy_ (u"࠭ࡅࡂࡅࡋࠫຼ") in data.bstack11ll1l111l_opy_():
                    return bstack11l1lll11l_opy_
            else:
                return bstack11l1lll11l_opy_
    def _11ll1ll1l1_opy_(self, messages):
        try:
            bstack11ll1lll1l_opy_ = BuiltIn().get_variable_value(bstack1lll1l_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨຽ")) in (bstack11ll1l1ll1_opy_.DEBUG, bstack11ll1l1ll1_opy_.TRACE)
            for message, bstack11ll111ll1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ຾"))
                level = message.get(bstack1lll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ຿"))
                if level == bstack11ll1l1ll1_opy_.FAIL:
                    self._11ll11llll_opy_ = name or self._11ll11llll_opy_
                    self._11ll1lll11_opy_ = bstack11ll111ll1_opy_.get(bstack1lll1l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦເ")) if bstack11ll1lll1l_opy_ and bstack11ll111ll1_opy_ else self._11ll1lll11_opy_
        except:
            pass
    @classmethod
    def bstack11lll11lll_opy_(self, event: str, bstack11ll111l1l_opy_: bstack11ll11l1ll_opy_, bstack11l1ll111l_opy_=False):
        if event == bstack1lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ແ"):
            bstack11ll111l1l_opy_.set(hooks=self.store[bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩໂ")])
        if event == bstack1lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧໃ"):
            event = bstack1lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩໄ")
        if bstack11l1ll111l_opy_:
            bstack11ll111111_opy_ = {
                bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ໅"): event,
                bstack11ll111l1l_opy_.bstack11ll1l11l1_opy_(): bstack11ll111l1l_opy_.bstack11ll111l11_opy_(event)
            }
            self.bstack11ll11l1l1_opy_.append(bstack11ll111111_opy_)
        else:
            bstack1111ll111_opy_.bstack11lll11lll_opy_(event, bstack11ll111l1l_opy_)
class Messages:
    def __init__(self):
        self._11ll11lll1_opy_ = []
    def bstack11ll1l11ll_opy_(self):
        self._11ll11lll1_opy_.append([])
    def bstack11ll11ll1l_opy_(self):
        return self._11ll11lll1_opy_.pop() if self._11ll11lll1_opy_ else list()
    def push(self, message):
        self._11ll11lll1_opy_[-1].append(message) if self._11ll11lll1_opy_ else self._11ll11lll1_opy_.append([message])
class bstack11ll1l1ll1_opy_:
    FAIL = bstack1lll1l_opy_ (u"ࠩࡉࡅࡎࡒࠧໆ")
    ERROR = bstack1lll1l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩ໇")
    WARNING = bstack1lll1l_opy_ (u"ࠫ࡜ࡇࡒࡏ່ࠩ")
    bstack11ll1lllll_opy_ = bstack1lll1l_opy_ (u"ࠬࡏࡎࡇࡑ້ࠪ")
    DEBUG = bstack1lll1l_opy_ (u"࠭ࡄࡆࡄࡘࡋ໊ࠬ")
    TRACE = bstack1lll1l_opy_ (u"ࠧࡕࡔࡄࡇࡊ໋࠭")
    bstack11l1ll1111_opy_ = [FAIL, ERROR]
def bstack11l1lll1ll_opy_(bstack11ll1l1l11_opy_):
    if not bstack11ll1l1l11_opy_:
        return None
    if bstack11ll1l1l11_opy_.get(bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໌"), None):
        return getattr(bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬໍ")], bstack1lll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ໎"), None)
    return bstack11ll1l1l11_opy_.get(bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ໏"), None)
def bstack11ll1l1l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ໐"), bstack1lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ໑")]:
        return
    if hook_type.lower() == bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭໒"):
        if current_test_uuid is None:
            return bstack1lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ໓")
        else:
            return bstack1lll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ໔")
    elif hook_type.lower() == bstack1lll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ໕"):
        if current_test_uuid is None:
            return bstack1lll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ໖")
        else:
            return bstack1lll1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ໗")