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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111111ll11_opy_, bstack1ll1111l11_opy_, bstack1ll111lll1_opy_, bstack111ll1l11_opy_, \
    bstack11111l1111_opy_
def bstack1l11lllll1_opy_(bstack1ll1llll1l1_opy_):
    for driver in bstack1ll1llll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1111l111_opy_(driver, status, reason=bstack1lll1l_opy_ (u"࠭ࠧᗭ")):
    bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
    if bstack1l1l111l_opy_.bstack11l1l111l1_opy_():
        return
    bstack1llll1l1ll_opy_ = bstack11l1l1l11_opy_(bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᗮ"), bstack1lll1l_opy_ (u"ࠨࠩᗯ"), status, reason, bstack1lll1l_opy_ (u"ࠩࠪᗰ"), bstack1lll1l_opy_ (u"ࠪࠫᗱ"))
    driver.execute_script(bstack1llll1l1ll_opy_)
def bstack1ll1l11ll1_opy_(page, status, reason=bstack1lll1l_opy_ (u"ࠫࠬᗲ")):
    try:
        if page is None:
            return
        bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
        if bstack1l1l111l_opy_.bstack11l1l111l1_opy_():
            return
        bstack1llll1l1ll_opy_ = bstack11l1l1l11_opy_(bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᗳ"), bstack1lll1l_opy_ (u"࠭ࠧᗴ"), status, reason, bstack1lll1l_opy_ (u"ࠧࠨᗵ"), bstack1lll1l_opy_ (u"ࠨࠩᗶ"))
        page.evaluate(bstack1lll1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᗷ"), bstack1llll1l1ll_opy_)
    except Exception as e:
        print(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣᗸ"), e)
def bstack11l1l1l11_opy_(type, name, status, reason, bstack1l1l1ll111_opy_, bstack1l11l1lll1_opy_):
    bstack11l1l111_opy_ = {
        bstack1lll1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫᗹ"): type,
        bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᗺ"): {}
    }
    if type == bstack1lll1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᗻ"):
        bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᗼ")][bstack1lll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᗽ")] = bstack1l1l1ll111_opy_
        bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗾ")][bstack1lll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᗿ")] = json.dumps(str(bstack1l11l1lll1_opy_))
    if type == bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᘀ"):
        bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᘁ")][bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᘂ")] = name
    if type == bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᘃ"):
        bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᘄ")][bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᘅ")] = status
        if status == bstack1lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᘆ") and str(reason) != bstack1lll1l_opy_ (u"ࠦࠧᘇ"):
            bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᘈ")][bstack1lll1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᘉ")] = json.dumps(str(reason))
    bstack1111lll1_opy_ = bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᘊ").format(json.dumps(bstack11l1l111_opy_))
    return bstack1111lll1_opy_
def bstack11111ll11_opy_(url, config, logger, bstack1ll11l1ll_opy_=False):
    hostname = bstack1ll1111l11_opy_(url)
    is_private = bstack111ll1l11_opy_(hostname)
    try:
        if is_private or bstack1ll11l1ll_opy_:
            file_path = bstack111111ll11_opy_(bstack1lll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᘋ"), bstack1lll1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᘌ"), logger)
            if os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᘍ")) and eval(
                    os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᘎ"))):
                return
            if (bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᘏ") in config and not config[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᘐ")]):
                os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᘑ")] = str(True)
                bstack1ll1llll1ll_opy_ = {bstack1lll1l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᘒ"): hostname}
                bstack11111l1111_opy_(bstack1lll1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᘓ"), bstack1lll1l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᘔ"), bstack1ll1llll1ll_opy_, logger)
    except Exception as e:
        pass
def bstack1l11lll1l_opy_(caps, bstack1ll1llll11l_opy_):
    if bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘕ") in caps:
        caps[bstack1lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘖ")][bstack1lll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᘗ")] = True
        if bstack1ll1llll11l_opy_:
            caps[bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘘ")][bstack1lll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᘙ")] = bstack1ll1llll11l_opy_
    else:
        caps[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᘚ")] = True
        if bstack1ll1llll11l_opy_:
            caps[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᘛ")] = bstack1ll1llll11l_opy_
def bstack1lll111ll1l_opy_(bstack11ll1111l1_opy_):
    bstack1ll1llll111_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᘜ"), bstack1lll1l_opy_ (u"ࠬ࠭ᘝ"))
    if bstack1ll1llll111_opy_ == bstack1lll1l_opy_ (u"࠭ࠧᘞ") or bstack1ll1llll111_opy_ == bstack1lll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᘟ"):
        threading.current_thread().testStatus = bstack11ll1111l1_opy_
    else:
        if bstack11ll1111l1_opy_ == bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᘠ"):
            threading.current_thread().testStatus = bstack11ll1111l1_opy_