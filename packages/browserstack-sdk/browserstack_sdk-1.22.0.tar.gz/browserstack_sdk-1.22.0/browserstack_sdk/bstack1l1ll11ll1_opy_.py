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
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11lll1l11l_opy_ import bstack11lll111ll_opy_, bstack11lll1l111_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11l111l1l_opy_
from bstack_utils.helper import bstack1ll111lll1_opy_, bstack11l111ll1_opy_, Result
from bstack_utils.bstack11lll1l1_opy_ import bstack1111ll111_opy_
from bstack_utils.capture import bstack11lll1l1ll_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l1ll11ll1_opy_:
    def __init__(self):
        self.bstack11lll11ll1_opy_ = bstack11lll1l1ll_opy_(self.bstack11lll1ll11_opy_)
        self.tests = {}
    @staticmethod
    def bstack11lll1ll11_opy_(log):
        if not (log[bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬළ")] and log[bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ෆ")].strip()):
            return
        active = bstack11l111l1l_opy_.bstack11lll11111_opy_()
        log = {
            bstack1lll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ෇"): log[bstack1lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭෈")],
            bstack1lll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ෉"): bstack11l111ll1_opy_(),
            bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧ්ࠪ"): log[bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෋")],
        }
        if active:
            if active[bstack1lll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩ෌")] == bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ෍"):
                log[bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭෎")] = active[bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧා")]
            elif active[bstack1lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ැ")] == bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺࠧෑ"):
                log[bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪි")] = active[bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫී")]
        bstack1111ll111_opy_.bstack1l11llll_opy_([log])
    def start_test(self, name, attrs):
        bstack11llll1lll_opy_ = uuid4().__str__()
        self.tests[bstack11llll1lll_opy_] = {}
        self.bstack11lll11ll1_opy_.start()
        bstack11lll1l11l_opy_ = bstack11lll1l111_opy_(
            name=name,
            uuid=bstack11llll1lll_opy_,
            bstack11llll1111_opy_=bstack11l111ll1_opy_(),
            file_path=attrs.filename,
            result=bstack1lll1l_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨු"),
            framework=bstack1lll1l_opy_ (u"࠭ࡂࡦࡪࡤࡺࡪ࠭෕"),
            scope=[attrs.feature.name],
            meta={},
            tags=attrs.tags
        )
        self.tests[bstack11llll1lll_opy_][bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪූ")] = bstack11lll1l11l_opy_
        threading.current_thread().current_test_uuid = bstack11llll1lll_opy_
        bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ෗"), bstack11lll1l11l_opy_)
    def end_test(self, attrs):
        bstack11lll1llll_opy_ = {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢෘ"): attrs.feature.name,
            bstack1lll1l_opy_ (u"ࠥࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣෙ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11lll1l11l_opy_ = self.tests[current_test_uuid][bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧේ")]
        meta = {
            bstack1lll1l_opy_ (u"ࠧ࡬ࡥࡢࡶࡸࡶࡪࠨෛ"): bstack11lll1llll_opy_,
            bstack1lll1l_opy_ (u"ࠨࡳࡵࡧࡳࡷࠧො"): bstack11lll1l11l_opy_.meta.get(bstack1lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ෝ"), []),
            bstack1lll1l_opy_ (u"ࠣࡵࡦࡩࡳࡧࡲࡪࡱࠥෞ"): {
                bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢෟ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11lll1l11l_opy_.bstack11llll11ll_opy_(meta)
        bstack11llll1ll1_opy_, exception = self._11llll11l1_opy_(attrs)
        bstack11lll1111l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11llll1l1l_opy_=[bstack11llll1ll1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෠")].stop(time=bstack11l111ll1_opy_(), duration=int(attrs.duration)*1000, result=bstack11lll1111l_opy_)
        bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭෡"), self.tests[threading.current_thread().current_test_uuid][bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ෢")])
    def bstack1ll11lll11_opy_(self, attrs):
        bstack11lll11l1l_opy_ = {
            bstack1lll1l_opy_ (u"࠭ࡩࡥࠩ෣"): uuid4().__str__(),
            bstack1lll1l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ෤"): attrs.keyword,
            bstack1lll1l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ෥"): [],
            bstack1lll1l_opy_ (u"ࠩࡷࡩࡽࡺࠧ෦"): attrs.name,
            bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ෧"): bstack11l111ll1_opy_(),
            bstack1lll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ෨"): bstack1lll1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭෩"),
            bstack1lll1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ෪"): bstack1lll1l_opy_ (u"ࠧࠨ෫")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ෬")].add_step(bstack11lll11l1l_opy_)
        threading.current_thread().current_step_uuid = bstack11lll11l1l_opy_[bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬ෭")]
    def bstack1ll1llll_opy_(self, attrs):
        current_test_id = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ෮"), None)
        current_step_uuid = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨ෯"), None)
        bstack11llll1ll1_opy_, exception = self._11llll11l1_opy_(attrs)
        bstack11lll1111l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11llll1l1l_opy_=[bstack11llll1ll1_opy_])
        self.tests[current_test_id][bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ෰")].bstack11lll111l1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11lll1111l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1lll11l1_opy_(self, name, attrs):
        bstack11lll1l1l1_opy_ = uuid4().__str__()
        self.tests[bstack11lll1l1l1_opy_] = {}
        self.bstack11lll11ll1_opy_.start()
        scopes = []
        if name in [bstack1lll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ෱"), bstack1lll1l_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠥෲ")]:
            file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
            scopes = [attrs.config.environment_file]
        elif name in [bstack1lll1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤෳ"), bstack1lll1l_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠤ෴")]:
            file_path = attrs.filename
            scopes = [attrs.name]
        else:
            file_path = attrs.filename
            scopes = [attrs.feature.name]
        hook_data = bstack11lll111ll_opy_(
            name=name,
            uuid=bstack11lll1l1l1_opy_,
            bstack11llll1111_opy_=bstack11l111ll1_opy_(),
            file_path=file_path,
            framework=bstack1lll1l_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ෵"),
            scope=scopes,
            result=bstack1lll1l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ෶"),
            hook_type=bstack11lll1lll1_opy_[name]
        )
        self.tests[bstack11lll1l1l1_opy_][bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ෷")] = hook_data
        current_test_id = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ෸"), None)
        if current_test_id:
            hook_data.bstack11lll11l11_opy_(current_test_id)
        if name == bstack1lll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ෹"):
            threading.current_thread().before_all_hook_uuid = bstack11lll1l1l1_opy_
        threading.current_thread().current_hook_uuid = bstack11lll1l1l1_opy_
        bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ෺"), hook_data)
    def bstack111l11111_opy_(self, attrs):
        bstack11llll111l_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭෻"), None)
        hook_data = self.tests[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෼")]
        status = bstack1lll1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ෽")
        exception = None
        bstack11llll1ll1_opy_ = None
        if hook_data.name == bstack1lll1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ෾"):
            self.bstack11lll11ll1_opy_.reset()
            bstack11llll1l11_opy_ = self.tests[bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭෿"), None)][bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ฀")].result.result
            if bstack11llll1l11_opy_ == bstack1lll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣก"):
                if attrs.hook_failures == 1:
                    status = bstack1lll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤข")
                elif attrs.hook_failures == 2:
                    status = bstack1lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥฃ")
            elif attrs.bstack11lll1ll1l_opy_:
                status = bstack1lll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦค")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1lll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩฅ") and attrs.hook_failures == 1:
                status = bstack1lll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨฆ")
            elif hasattr(attrs, bstack1lll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧง")) and attrs.error_message:
                status = bstack1lll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣจ")
            bstack11llll1ll1_opy_, exception = self._11llll11l1_opy_(attrs)
        bstack11lll1111l_opy_ = Result(result=status, exception=exception, bstack11llll1l1l_opy_=[bstack11llll1ll1_opy_])
        hook_data.stop(time=bstack11l111ll1_opy_(), duration=0, result=bstack11lll1111l_opy_)
        bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫฉ"), self.tests[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ช")])
        threading.current_thread().current_hook_uuid = None
    def _11llll11l1_opy_(self, attrs):
        try:
            import traceback
            bstack1l11ll1l1l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11llll1ll1_opy_ = bstack1l11ll1l1l_opy_[-1] if bstack1l11ll1l1l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣซ"))
            bstack11llll1ll1_opy_ = None
            exception = None
        return bstack11llll1ll1_opy_, exception