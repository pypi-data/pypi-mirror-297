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
import json
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l111l1ll_opy_ as bstack111lllll11_opy_
from bstack_utils.bstack1l111111l1_opy_ import bstack1l111111l1_opy_
from bstack_utils.helper import bstack11l111ll1_opy_, bstack11ll1ll1ll_opy_, bstack1l11l1l111_opy_, bstack11l111lll1_opy_, bstack111llllll1_opy_, bstack11ll11l1_opy_, get_host_info, bstack11l111l11l_opy_, bstack1l1l11l1_opy_, bstack11ll1l1lll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11ll1l1lll_opy_(class_method=False)
def _11l11l1l11_opy_(driver, bstack11l11lll1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1lll1l_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩ໽"): caps.get(bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ໾"), None),
        bstack1lll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ໿"): bstack11l11lll1l_opy_.get(bstack1lll1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧༀ"), None),
        bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫ༁"): caps.get(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ༂"), None),
        bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ༃"): caps.get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ༄"), None)
    }
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭༅") + str(error))
  return response
def on():
    if os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ༆"), None) is None or os.environ[bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ༇")] == bstack1lll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ༈"):
        return False
    return True
def bstack111llll1l1_opy_(config):
  return config.get(bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭༉"), False) or any([p.get(bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༊"), False) == True for p in config.get(bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ་"), [])])
def bstack11l1lllll_opy_(config, bstack1llllll1l1_opy_):
  try:
    if not bstack1l11l1l111_opy_(config):
      return False
    bstack11l111l111_opy_ = config.get(bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ༌"), False)
    if int(bstack1llllll1l1_opy_) < len(config.get(bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭།"), [])) and config[bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༎")][bstack1llllll1l1_opy_]:
      bstack111lllll1l_opy_ = config[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༏")][bstack1llllll1l1_opy_].get(bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭༐"), None)
    else:
      bstack111lllll1l_opy_ = config.get(bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༑"), None)
    if bstack111lllll1l_opy_ != None:
      bstack11l111l111_opy_ = bstack111lllll1l_opy_
    bstack11l1111111_opy_ = os.getenv(bstack1lll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭༒")) is not None and len(os.getenv(bstack1lll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ༓"))) > 0 and os.getenv(bstack1lll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ༔")) != bstack1lll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ༕")
    return bstack11l111l111_opy_ and bstack11l1111111_opy_
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ༖") + str(error))
  return False
def bstack1l1l1lll11_opy_(test_tags):
  bstack11l11l1l1l_opy_ = os.getenv(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ༗"))
  if bstack11l11l1l1l_opy_ is None:
    return True
  bstack11l11l1l1l_opy_ = json.loads(bstack11l11l1l1l_opy_)
  try:
    include_tags = bstack11l11l1l1l_opy_[bstack1lll1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩ༘ࠬ")] if bstack1lll1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ༙࠭") in bstack11l11l1l1l_opy_ and isinstance(bstack11l11l1l1l_opy_[bstack1lll1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ༚")], list) else []
    exclude_tags = bstack11l11l1l1l_opy_[bstack1lll1l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ༛")] if bstack1lll1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ༜") in bstack11l11l1l1l_opy_ and isinstance(bstack11l11l1l1l_opy_[bstack1lll1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ༝")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨ༞") + str(error))
  return False
def bstack11l1111ll1_opy_(config, bstack11l1111lll_opy_, bstack11l11l1ll1_opy_, bstack11l11l111l_opy_):
  bstack111llll11l_opy_ = bstack11l111lll1_opy_(config)
  bstack11l11l11ll_opy_ = bstack111llllll1_opy_(config)
  if bstack111llll11l_opy_ is None or bstack11l11l11ll_opy_ is None:
    logger.error(bstack1lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ༟"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ༠"), bstack1lll1l_opy_ (u"ࠩࡾࢁࠬ༡")))
    data = {
        bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ༢"): config[bstack1lll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ༣")],
        bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ༤"): config.get(bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༥"), os.path.basename(os.getcwd())),
        bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪ༦"): bstack11l111ll1_opy_(),
        bstack1lll1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭༧"): config.get(bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ༨"), bstack1lll1l_opy_ (u"ࠪࠫ༩")),
        bstack1lll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ༪"): {
            bstack1lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ༫"): bstack11l1111lll_opy_,
            bstack1lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ༬"): bstack11l11l1ll1_opy_,
            bstack1lll1l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ༭"): __version__,
            bstack1lll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ༮"): bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ༯"),
            bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ༰"): bstack1lll1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭༱"),
            bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ༲"): bstack11l11l111l_opy_
        },
        bstack1lll1l_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ༳"): settings,
        bstack1lll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨ༴"): bstack11l111l11l_opy_(),
        bstack1lll1l_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨ༵"): bstack11ll11l1_opy_(),
        bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫ༶"): get_host_info(),
        bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ༷ࠬ"): bstack1l11l1l111_opy_(config)
    }
    headers = {
        bstack1lll1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ༸"): bstack1lll1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ༹"),
    }
    config = {
        bstack1lll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ༺"): (bstack111llll11l_opy_, bstack11l11l11ll_opy_),
        bstack1lll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ༻"): headers
    }
    response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭༼"), bstack111lllll11_opy_ + bstack1lll1l_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩ༽"), data, config)
    bstack11l11111ll_opy_ = response.json()
    if bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ༾")]:
      parsed = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ༿"), bstack1lll1l_opy_ (u"ࠬࢁࡽࠨཀ")))
      parsed[bstack1lll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧཁ")] = bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬག")][bstack1lll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩགྷ")]
      os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪང")] = json.dumps(parsed)
      bstack1l111111l1_opy_.bstack11l11l11l1_opy_(bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨཅ")][bstack1lll1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬཆ")])
      bstack1l111111l1_opy_.bstack11l111l1l1_opy_(bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪཇ")][bstack1lll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ཈")])
      bstack1l111111l1_opy_.store()
      return bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬཉ")][bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ཊ")], bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠩࡧࡥࡹࡧࠧཋ")][bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭ཌ")]
    else:
      logger.error(bstack1lll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬཌྷ") + bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཎ")])
      if bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧཏ")] == bstack1lll1l_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩཐ"):
        for bstack111llll1ll_opy_ in bstack11l11111ll_opy_[bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨད")]:
          logger.error(bstack111llll1ll_opy_[bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪདྷ")])
      return None, None
  except Exception as error:
    logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦན") +  str(error))
    return None, None
def bstack111lllllll_opy_():
  if os.getenv(bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཔ")) is None:
    return {
        bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬཕ"): bstack1lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬབ"),
        bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨབྷ"): bstack1lll1l_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧམ")
    }
  data = {bstack1lll1l_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪཙ"): bstack11l111ll1_opy_()}
  headers = {
      bstack1lll1l_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪཚ"): bstack1lll1l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬཛ") + os.getenv(bstack1lll1l_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥཛྷ")),
      bstack1lll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬཝ"): bstack1lll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪཞ")
  }
  response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"ࠨࡒࡘࡘࠬཟ"), bstack111lllll11_opy_ + bstack1lll1l_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫའ"), data, { bstack1lll1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫཡ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1lll1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧར") + bstack11ll1ll1ll_opy_().isoformat() + bstack1lll1l_opy_ (u"ࠬࡠࠧལ"))
      return {bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ཤ"): bstack1lll1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨཥ"), bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩས"): bstack1lll1l_opy_ (u"ࠩࠪཧ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨཨ") + str(error))
    return {
        bstack1lll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫཀྵ"): bstack1lll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫཪ"),
        bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧཫ"): str(error)
    }
def bstack11ll1l11_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11l1111l11_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨཬ"), {}).get(bstack1lll1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ཭"), caps.get(bstack1lll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ཮"), bstack1lll1l_opy_ (u"ࠪࠫ཯")))
    if bstack11l1111l11_opy_:
      logger.warn(bstack1lll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ཰"))
      return False
    if options:
      bstack11l111llll_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack11l111llll_opy_ = desired_capabilities
    else:
      bstack11l111llll_opy_ = {}
    browser = caps.get(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧཱࠪ"), bstack1lll1l_opy_ (u"ི࠭ࠧ")).lower() or bstack11l111llll_opy_.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩཱིࠬ"), bstack1lll1l_opy_ (u"ࠨུࠩ")).lower()
    if browser != bstack1lll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦཱུࠩ"):
      logger.warn(bstack1lll1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨྲྀ"))
      return False
    browser_version = caps.get(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬཷ")) or caps.get(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧླྀ")) or bstack11l111llll_opy_.get(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧཹ")) or bstack11l111llll_opy_.get(bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨེ"), {}).get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ཻࠩ")) or bstack11l111llll_opy_.get(bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵོࠪ"), {}).get(bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲཽࠬ"))
    if browser_version and browser_version != bstack1lll1l_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫཾ") and int(browser_version.split(bstack1lll1l_opy_ (u"ࠬ࠴ࠧཿ"))[0]) <= 98:
      logger.warn(bstack1lll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠺࠱ྀࠦ"))
      return False
    if not options:
      bstack11l111ll1l_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷཱྀࠬ")) or bstack11l111llll_opy_.get(bstack1lll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ྂ"), {})
      if bstack1lll1l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ྃ") in bstack11l111ll1l_opy_.get(bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ྄"), []):
        logger.warn(bstack1lll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨ྅"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢ྆") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l11l1lll_opy_ = config.get(bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭྇"), {})
    bstack11l11l1lll_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪྈ")] = os.getenv(bstack1lll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ྉ"))
    bstack111llll111_opy_ = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪྊ"), bstack1lll1l_opy_ (u"ࠪࡿࢂ࠭ྋ"))).get(bstack1lll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬྌ"))
    caps[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬྍ")] = True
    if bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧྎ") in caps:
      caps[bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨྏ")][bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨྐ")] = bstack11l11l1lll_opy_
      caps[bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪྑ")][bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪྒ")][bstack1lll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬྒྷ")] = bstack111llll111_opy_
    else:
      caps[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫྔ")] = bstack11l11l1lll_opy_
      caps[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬྕ")][bstack1lll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྖ")] = bstack111llll111_opy_
  except Exception as error:
    logger.debug(bstack1lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤྗ") +  str(error))
def bstack1lllllll11_opy_(driver, bstack11l11l1111_opy_):
  try:
    setattr(driver, bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ྘"), True)
    session = driver.session_id
    if session:
      bstack11l111ll11_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l111ll11_opy_ = False
      bstack11l111ll11_opy_ = url.scheme in [bstack1lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࠣྙ"), bstack1lll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥྚ")]
      if bstack11l111ll11_opy_:
        if bstack11l11l1111_opy_:
          logger.info(bstack1lll1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧྛ"))
      return bstack11l11l1111_opy_
  except Exception as e:
    logger.error(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤྜ") + str(e))
    return False
def bstack1lll1l1l1l_opy_(driver, name, path):
  try:
    bstack11l11111l1_opy_ = {
        bstack1lll1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧྜྷ"): threading.current_thread().current_test_uuid,
        bstack1lll1l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ྞ"): os.environ.get(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧྟ"), bstack1lll1l_opy_ (u"ࠪࠫྠ")),
        bstack1lll1l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨྡ"): os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ྡྷ"), bstack1lll1l_opy_ (u"࠭ࠧྣ"))
    }
    logger.debug(bstack1lll1l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪྤ"))
    logger.debug(driver.execute_async_script(bstack1l111111l1_opy_.perform_scan, {bstack1lll1l_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣྥ"): name}))
    logger.debug(driver.execute_async_script(bstack1l111111l1_opy_.bstack11l1111l1l_opy_, bstack11l11111l1_opy_))
    logger.info(bstack1lll1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧྦ"))
  except Exception as bstack11l111111l_opy_:
    logger.error(bstack1lll1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧྦྷ") + str(path) + bstack1lll1l_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨྨ") + str(bstack11l111111l_opy_))