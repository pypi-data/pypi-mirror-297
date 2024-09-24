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
import re
from bstack_utils.bstack1ll1l11111_opy_ import bstack1lll111ll1l_opy_
def bstack1lll11l1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᖸ")):
        return bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᖹ")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᖺ")):
        return bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᖻ")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᖼ")):
        return bstack1lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᖽ")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᖾ")):
        return bstack1lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᖿ")
def bstack1lll111ll11_opy_(fixture_name):
    return bool(re.match(bstack1lll1l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᗀ"), fixture_name))
def bstack1lll11ll111_opy_(fixture_name):
    return bool(re.match(bstack1lll1l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᗁ"), fixture_name))
def bstack1lll11l1l11_opy_(fixture_name):
    return bool(re.match(bstack1lll1l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᗂ"), fixture_name))
def bstack1lll111lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᗃ")):
        return bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᗄ"), bstack1lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᗅ")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᗆ")):
        return bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᗇ"), bstack1lll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᗈ")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᗉ")):
        return bstack1lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᗊ"), bstack1lll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᗋ")
    elif fixture_name.startswith(bstack1lll1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᗌ")):
        return bstack1lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᗍ"), bstack1lll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᗎ")
    return None, None
def bstack1lll111llll_opy_(hook_name):
    if hook_name in [bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᗏ"), bstack1lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᗐ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11l1ll1_opy_(hook_name):
    if hook_name in [bstack1lll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᗑ"), bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᗒ")]:
        return bstack1lll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᗓ")
    elif hook_name in [bstack1lll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᗔ"), bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᗕ")]:
        return bstack1lll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᗖ")
    elif hook_name in [bstack1lll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᗗ"), bstack1lll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᗘ")]:
        return bstack1lll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᗙ")
    elif hook_name in [bstack1lll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᗚ"), bstack1lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᗛ")]:
        return bstack1lll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᗜ")
    return hook_name
def bstack1lll11l1l1l_opy_(node, scenario):
    if hasattr(node, bstack1lll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᗝ")):
        parts = node.nodeid.rsplit(bstack1lll1l_opy_ (u"ࠧࡡࠢᗞ"))
        params = parts[-1]
        return bstack1lll1l_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᗟ").format(scenario.name, params)
    return scenario.name
def bstack1lll11l11ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1lll1l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᗠ")):
            examples = list(node.callspec.params[bstack1lll1l_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᗡ")].values())
        return examples
    except:
        return []
def bstack1lll11ll11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11l111l_opy_(report):
    try:
        status = bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᗢ")
        if report.passed or (report.failed and hasattr(report, bstack1lll1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᗣ"))):
            status = bstack1lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᗤ")
        elif report.skipped:
            status = bstack1lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᗥ")
        bstack1lll111ll1l_opy_(status)
    except:
        pass
def bstack1l1l11l1ll_opy_(status):
    try:
        bstack1lll11l1111_opy_ = bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗦ")
        if status == bstack1lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᗧ"):
            bstack1lll11l1111_opy_ = bstack1lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᗨ")
        elif status == bstack1lll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᗩ"):
            bstack1lll11l1111_opy_ = bstack1lll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᗪ")
        bstack1lll111ll1l_opy_(bstack1lll11l1111_opy_)
    except:
        pass
def bstack1lll11l11l1_opy_(item=None, report=None, summary=None, extra=None):
    return