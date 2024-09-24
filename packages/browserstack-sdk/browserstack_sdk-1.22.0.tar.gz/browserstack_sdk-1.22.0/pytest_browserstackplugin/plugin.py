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
import atexit
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11lllll_opy_, bstack1l1ll1ll_opy_, update, bstack1ll1l1ll1l_opy_,
                                       bstack1lll11l1ll_opy_, bstack1l1ll111l1_opy_, bstack11ll11111_opy_, bstack1l11l11l1l_opy_,
                                       bstack1ll1111l1l_opy_, bstack111ll11l1_opy_, bstack11111l1ll_opy_, bstack1lllll1ll1_opy_,
                                       bstack1l111111ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11llll1_opy_)
from browserstack_sdk.bstack1ll1llll11_opy_ import bstack1111l11l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1lll111l1_opy_
from bstack_utils.capture import bstack11lll1l1ll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1l1llll1_opy_, bstack11llllllll_opy_, bstack1llllll111_opy_, \
    bstack1l111llll_opy_
from bstack_utils.helper import bstack1ll111lll1_opy_, bstack111l1111ll_opy_, bstack11ll1ll1ll_opy_, bstack11lllll1l_opy_, bstack11111l1l1l_opy_, bstack11l111ll1_opy_, \
    bstack11111lllll_opy_, \
    bstack1111llll1l_opy_, bstack1111l1l1l_opy_, bstack1ll11l1l1_opy_, bstack1111lll11l_opy_, bstack11ll1111_opy_, Notset, \
    bstack1lll1lll1_opy_, bstack1111l1l1l1_opy_, bstack1111l1ll11_opy_, Result, bstack111l11ll11_opy_, bstack11111lll1l_opy_, bstack11ll1l1lll_opy_, \
    bstack1l1l1ll11_opy_, bstack1lll1l1ll_opy_, bstack1l1lllll1l_opy_, bstack111111l1l1_opy_
from bstack_utils.bstack11111111l1_opy_ import bstack1111111111_opy_
from bstack_utils.messages import bstack1l1l11lll_opy_, bstack1lllll1l1_opy_, bstack1llll1l11l_opy_, bstack11l111lll_opy_, bstack1l11l1111_opy_, \
    bstack111llll1_opy_, bstack1ll11ll1l1_opy_, bstack111l11ll_opy_, bstack1ll111ll_opy_, bstack1l1l1lll_opy_, \
    bstack111l1l11_opy_, bstack11lll1l11_opy_
from bstack_utils.proxy import bstack1l1l1lll1_opy_, bstack1llll111ll_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack1lll11l11l1_opy_, bstack1lll111llll_opy_, bstack1lll11l1ll1_opy_, bstack1lll11ll111_opy_, \
    bstack1lll11l1l11_opy_, bstack1lll11l1l1l_opy_, bstack1lll11ll11l_opy_, bstack1l1l11l1ll_opy_, bstack1lll11l111l_opy_
from bstack_utils.bstack1l1111ll_opy_ import bstack111lll1l_opy_
from bstack_utils.bstack1ll1l11111_opy_ import bstack11l1l1l11_opy_, bstack11111ll11_opy_, bstack1l11lll1l_opy_, \
    bstack1l1111l111_opy_, bstack1ll1l11ll1_opy_
from bstack_utils.bstack11lll1l11l_opy_ import bstack11lll1l111_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11l111l1l_opy_
import bstack_utils.bstack1l111lll11_opy_ as bstack1ll111llll_opy_
from bstack_utils.bstack11lll1l1_opy_ import bstack1111ll111_opy_
from bstack_utils.bstack1l111111l1_opy_ import bstack1l111111l1_opy_
bstack1lll11l11l_opy_ = None
bstack11l1l11ll_opy_ = None
bstack1ll111l1_opy_ = None
bstack11l11lll1_opy_ = None
bstack111111111_opy_ = None
bstack1l1l1llll_opy_ = None
bstack1l1l111l1l_opy_ = None
bstack1ll1l1111l_opy_ = None
bstack1ll11l1l11_opy_ = None
bstack11l1l1ll1_opy_ = None
bstack11l1l1ll_opy_ = None
bstack1l11111l1l_opy_ = None
bstack1111l1l11_opy_ = None
bstack1ll1lllll_opy_ = bstack1lll1l_opy_ (u"ࠫࠬឤ")
CONFIG = {}
bstack1111ll11l_opy_ = False
bstack1l1lll1l_opy_ = bstack1lll1l_opy_ (u"ࠬ࠭ឥ")
bstack11lll1111_opy_ = bstack1lll1l_opy_ (u"࠭ࠧឦ")
bstack1lll111111_opy_ = False
bstack111ll1ll_opy_ = []
bstack1lll111ll1_opy_ = bstack1l1l1llll1_opy_
bstack1ll111lllll_opy_ = bstack1lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧឧ")
bstack1ll11l11l11_opy_ = False
bstack1ll1ll1l_opy_ = {}
bstack1ll1l11ll_opy_ = False
logger = bstack1lll111l1_opy_.get_logger(__name__, bstack1lll111ll1_opy_)
store = {
    bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬឨ"): []
}
bstack1ll111llll1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11ll1111ll_opy_ = {}
current_test_uuid = None
def bstack11l1ll1l_opy_(page, bstack1ll1ll11ll_opy_):
    try:
        page.evaluate(bstack1lll1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥឩ"),
                      bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧឪ") + json.dumps(
                          bstack1ll1ll11ll_opy_) + bstack1lll1l_opy_ (u"ࠦࢂࢃࠢឫ"))
    except Exception as e:
        print(bstack1lll1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥឬ"), e)
def bstack1l11l1l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1lll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢឭ"), bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬឮ") + json.dumps(
            message) + bstack1lll1l_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫឯ") + json.dumps(level) + bstack1lll1l_opy_ (u"ࠩࢀࢁࠬឰ"))
    except Exception as e:
        print(bstack1lll1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨឱ"), e)
def pytest_configure(config):
    bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
    config.args = bstack11l111l1l_opy_.bstack1ll11lll1l1_opy_(config.args)
    bstack1l1l111l_opy_.bstack1l1ll1l1_opy_(bstack1l1lllll1l_opy_(config.getoption(bstack1lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨឲ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll11ll1l11_opy_ = item.config.getoption(bstack1lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឳ"))
    plugins = item.config.getoption(bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢ឴"))
    report = outcome.get_result()
    bstack1ll11ll11l1_opy_(item, call, report)
    if bstack1lll1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧ឵") not in plugins or bstack11ll1111_opy_():
        return
    summary = []
    driver = getattr(item, bstack1lll1l_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤា"), None)
    page = getattr(item, bstack1lll1l_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣិ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll11ll11ll_opy_(item, report, summary, bstack1ll11ll1l11_opy_)
    if (page is not None):
        bstack1ll11l1l1ll_opy_(item, report, summary, bstack1ll11ll1l11_opy_)
def bstack1ll11ll11ll_opy_(item, report, summary, bstack1ll11ll1l11_opy_):
    if report.when == bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩី") and report.skipped:
        bstack1lll11l111l_opy_(report)
    if report.when in [bstack1lll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥឹ"), bstack1lll1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢឺ")]:
        return
    if not bstack11111l1l1l_opy_():
        return
    try:
        if (str(bstack1ll11ll1l11_opy_).lower() != bstack1lll1l_opy_ (u"࠭ࡴࡳࡷࡨࠫុ")):
            item._driver.execute_script(
                bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬូ") + json.dumps(
                    report.nodeid) + bstack1lll1l_opy_ (u"ࠨࡿࢀࠫួ"))
        os.environ[bstack1lll1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬើ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1lll1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥឿ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lll1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨៀ")))
    bstack1ll1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠧࠨេ")
    bstack1lll11l111l_opy_(report)
    if not passed:
        try:
            bstack1ll1l1lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1lll1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨែ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1l1lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1lll1l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤៃ")))
        bstack1ll1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠣࠤោ")
        if not passed:
            try:
                bstack1ll1l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lll1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤៅ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1l1lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧំ")
                    + json.dumps(bstack1lll1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧះ"))
                    + bstack1lll1l_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣៈ")
                )
            else:
                item._driver.execute_script(
                    bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ៉")
                    + json.dumps(str(bstack1ll1l1lll_opy_))
                    + bstack1lll1l_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ៊")
                )
        except Exception as e:
            summary.append(bstack1lll1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨ់").format(e))
def bstack1ll11l11l1l_opy_(test_name, error_message):
    try:
        bstack1ll11l1l1l1_opy_ = []
        bstack1llllll1l1_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ៌"), bstack1lll1l_opy_ (u"ࠪ࠴ࠬ៍"))
        bstack1ll11111ll_opy_ = {bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ៎"): test_name, bstack1lll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ៏"): error_message, bstack1lll1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ័"): bstack1llllll1l1_opy_}
        bstack1ll11l1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ៑"))
        if os.path.exists(bstack1ll11l1ll1l_opy_):
            with open(bstack1ll11l1ll1l_opy_) as f:
                bstack1ll11l1l1l1_opy_ = json.load(f)
        bstack1ll11l1l1l1_opy_.append(bstack1ll11111ll_opy_)
        with open(bstack1ll11l1ll1l_opy_, bstack1lll1l_opy_ (u"ࠨࡹ្ࠪ")) as f:
            json.dump(bstack1ll11l1l1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ៓") + str(e))
def bstack1ll11l1l1ll_opy_(item, report, summary, bstack1ll11ll1l11_opy_):
    if report.when in [bstack1lll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ។"), bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ៕")]:
        return
    if (str(bstack1ll11ll1l11_opy_).lower() != bstack1lll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ៖")):
        bstack11l1ll1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lll1l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣៗ")))
    bstack1ll1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠢࠣ៘")
    bstack1lll11l111l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll1l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lll1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ៙").format(e)
                )
        try:
            if passed:
                bstack1ll1l11ll1_opy_(getattr(item, bstack1lll1l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ៚"), None), bstack1lll1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ៛"))
            else:
                error_message = bstack1lll1l_opy_ (u"ࠫࠬៜ")
                if bstack1ll1l1lll_opy_:
                    bstack1l11l1l1_opy_(item._page, str(bstack1ll1l1lll_opy_), bstack1lll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ៝"))
                    bstack1ll1l11ll1_opy_(getattr(item, bstack1lll1l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ៞"), None), bstack1lll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ៟"), str(bstack1ll1l1lll_opy_))
                    error_message = str(bstack1ll1l1lll_opy_)
                else:
                    bstack1ll1l11ll1_opy_(getattr(item, bstack1lll1l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ០"), None), bstack1lll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ១"))
                bstack1ll11l11l1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1lll1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ២").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1lll1l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ៣"), default=bstack1lll1l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ៤"), help=bstack1lll1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ៥"))
    parser.addoption(bstack1lll1l_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ៦"), default=bstack1lll1l_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ៧"), help=bstack1lll1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ៨"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1lll1l_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ៩"), action=bstack1lll1l_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ៪"), default=bstack1lll1l_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ៫"),
                         help=bstack1lll1l_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ៬"))
def bstack11lll1ll11_opy_(log):
    if not (log[bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៭")] and log[bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ៮")].strip()):
        return
    active = bstack11lll11111_opy_()
    log = {
        bstack1lll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ៯"): log[bstack1lll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ៰")],
        bstack1lll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ៱"): bstack11ll1ll1ll_opy_().isoformat() + bstack1lll1l_opy_ (u"ࠬࡠࠧ៲"),
        bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ៳"): log[bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៴")],
    }
    if active:
        if active[bstack1lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭៵")] == bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ៶"):
            log[bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៷")] = active[bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៸")]
        elif active[bstack1lll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ៹")] == bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࠫ៺"):
            log[bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៻")] = active[bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៼")]
    bstack1111ll111_opy_.bstack1l11llll_opy_([log])
def bstack11lll11111_opy_():
    if len(store[bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭៽")]) > 0 and store[bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ៾")][-1]:
        return {
            bstack1lll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩ៿"): bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ᠀"),
            bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᠁"): store[bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ᠂")][-1]
        }
    if store.get(bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ᠃"), None):
        return {
            bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ᠄"): bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࠨ᠅"),
            bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᠆"): store[bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ᠇")]
        }
    return None
bstack11lll11ll1_opy_ = bstack11lll1l1ll_opy_(bstack11lll1ll11_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll11l11l11_opy_
        item._1ll11l1llll_opy_ = True
        bstack111l11lll_opy_ = bstack1ll111llll_opy_.bstack1l1l1lll11_opy_(bstack1111llll1l_opy_(item.own_markers))
        item._a11y_test_case = bstack111l11lll_opy_
        if bstack1ll11l11l11_opy_:
            driver = getattr(item, bstack1lll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ᠈"), None)
            item._a11y_started = bstack1ll111llll_opy_.bstack1lllllll11_opy_(driver, bstack111l11lll_opy_)
        if not bstack1111ll111_opy_.on() or bstack1ll111lllll_opy_ != bstack1lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᠉"):
            return
        global current_test_uuid, bstack11lll11ll1_opy_
        bstack11lll11ll1_opy_.start()
        bstack11ll1l1l11_opy_ = {
            bstack1lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᠊"): uuid4().__str__(),
            bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᠋"): bstack11ll1ll1ll_opy_().isoformat() + bstack1lll1l_opy_ (u"ࠪ࡞ࠬ᠌")
        }
        current_test_uuid = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ᠍")]
        store[bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ᠎")] = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᠏")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11ll1111ll_opy_[item.nodeid] = {**_11ll1111ll_opy_[item.nodeid], **bstack11ll1l1l11_opy_}
        bstack1ll111ll1l1_opy_(item, _11ll1111ll_opy_[item.nodeid], bstack1lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᠐"))
    except Exception as err:
        print(bstack1lll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ᠑"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll111llll1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111lll11l_opy_():
        atexit.register(bstack1l11lllll1_opy_)
        if not bstack1ll111llll1_opy_:
            try:
                bstack1ll11l1ll11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111111l1l1_opy_():
                    bstack1ll11l1ll11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11l1ll11_opy_:
                    signal.signal(s, bstack1ll11l1l11l_opy_)
                bstack1ll111llll1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ᠒") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll11l11l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᠓")
    try:
        if not bstack1111ll111_opy_.on():
            return
        bstack11lll11ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll1l1l11_opy_ = {
            bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ᠔"): uuid,
            bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᠕"): bstack11ll1ll1ll_opy_().isoformat() + bstack1lll1l_opy_ (u"࡚࠭ࠨ᠖"),
            bstack1lll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ᠗"): bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭᠘"),
            bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᠙"): bstack1lll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ᠚"),
            bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ᠛"): bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ᠜")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᠝")] = item
        store[bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ᠞")] = [uuid]
        if not _11ll1111ll_opy_.get(item.nodeid, None):
            _11ll1111ll_opy_[item.nodeid] = {bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᠟"): [], bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᠠ"): []}
        _11ll1111ll_opy_[item.nodeid][bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᠡ")].append(bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᠢ")])
        _11ll1111ll_opy_[item.nodeid + bstack1lll1l_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬᠣ")] = bstack11ll1l1l11_opy_
        bstack1ll11l11lll_opy_(item, bstack11ll1l1l11_opy_, bstack1lll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᠤ"))
    except Exception as err:
        print(bstack1lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᠥ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1ll1ll1l_opy_
        bstack1llllll1l1_opy_ = 0
        if bstack1lll111111_opy_ is True:
            bstack1llllll1l1_opy_ = int(os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᠦ")))
        if bstack1ll111111l_opy_.bstack11ll1lll_opy_() == bstack1lll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᠧ"):
            if bstack1ll111111l_opy_.bstack1l1lll1l11_opy_() == bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᠨ"):
                bstack1ll111lll1l_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᠩ"), None)
                bstack1l11111111_opy_ = bstack1ll111lll1l_opy_ + bstack1lll1l_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣᠪ")
                driver = getattr(item, bstack1lll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᠫ"), None)
                bstack1111l1ll_opy_ = getattr(item, bstack1lll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᠬ"), None)
                bstack1l111l11ll_opy_ = getattr(item, bstack1lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᠭ"), None)
                PercySDK.screenshot(driver, bstack1l11111111_opy_, bstack1111l1ll_opy_=bstack1111l1ll_opy_, bstack1l111l11ll_opy_=bstack1l111l11ll_opy_, bstack1l1lll111_opy_=bstack1llllll1l1_opy_)
        if getattr(item, bstack1lll1l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩᠮ"), False):
            bstack1111l11l_opy_.bstack1lllllll1l_opy_(getattr(item, bstack1lll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᠯ"), None), bstack1ll1ll1l_opy_, logger, item)
        if not bstack1111ll111_opy_.on():
            return
        bstack11ll1l1l11_opy_ = {
            bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᠰ"): uuid4().__str__(),
            bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᠱ"): bstack11ll1ll1ll_opy_().isoformat() + bstack1lll1l_opy_ (u"࡚࠭ࠨᠲ"),
            bstack1lll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᠳ"): bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᠴ"),
            bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᠵ"): bstack1lll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᠶ"),
            bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᠷ"): bstack1lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᠸ")
        }
        _11ll1111ll_opy_[item.nodeid + bstack1lll1l_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᠹ")] = bstack11ll1l1l11_opy_
        bstack1ll11l11lll_opy_(item, bstack11ll1l1l11_opy_, bstack1lll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᠺ"))
    except Exception as err:
        print(bstack1lll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧᠻ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1111ll111_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lll11ll111_opy_(fixturedef.argname):
        store[bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᠼ")] = request.node
    elif bstack1lll11l1l11_opy_(fixturedef.argname):
        store[bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᠽ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᠾ"): fixturedef.argname,
            bstack1lll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᠿ"): bstack11111lllll_opy_(outcome),
            bstack1lll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᡀ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᡁ")]
        if not _11ll1111ll_opy_.get(current_test_item.nodeid, None):
            _11ll1111ll_opy_[current_test_item.nodeid] = {bstack1lll1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᡂ"): []}
        _11ll1111ll_opy_[current_test_item.nodeid][bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᡃ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1lll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᡄ"), str(err))
if bstack11ll1111_opy_() and bstack1111ll111_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11ll1111ll_opy_[request.node.nodeid][bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᡅ")].bstack1ll11lll11_opy_(id(step))
        except Exception as err:
            print(bstack1lll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪᡆ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11ll1111ll_opy_[request.node.nodeid][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᡇ")].bstack11lll111l1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᡈ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11lll1l11l_opy_: bstack11lll1l111_opy_ = _11ll1111ll_opy_[request.node.nodeid][bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᡉ")]
            bstack11lll1l11l_opy_.bstack11lll111l1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1lll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ᡊ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111lllll_opy_
        try:
            if not bstack1111ll111_opy_.on() or bstack1ll111lllll_opy_ != bstack1lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᡋ"):
                return
            global bstack11lll11ll1_opy_
            bstack11lll11ll1_opy_.start()
            driver = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᡌ"), None)
            if not _11ll1111ll_opy_.get(request.node.nodeid, None):
                _11ll1111ll_opy_[request.node.nodeid] = {}
            bstack11lll1l11l_opy_ = bstack11lll1l111_opy_.bstack1ll1ll1lll1_opy_(
                scenario, feature, request.node,
                name=bstack1lll11l1l1l_opy_(request.node, scenario),
                bstack11llll1111_opy_=bstack11l111ll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1lll1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᡍ"),
                tags=bstack1lll11ll11l_opy_(feature, scenario),
                bstack11ll1l1111_opy_=bstack1111ll111_opy_.bstack11ll1llll1_opy_(driver) if driver and driver.session_id else {}
            )
            _11ll1111ll_opy_[request.node.nodeid][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᡎ")] = bstack11lll1l11l_opy_
            bstack1ll111ll11l_opy_(bstack11lll1l11l_opy_.uuid)
            bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᡏ"), bstack11lll1l11l_opy_)
        except Exception as err:
            print(bstack1lll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪᡐ"), str(err))
def bstack1ll111l1lll_opy_(bstack11lll1l1l1_opy_):
    if bstack11lll1l1l1_opy_ in store[bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᡑ")]:
        store[bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᡒ")].remove(bstack11lll1l1l1_opy_)
def bstack1ll111ll11l_opy_(bstack11llll1lll_opy_):
    store[bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᡓ")] = bstack11llll1lll_opy_
    threading.current_thread().current_test_uuid = bstack11llll1lll_opy_
@bstack1111ll111_opy_.bstack1ll1l1l1ll1_opy_
def bstack1ll11ll11l1_opy_(item, call, report):
    global bstack1ll111lllll_opy_
    bstack1llll1ll_opy_ = bstack11l111ll1_opy_()
    if hasattr(report, bstack1lll1l_opy_ (u"ࠬࡹࡴࡰࡲࠪᡔ")):
        bstack1llll1ll_opy_ = bstack111l11ll11_opy_(report.stop)
    elif hasattr(report, bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬᡕ")):
        bstack1llll1ll_opy_ = bstack111l11ll11_opy_(report.start)
    try:
        if getattr(report, bstack1lll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬᡖ"), bstack1lll1l_opy_ (u"ࠨࠩᡗ")) == bstack1lll1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᡘ"):
            bstack11lll11ll1_opy_.reset()
        if getattr(report, bstack1lll1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡙ"), bstack1lll1l_opy_ (u"ࠫࠬᡚ")) == bstack1lll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᡛ"):
            if bstack1ll111lllll_opy_ == bstack1lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᡜ"):
                _11ll1111ll_opy_[item.nodeid][bstack1lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᡝ")] = bstack1llll1ll_opy_
                bstack1ll111ll1l1_opy_(item, _11ll1111ll_opy_[item.nodeid], bstack1lll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᡞ"), report, call)
                store[bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᡟ")] = None
            elif bstack1ll111lllll_opy_ == bstack1lll1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᡠ"):
                bstack11lll1l11l_opy_ = _11ll1111ll_opy_[item.nodeid][bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᡡ")]
                bstack11lll1l11l_opy_.set(hooks=_11ll1111ll_opy_[item.nodeid].get(bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᡢ"), []))
                exception, bstack11llll1l1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11llll1l1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1lll1l_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬᡣ"), bstack1lll1l_opy_ (u"ࠧࠨᡤ"))]
                bstack11lll1l11l_opy_.stop(time=bstack1llll1ll_opy_, result=Result(result=getattr(report, bstack1lll1l_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩᡥ"), bstack1lll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᡦ")), exception=exception, bstack11llll1l1l_opy_=bstack11llll1l1l_opy_))
                bstack1111ll111_opy_.bstack11lll11lll_opy_(bstack1lll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᡧ"), _11ll1111ll_opy_[item.nodeid][bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᡨ")])
        elif getattr(report, bstack1lll1l_opy_ (u"ࠬࡽࡨࡦࡰࠪᡩ"), bstack1lll1l_opy_ (u"࠭ࠧᡪ")) in [bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᡫ"), bstack1lll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᡬ")]:
            bstack11llll111l_opy_ = item.nodeid + bstack1lll1l_opy_ (u"ࠩ࠰ࠫᡭ") + getattr(report, bstack1lll1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡮ"), bstack1lll1l_opy_ (u"ࠫࠬᡯ"))
            if getattr(report, bstack1lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᡰ"), False):
                hook_type = bstack1lll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᡱ") if getattr(report, bstack1lll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬᡲ"), bstack1lll1l_opy_ (u"ࠨࠩᡳ")) == bstack1lll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᡴ") else bstack1lll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᡵ")
                _11ll1111ll_opy_[bstack11llll111l_opy_] = {
                    bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᡶ"): uuid4().__str__(),
                    bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᡷ"): bstack1llll1ll_opy_,
                    bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᡸ"): hook_type
                }
            _11ll1111ll_opy_[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᡹")] = bstack1llll1ll_opy_
            bstack1ll111l1lll_opy_(_11ll1111ll_opy_[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᡺")])
            bstack1ll11l11lll_opy_(item, _11ll1111ll_opy_[bstack11llll111l_opy_], bstack1lll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ᡻"), report, call)
            if getattr(report, bstack1lll1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ᡼"), bstack1lll1l_opy_ (u"ࠫࠬ᡽")) == bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ᡾"):
                if getattr(report, bstack1lll1l_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ᡿"), bstack1lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᢀ")) == bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᢁ"):
                    bstack11ll1l1l11_opy_ = {
                        bstack1lll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢂ"): uuid4().__str__(),
                        bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᢃ"): bstack11l111ll1_opy_(),
                        bstack1lll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᢄ"): bstack11l111ll1_opy_()
                    }
                    _11ll1111ll_opy_[item.nodeid] = {**_11ll1111ll_opy_[item.nodeid], **bstack11ll1l1l11_opy_}
                    bstack1ll111ll1l1_opy_(item, _11ll1111ll_opy_[item.nodeid], bstack1lll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᢅ"))
                    bstack1ll111ll1l1_opy_(item, _11ll1111ll_opy_[item.nodeid], bstack1lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᢆ"), report, call)
    except Exception as err:
        print(bstack1lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬᢇ"), str(err))
def bstack1ll11l111l1_opy_(test, bstack11ll1l1l11_opy_, result=None, call=None, bstack1lll111l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11lll1l11l_opy_ = {
        bstack1lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᢈ"): bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢉ")],
        bstack1lll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᢊ"): bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᢋ"),
        bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢌ"): test.name,
        bstack1lll1l_opy_ (u"࠭ࡢࡰࡦࡼࠫᢍ"): {
            bstack1lll1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᢎ"): bstack1lll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᢏ"),
            bstack1lll1l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᢐ"): inspect.getsource(test.obj)
        },
        bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢑ"): test.name,
        bstack1lll1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᢒ"): test.name,
        bstack1lll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᢓ"): bstack11l111l1l_opy_.bstack11l1ll1l1l_opy_(test),
        bstack1lll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᢔ"): file_path,
        bstack1lll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᢕ"): file_path,
        bstack1lll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᢖ"): bstack1lll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᢗ"),
        bstack1lll1l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᢘ"): file_path,
        bstack1lll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᢙ"): bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᢚ")],
        bstack1lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᢛ"): bstack1lll1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᢜ"),
        bstack1lll1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᢝ"): {
            bstack1lll1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᢞ"): test.nodeid
        },
        bstack1lll1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᢟ"): bstack1111llll1l_opy_(test.own_markers)
    }
    if bstack1lll111l1l_opy_ in [bstack1lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᢠ"), bstack1lll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᢡ")]:
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"࠭࡭ࡦࡶࡤࠫᢢ")] = {
            bstack1lll1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᢣ"): bstack11ll1l1l11_opy_.get(bstack1lll1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᢤ"), [])
        }
    if bstack1lll111l1l_opy_ == bstack1lll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᢥ"):
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢦ")] = bstack1lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᢧ")
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᢨ")] = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷᢩࠬ")]
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᢪ")] = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᢫")]
    if result:
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᢬")] = result.outcome
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ᢭")] = result.duration * 1000
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᢮")] = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᢯")]
        if result.failed:
            bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᢰ")] = bstack1111ll111_opy_.bstack11l11ll111_opy_(call.excinfo.typename)
            bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᢱ")] = bstack1111ll111_opy_.bstack1ll1l1lll1l_opy_(call.excinfo, result)
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᢲ")] = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᢳ")]
    if outcome:
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢴ")] = bstack11111lllll_opy_(outcome)
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᢵ")] = 0
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢶ")] = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᢷ")]
        if bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᢸ")] == bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᢹ"):
            bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᢺ")] = bstack1lll1l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᢻ")  # bstack1ll111ll111_opy_
            bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᢼ")] = [{bstack1lll1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᢽ"): [bstack1lll1l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᢾ")]}]
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢿ")] = bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᣀ")]
    return bstack11lll1l11l_opy_
def bstack1ll11ll111l_opy_(test, bstack11l1ll11l1_opy_, bstack1lll111l1l_opy_, result, call, outcome, bstack1ll111lll11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᣁ")]
    hook_name = bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᣂ")]
    hook_data = {
        bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᣃ"): bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᣄ")],
        bstack1lll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᣅ"): bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᣆ"),
        bstack1lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᣇ"): bstack1lll1l_opy_ (u"ࠩࡾࢁࠬᣈ").format(bstack1lll111llll_opy_(hook_name)),
        bstack1lll1l_opy_ (u"ࠪࡦࡴࡪࡹࠨᣉ"): {
            bstack1lll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᣊ"): bstack1lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᣋ"),
            bstack1lll1l_opy_ (u"࠭ࡣࡰࡦࡨࠫᣌ"): None
        },
        bstack1lll1l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᣍ"): test.name,
        bstack1lll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᣎ"): bstack11l111l1l_opy_.bstack11l1ll1l1l_opy_(test, hook_name),
        bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᣏ"): file_path,
        bstack1lll1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᣐ"): file_path,
        bstack1lll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣑ"): bstack1lll1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᣒ"),
        bstack1lll1l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᣓ"): file_path,
        bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᣔ"): bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᣕ")],
        bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᣖ"): bstack1lll1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᣗ") if bstack1ll111lllll_opy_ == bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᣘ") else bstack1lll1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᣙ"),
        bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᣚ"): hook_type
    }
    bstack1ll1lll1l1l_opy_ = bstack11l1lll1ll_opy_(_11ll1111ll_opy_.get(test.nodeid, None))
    if bstack1ll1lll1l1l_opy_:
        hook_data[bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᣛ")] = bstack1ll1lll1l1l_opy_
    if result:
        hook_data[bstack1lll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣜ")] = result.outcome
        hook_data[bstack1lll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᣝ")] = result.duration * 1000
        hook_data[bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣞ")] = bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᣟ")]
        if result.failed:
            hook_data[bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᣠ")] = bstack1111ll111_opy_.bstack11l11ll111_opy_(call.excinfo.typename)
            hook_data[bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᣡ")] = bstack1111ll111_opy_.bstack1ll1l1lll1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1lll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᣢ")] = bstack11111lllll_opy_(outcome)
        hook_data[bstack1lll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᣣ")] = 100
        hook_data[bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣤ")] = bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣥ")]
        if hook_data[bstack1lll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣦ")] == bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᣧ"):
            hook_data[bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᣨ")] = bstack1lll1l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᣩ")  # bstack1ll111ll111_opy_
            hook_data[bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᣪ")] = [{bstack1lll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᣫ"): [bstack1lll1l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᣬ")]}]
    if bstack1ll111lll11_opy_:
        hook_data[bstack1lll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣭ")] = bstack1ll111lll11_opy_.result
        hook_data[bstack1lll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᣮ")] = bstack1111l1l1l1_opy_(bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᣯ")], bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣰ")])
        hook_data[bstack1lll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣱ")] = bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣲ")]
        if hook_data[bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᣳ")] == bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᣴ"):
            hook_data[bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᣵ")] = bstack1111ll111_opy_.bstack11l11ll111_opy_(bstack1ll111lll11_opy_.exception_type)
            hook_data[bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᣶")] = [{bstack1lll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ᣷"): bstack1111l1ll11_opy_(bstack1ll111lll11_opy_.exception)}]
    return hook_data
def bstack1ll111ll1l1_opy_(test, bstack11ll1l1l11_opy_, bstack1lll111l1l_opy_, result=None, call=None, outcome=None):
    bstack11lll1l11l_opy_ = bstack1ll11l111l1_opy_(test, bstack11ll1l1l11_opy_, result, call, bstack1lll111l1l_opy_, outcome)
    driver = getattr(test, bstack1lll1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ᣸"), None)
    if bstack1lll111l1l_opy_ == bstack1lll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᣹") and driver:
        bstack11lll1l11l_opy_[bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ᣺")] = bstack1111ll111_opy_.bstack11ll1llll1_opy_(driver)
    if bstack1lll111l1l_opy_ == bstack1lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ᣻"):
        bstack1lll111l1l_opy_ = bstack1lll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ᣼")
    bstack11ll111111_opy_ = {
        bstack1lll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᣽"): bstack1lll111l1l_opy_,
        bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ᣾"): bstack11lll1l11l_opy_
    }
    bstack1111ll111_opy_.bstack11ll1ll111_opy_(bstack11ll111111_opy_)
def bstack1ll11l11lll_opy_(test, bstack11ll1l1l11_opy_, bstack1lll111l1l_opy_, result=None, call=None, outcome=None, bstack1ll111lll11_opy_=None):
    hook_data = bstack1ll11ll111l_opy_(test, bstack11ll1l1l11_opy_, bstack1lll111l1l_opy_, result, call, outcome, bstack1ll111lll11_opy_)
    bstack11ll111111_opy_ = {
        bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᣿"): bstack1lll111l1l_opy_,
        bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᤀ"): hook_data
    }
    bstack1111ll111_opy_.bstack11ll1ll111_opy_(bstack11ll111111_opy_)
def bstack11l1lll1ll_opy_(bstack11ll1l1l11_opy_):
    if not bstack11ll1l1l11_opy_:
        return None
    if bstack11ll1l1l11_opy_.get(bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᤁ"), None):
        return getattr(bstack11ll1l1l11_opy_[bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᤂ")], bstack1lll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᤃ"), None)
    return bstack11ll1l1l11_opy_.get(bstack1lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᤄ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1111ll111_opy_.on():
            return
        places = [bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᤅ"), bstack1lll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᤆ"), bstack1lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᤇ")]
        bstack11l1llll11_opy_ = []
        for bstack1ll11l1l111_opy_ in places:
            records = caplog.get_records(bstack1ll11l1l111_opy_)
            bstack1ll11l1lll1_opy_ = bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᤈ") if bstack1ll11l1l111_opy_ == bstack1lll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᤉ") else bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᤊ")
            bstack1ll111l1l1l_opy_ = request.node.nodeid + (bstack1lll1l_opy_ (u"࠭ࠧᤋ") if bstack1ll11l1l111_opy_ == bstack1lll1l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᤌ") else bstack1lll1l_opy_ (u"ࠨ࠯ࠪᤍ") + bstack1ll11l1l111_opy_)
            bstack11llll1lll_opy_ = bstack11l1lll1ll_opy_(_11ll1111ll_opy_.get(bstack1ll111l1l1l_opy_, None))
            if not bstack11llll1lll_opy_:
                continue
            for record in records:
                if bstack11111lll1l_opy_(record.message):
                    continue
                bstack11l1llll11_opy_.append({
                    bstack1lll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᤎ"): bstack111l1111ll_opy_(record.created).isoformat() + bstack1lll1l_opy_ (u"ࠪ࡞ࠬᤏ"),
                    bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᤐ"): record.levelname,
                    bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᤑ"): record.message,
                    bstack1ll11l1lll1_opy_: bstack11llll1lll_opy_
                })
        if len(bstack11l1llll11_opy_) > 0:
            bstack1111ll111_opy_.bstack1l11llll_opy_(bstack11l1llll11_opy_)
    except Exception as err:
        print(bstack1lll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪᤒ"), str(err))
def bstack1l11l1ll11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll1l11ll_opy_
    bstack11l1ll11_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᤓ"), None) and bstack1ll111lll1_opy_(
            threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᤔ"), None)
    bstack1l11ll1l11_opy_ = getattr(driver, bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᤕ"), None) != None and getattr(driver, bstack1lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᤖ"), None) == True
    if sequence == bstack1lll1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᤗ") and driver != None:
      if not bstack1ll1l11ll_opy_ and bstack11111l1l1l_opy_() and bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᤘ") in CONFIG and CONFIG[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᤙ")] == True and bstack1l111111l1_opy_.bstack1llll111l1_opy_(driver_command) and (bstack1l11ll1l11_opy_ or bstack11l1ll11_opy_) and not bstack1l11llll1_opy_(args):
        try:
          bstack1ll1l11ll_opy_ = True
          logger.debug(bstack1lll1l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩᤚ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭ᤛ").format(str(err)))
        bstack1ll1l11ll_opy_ = False
    if sequence == bstack1lll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᤜ"):
        if driver_command == bstack1lll1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᤝ"):
            bstack1111ll111_opy_.bstack1lll11ll1l_opy_({
                bstack1lll1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᤞ"): response[bstack1lll1l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ᤟")],
                bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᤠ"): store[bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᤡ")]
            })
def bstack1l11lllll1_opy_():
    global bstack111ll1ll_opy_
    bstack1lll111l1_opy_.bstack11llllll1l_opy_()
    logging.shutdown()
    bstack1111ll111_opy_.bstack11l1ll1l11_opy_()
    for driver in bstack111ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11l1l11l_opy_(*args):
    global bstack111ll1ll_opy_
    bstack1111ll111_opy_.bstack11l1ll1l11_opy_()
    for driver in bstack111ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1ll1lll_opy_(self, *args, **kwargs):
    bstack1l11l1111l_opy_ = bstack1lll11l11l_opy_(self, *args, **kwargs)
    bstack1111ll111_opy_.bstack111l1l1l_opy_(self)
    return bstack1l11l1111l_opy_
def bstack1l1llll111_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
    if bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬᤢ")):
        return
    bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ᤣ"), True)
    global bstack1ll1lllll_opy_
    global bstack1ll1lll111_opy_
    bstack1ll1lllll_opy_ = framework_name
    logger.info(bstack11lll1l11_opy_.format(bstack1ll1lllll_opy_.split(bstack1lll1l_opy_ (u"ࠪ࠱ࠬᤤ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11111l1l1l_opy_():
            Service.start = bstack11ll11111_opy_
            Service.stop = bstack1l11l11l1l_opy_
            webdriver.Remote.__init__ = bstack1lll1l111_opy_
            webdriver.Remote.get = bstack1111l1ll1_opy_
            if not isinstance(os.getenv(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬᤥ")), str):
                return
            WebDriver.close = bstack1ll1111l1l_opy_
            WebDriver.quit = bstack11l1ll111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack11111l1l1l_opy_() and bstack1111ll111_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1ll1lll_opy_
        bstack1ll1lll111_opy_ = True
    except Exception as e:
        pass
    bstack1l11ll11_opy_()
    if os.environ.get(bstack1lll1l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᤦ")):
        bstack1ll1lll111_opy_ = eval(os.environ.get(bstack1lll1l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᤧ")))
    if not bstack1ll1lll111_opy_:
        bstack11111l1ll_opy_(bstack1lll1l_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤᤨ"), bstack111l1l11_opy_)
    if bstack11111l1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11l11111l_opy_
        except Exception as e:
            logger.error(bstack111llll1_opy_.format(str(e)))
    if bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᤩ") in str(framework_name).lower():
        if not bstack11111l1l1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1lll11l1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1ll111l1_opy_
            Config.getoption = bstack1ll111l11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll111ll1_opy_
        except Exception as e:
            pass
def bstack11l1ll111_opy_(self):
    global bstack1ll1lllll_opy_
    global bstack1l11ll11l_opy_
    global bstack11l1l11ll_opy_
    try:
        if bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᤪ") in bstack1ll1lllll_opy_ and self.session_id != None and bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᤫ"), bstack1lll1l_opy_ (u"ࠫࠬ᤬")) != bstack1lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᤭"):
            bstack1l1lllll1_opy_ = bstack1lll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᤮") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᤯")
            bstack1lll1l1ll_opy_(logger, True)
            if self != None:
                bstack1l1111l111_opy_(self, bstack1l1lllll1_opy_, bstack1lll1l_opy_ (u"ࠨ࠮ࠣࠫᤰ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᤱ"), None)
        if item is not None and bstack1ll11l11l11_opy_:
            bstack1111l11l_opy_.bstack1lllllll1l_opy_(self, bstack1ll1ll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1lll1l_opy_ (u"ࠪࠫᤲ")
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᤳ") + str(e))
    bstack11l1l11ll_opy_(self)
    self.session_id = None
def bstack1lll1l111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l11ll11l_opy_
    global bstack1l1ll1ll1_opy_
    global bstack1lll111111_opy_
    global bstack1ll1lllll_opy_
    global bstack1lll11l11l_opy_
    global bstack111ll1ll_opy_
    global bstack1l1lll1l_opy_
    global bstack11lll1111_opy_
    global bstack1ll11l11l11_opy_
    global bstack1ll1ll1l_opy_
    CONFIG[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᤴ")] = str(bstack1ll1lllll_opy_) + str(__version__)
    command_executor = bstack1ll11l1l1_opy_(bstack1l1lll1l_opy_)
    logger.debug(bstack11l111lll_opy_.format(command_executor))
    proxy = bstack1l111111ll_opy_(CONFIG, proxy)
    bstack1llllll1l1_opy_ = 0
    try:
        if bstack1lll111111_opy_ is True:
            bstack1llllll1l1_opy_ = int(os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᤵ")))
    except:
        bstack1llllll1l1_opy_ = 0
    bstack1l1l111lll_opy_ = bstack1l11lllll_opy_(CONFIG, bstack1llllll1l1_opy_)
    logger.debug(bstack111l11ll_opy_.format(str(bstack1l1l111lll_opy_)))
    bstack1ll1ll1l_opy_ = CONFIG.get(bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᤶ"))[bstack1llllll1l1_opy_]
    if bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᤷ") in CONFIG and CONFIG[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᤸ")]:
        bstack1l11lll1l_opy_(bstack1l1l111lll_opy_, bstack11lll1111_opy_)
    if bstack1ll111llll_opy_.bstack11l1lllll_opy_(CONFIG, bstack1llllll1l1_opy_) and bstack1ll111llll_opy_.bstack11ll1l11_opy_(bstack1l1l111lll_opy_, options, desired_capabilities):
        bstack1ll11l11l11_opy_ = True
        bstack1ll111llll_opy_.set_capabilities(bstack1l1l111lll_opy_, CONFIG)
    if desired_capabilities:
        bstack11l1lll11_opy_ = bstack1l1ll1ll_opy_(desired_capabilities)
        bstack11l1lll11_opy_[bstack1lll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅ᤹ࠪ")] = bstack1lll1lll1_opy_(CONFIG)
        bstack1l11l111l_opy_ = bstack1l11lllll_opy_(bstack11l1lll11_opy_)
        if bstack1l11l111l_opy_:
            bstack1l1l111lll_opy_ = update(bstack1l11l111l_opy_, bstack1l1l111lll_opy_)
        desired_capabilities = None
    if options:
        bstack111ll11l1_opy_(options, bstack1l1l111lll_opy_)
    if not options:
        options = bstack1ll1l1ll1l_opy_(bstack1l1l111lll_opy_)
    if proxy and bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ᤺")):
        options.proxy(proxy)
    if options and bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳᤻ࠫ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1111l1l1l_opy_() < version.parse(bstack1lll1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ᤼")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1l111lll_opy_)
    logger.info(bstack1llll1l11l_opy_)
    if bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ᤽")):
        bstack1lll11l11l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ᤾")):
        bstack1lll11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ᤿")):
        bstack1lll11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll11l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l11l11111_opy_ = bstack1lll1l_opy_ (u"ࠪࠫ᥀")
        if bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ᥁")):
            bstack1l11l11111_opy_ = self.caps.get(bstack1lll1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ᥂"))
        else:
            bstack1l11l11111_opy_ = self.capabilities.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ᥃"))
        if bstack1l11l11111_opy_:
            bstack1l1l1ll11_opy_(bstack1l11l11111_opy_)
            if bstack1111l1l1l_opy_() <= version.parse(bstack1lll1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ᥄")):
                self.command_executor._url = bstack1lll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᥅") + bstack1l1lll1l_opy_ + bstack1lll1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ᥆")
            else:
                self.command_executor._url = bstack1lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᥇") + bstack1l11l11111_opy_ + bstack1lll1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ᥈")
            logger.debug(bstack1lllll1l1_opy_.format(bstack1l11l11111_opy_))
        else:
            logger.debug(bstack1l1l11lll_opy_.format(bstack1lll1l_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ᥉")))
    except Exception as e:
        logger.debug(bstack1l1l11lll_opy_.format(e))
    bstack1l11ll11l_opy_ = self.session_id
    if bstack1lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᥊") in bstack1ll1lllll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1lll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᥋"), None)
        if item:
            bstack1ll11ll1111_opy_ = getattr(item, bstack1lll1l_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭᥌"), False)
            if not getattr(item, bstack1lll1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᥍"), None) and bstack1ll11ll1111_opy_:
                setattr(store[bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ᥎")], bstack1lll1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ᥏"), self)
        bstack1111ll111_opy_.bstack111l1l1l_opy_(self)
    bstack111ll1ll_opy_.append(self)
    if bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᥐ") in CONFIG and bstack1lll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᥑ") in CONFIG[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᥒ")][bstack1llllll1l1_opy_]:
        bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᥓ")][bstack1llllll1l1_opy_][bstack1lll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᥔ")]
    logger.debug(bstack1l1l1lll_opy_.format(bstack1l11ll11l_opy_))
def bstack1111l1ll1_opy_(self, url):
    global bstack1ll11l1l11_opy_
    global CONFIG
    try:
        bstack11111ll11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll111ll_opy_.format(str(err)))
    try:
        bstack1ll11l1l11_opy_(self, url)
    except Exception as e:
        try:
            bstack11llll1l_opy_ = str(e)
            if any(err_msg in bstack11llll1l_opy_ for err_msg in bstack1llllll111_opy_):
                bstack11111ll11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll111ll_opy_.format(str(err)))
        raise e
def bstack1ll1ll1ll1_opy_(item, when):
    global bstack1l11111l1l_opy_
    try:
        bstack1l11111l1l_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll111ll1_opy_(item, call, rep):
    global bstack1111l1l11_opy_
    global bstack111ll1ll_opy_
    name = bstack1lll1l_opy_ (u"ࠪࠫᥕ")
    try:
        if rep.when == bstack1lll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᥖ"):
            bstack1l11ll11l_opy_ = threading.current_thread().bstackSessionId
            bstack1ll11ll1l11_opy_ = item.config.getoption(bstack1lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᥗ"))
            try:
                if (str(bstack1ll11ll1l11_opy_).lower() != bstack1lll1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᥘ")):
                    name = str(rep.nodeid)
                    bstack1llll1l1ll_opy_ = bstack11l1l1l11_opy_(bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᥙ"), name, bstack1lll1l_opy_ (u"ࠨࠩᥚ"), bstack1lll1l_opy_ (u"ࠩࠪᥛ"), bstack1lll1l_opy_ (u"ࠪࠫᥜ"), bstack1lll1l_opy_ (u"ࠫࠬᥝ"))
                    os.environ[bstack1lll1l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᥞ")] = name
                    for driver in bstack111ll1ll_opy_:
                        if bstack1l11ll11l_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll1l1ll_opy_)
            except Exception as e:
                logger.debug(bstack1lll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ᥟ").format(str(e)))
            try:
                bstack1l1l11l1ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1lll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᥠ"):
                    status = bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᥡ") if rep.outcome.lower() == bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᥢ") else bstack1lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᥣ")
                    reason = bstack1lll1l_opy_ (u"ࠫࠬᥤ")
                    if status == bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᥥ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1lll1l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᥦ") if status == bstack1lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᥧ") else bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᥨ")
                    data = name + bstack1lll1l_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫᥩ") if status == bstack1lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᥪ") else name + bstack1lll1l_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧᥫ") + reason
                    bstack1l111lllll_opy_ = bstack11l1l1l11_opy_(bstack1lll1l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᥬ"), bstack1lll1l_opy_ (u"࠭ࠧᥭ"), bstack1lll1l_opy_ (u"ࠧࠨ᥮"), bstack1lll1l_opy_ (u"ࠨࠩ᥯"), level, data)
                    for driver in bstack111ll1ll_opy_:
                        if bstack1l11ll11l_opy_ == driver.session_id:
                            driver.execute_script(bstack1l111lllll_opy_)
            except Exception as e:
                logger.debug(bstack1lll1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ᥰ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧᥱ").format(str(e)))
    bstack1111l1l11_opy_(item, call, rep)
notset = Notset()
def bstack1ll111l11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11l1l1ll_opy_
    if str(name).lower() == bstack1lll1l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᥲ"):
        return bstack1lll1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᥳ")
    else:
        return bstack11l1l1ll_opy_(self, name, default, skip)
def bstack11l11111l_opy_(self):
    global CONFIG
    global bstack1l1l111l1l_opy_
    try:
        proxy = bstack1l1l1lll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1lll1l_opy_ (u"࠭࠮ࡱࡣࡦࠫᥴ")):
                proxies = bstack1llll111ll_opy_(proxy, bstack1ll11l1l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1111111_opy_ = proxies.popitem()
                    if bstack1lll1l_opy_ (u"ࠢ࠻࠱࠲ࠦ᥵") in bstack1ll1111111_opy_:
                        return bstack1ll1111111_opy_
                    else:
                        return bstack1lll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᥶") + bstack1ll1111111_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ᥷").format(str(e)))
    return bstack1l1l111l1l_opy_(self)
def bstack11111l1l_opy_():
    return (bstack1lll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭᥸") in CONFIG or bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᥹") in CONFIG) and bstack11lllll1l_opy_() and bstack1111l1l1l_opy_() >= version.parse(
        bstack11llllllll_opy_)
def bstack1llll1111l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1ll1ll1_opy_
    global bstack1lll111111_opy_
    global bstack1ll1lllll_opy_
    CONFIG[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᥺")] = str(bstack1ll1lllll_opy_) + str(__version__)
    bstack1llllll1l1_opy_ = 0
    try:
        if bstack1lll111111_opy_ is True:
            bstack1llllll1l1_opy_ = int(os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᥻")))
    except:
        bstack1llllll1l1_opy_ = 0
    CONFIG[bstack1lll1l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᥼")] = True
    bstack1l1l111lll_opy_ = bstack1l11lllll_opy_(CONFIG, bstack1llllll1l1_opy_)
    logger.debug(bstack111l11ll_opy_.format(str(bstack1l1l111lll_opy_)))
    if CONFIG.get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ᥽")):
        bstack1l11lll1l_opy_(bstack1l1l111lll_opy_, bstack11lll1111_opy_)
    if bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᥾") in CONFIG and bstack1lll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᥿") in CONFIG[bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᦀ")][bstack1llllll1l1_opy_]:
        bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᦁ")][bstack1llllll1l1_opy_][bstack1lll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᦂ")]
    import urllib
    import json
    bstack1l111ll1_opy_ = bstack1lll1l_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩᦃ") + urllib.parse.quote(json.dumps(bstack1l1l111lll_opy_))
    browser = self.connect(bstack1l111ll1_opy_)
    return browser
def bstack1l11ll11_opy_():
    global bstack1ll1lll111_opy_
    global bstack1ll1lllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l111l11_opy_
        if not bstack11111l1l1l_opy_():
            global bstack11ll11l1l_opy_
            if not bstack11ll11l1l_opy_:
                from bstack_utils.helper import bstack1l1ll1l11l_opy_, bstack1l111l1ll1_opy_
                bstack11ll11l1l_opy_ = bstack1l1ll1l11l_opy_()
                bstack1l111l1ll1_opy_(bstack1ll1lllll_opy_)
            BrowserType.connect = bstack1l1l111l11_opy_
            return
        BrowserType.launch = bstack1llll1111l_opy_
        bstack1ll1lll111_opy_ = True
    except Exception as e:
        pass
def bstack1ll11l11ll1_opy_():
    global CONFIG
    global bstack1111ll11l_opy_
    global bstack1l1lll1l_opy_
    global bstack11lll1111_opy_
    global bstack1lll111111_opy_
    global bstack1lll111ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧᦄ")))
    bstack1111ll11l_opy_ = eval(os.environ.get(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᦅ")))
    bstack1l1lll1l_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪᦆ"))
    bstack1lllll1ll1_opy_(CONFIG, bstack1111ll11l_opy_)
    bstack1lll111ll1_opy_ = bstack1lll111l1_opy_.bstack1l1ll11l_opy_(CONFIG, bstack1lll111ll1_opy_)
    global bstack1lll11l11l_opy_
    global bstack11l1l11ll_opy_
    global bstack1ll111l1_opy_
    global bstack11l11lll1_opy_
    global bstack111111111_opy_
    global bstack1l1l1llll_opy_
    global bstack1ll1l1111l_opy_
    global bstack1ll11l1l11_opy_
    global bstack1l1l111l1l_opy_
    global bstack11l1l1ll_opy_
    global bstack1l11111l1l_opy_
    global bstack1111l1l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll11l11l_opy_ = webdriver.Remote.__init__
        bstack11l1l11ll_opy_ = WebDriver.quit
        bstack1ll1l1111l_opy_ = WebDriver.close
        bstack1ll11l1l11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᦇ") in CONFIG or bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᦈ") in CONFIG) and bstack11lllll1l_opy_():
        if bstack1111l1l1l_opy_() < version.parse(bstack11llllllll_opy_):
            logger.error(bstack1ll11ll1l1_opy_.format(bstack1111l1l1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1l111l1l_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack111llll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11l1l1ll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l11111l1l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l11l1111_opy_)
    try:
        from pytest_bdd import reporting
        bstack1111l1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧᦉ"))
    bstack11lll1111_opy_ = CONFIG.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᦊ"), {}).get(bstack1lll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᦋ"))
    bstack1lll111111_opy_ = True
    bstack1l1llll111_opy_(bstack1l111llll_opy_)
if (bstack1111lll11l_opy_()):
    bstack1ll11l11ll1_opy_()
@bstack11ll1l1lll_opy_(class_method=False)
def bstack1ll11l1111l_opy_(hook_name, event, bstack1ll11l11111_opy_=None):
    if hook_name not in [bstack1lll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᦌ"), bstack1lll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᦍ"), bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᦎ"), bstack1lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᦏ"), bstack1lll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᦐ"), bstack1lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᦑ"), bstack1lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᦒ"), bstack1lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᦓ")]:
        return
    node = store[bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᦔ")]
    if hook_name in [bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᦕ"), bstack1lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᦖ")]:
        node = store[bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᦗ")]
    elif hook_name in [bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᦘ"), bstack1lll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᦙ")]:
        node = store[bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧᦚ")]
    if event == bstack1lll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᦛ"):
        hook_type = bstack1lll11l1ll1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l1ll11l1_opy_ = {
            bstack1lll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᦜ"): uuid,
            bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᦝ"): bstack11l111ll1_opy_(),
            bstack1lll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᦞ"): bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᦟ"),
            bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᦠ"): hook_type,
            bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᦡ"): hook_name
        }
        store[bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᦢ")].append(uuid)
        bstack1ll111ll1ll_opy_ = node.nodeid
        if hook_type == bstack1lll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᦣ"):
            if not _11ll1111ll_opy_.get(bstack1ll111ll1ll_opy_, None):
                _11ll1111ll_opy_[bstack1ll111ll1ll_opy_] = {bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᦤ"): []}
            _11ll1111ll_opy_[bstack1ll111ll1ll_opy_][bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᦥ")].append(bstack11l1ll11l1_opy_[bstack1lll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᦦ")])
        _11ll1111ll_opy_[bstack1ll111ll1ll_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࠪᦧ") + hook_name] = bstack11l1ll11l1_opy_
        bstack1ll11l11lll_opy_(node, bstack11l1ll11l1_opy_, bstack1lll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᦨ"))
    elif event == bstack1lll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᦩ"):
        bstack11llll111l_opy_ = node.nodeid + bstack1lll1l_opy_ (u"ࠫ࠲࠭ᦪ") + hook_name
        _11ll1111ll_opy_[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᦫ")] = bstack11l111ll1_opy_()
        bstack1ll111l1lll_opy_(_11ll1111ll_opy_[bstack11llll111l_opy_][bstack1lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᦬")])
        bstack1ll11l11lll_opy_(node, _11ll1111ll_opy_[bstack11llll111l_opy_], bstack1lll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ᦭"), bstack1ll111lll11_opy_=bstack1ll11l11111_opy_)
def bstack1ll111l1ll1_opy_():
    global bstack1ll111lllll_opy_
    if bstack11ll1111_opy_():
        bstack1ll111lllll_opy_ = bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ᦮")
    else:
        bstack1ll111lllll_opy_ = bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᦯")
@bstack1111ll111_opy_.bstack1ll1l1l1ll1_opy_
def bstack1ll11l111ll_opy_():
    bstack1ll111l1ll1_opy_()
    if bstack11lllll1l_opy_():
        bstack111lll1l_opy_(bstack1l11l1ll11_opy_)
    try:
        bstack1111111111_opy_(bstack1ll11l1111l_opy_)
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᦰ").format(e))
bstack1ll11l111ll_opy_()