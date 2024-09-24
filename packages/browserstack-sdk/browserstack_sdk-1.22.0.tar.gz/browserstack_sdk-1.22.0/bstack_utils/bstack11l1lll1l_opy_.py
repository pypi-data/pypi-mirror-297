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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l111l11l_opy_, bstack11ll11l1_opy_, get_host_info, bstack111l1l1ll1_opy_, \
 bstack1l11l1l111_opy_, bstack1ll111lll1_opy_, bstack11ll1l1lll_opy_, bstack1111ll111l_opy_, bstack11l111ll1_opy_
import bstack_utils.bstack1l111lll11_opy_ as bstack1ll111llll_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11l111l1l_opy_
from bstack_utils.percy import bstack1ll111111l_opy_
from bstack_utils.config import Config
bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1ll111111l_opy_()
@bstack11ll1l1lll_opy_(class_method=False)
def bstack1ll1l11ll1l_opy_(bs_config, bstack1l11ll111l_opy_):
  try:
    data = {
        bstack1lll1l_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨᝆ"): bstack1lll1l_opy_ (u"ࠩ࡭ࡷࡴࡴࠧᝇ"),
        bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩᝈ"): bs_config.get(bstack1lll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᝉ"), bstack1lll1l_opy_ (u"ࠬ࠭ᝊ")),
        bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝋ"): bs_config.get(bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᝌ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᝍ"): bs_config.get(bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᝎ")),
        bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᝏ"): bs_config.get(bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᝐ"), bstack1lll1l_opy_ (u"ࠬ࠭ᝑ")),
        bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᝒ"): bstack11l111ll1_opy_(),
        bstack1lll1l_opy_ (u"ࠧࡵࡣࡪࡷࠬᝓ"): bstack111l1l1ll1_opy_(bs_config),
        bstack1lll1l_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ᝔"): get_host_info(),
        bstack1lll1l_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ᝕"): bstack11ll11l1_opy_(),
        bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᝖"): os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ᝗")),
        bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ᝘"): os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ᝙"), False),
        bstack1lll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ᝚"): bstack11l111l11l_opy_(),
        bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᝛"): bstack1ll1l111l11_opy_(),
        bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭᝜"): bstack1ll11llll11_opy_(bstack1l11ll111l_opy_),
        bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ᝝"): bstack11llll1ll_opy_(bs_config, bstack1l11ll111l_opy_.get(bstack1lll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ᝞"), bstack1lll1l_opy_ (u"ࠬ࠭᝟"))),
        bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᝠ"): bstack1l11l1l111_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1lll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣᝡ").format(str(error)))
    return None
def bstack1ll11llll11_opy_(framework):
  return {
    bstack1lll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᝢ"): framework.get(bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪᝣ"), bstack1lll1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᝤ")),
    bstack1lll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᝥ"): framework.get(bstack1lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᝦ")),
    bstack1lll1l_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᝧ"): framework.get(bstack1lll1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᝨ")),
    bstack1lll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᝩ"): bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᝪ"),
    bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᝫ"): framework.get(bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᝬ"))
  }
def bstack11llll1ll_opy_(bs_config, framework):
  bstack1llll11111_opy_ = False
  bstack1l111l11l1_opy_ = False
  if bstack1lll1l_opy_ (u"ࠬࡧࡰࡱࠩ᝭") in bs_config:
    bstack1llll11111_opy_ = True
  else:
    bstack1l111l11l1_opy_ = True
  bstack1l1ll1lll1_opy_ = {
    bstack1lll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᝮ"): bstack11l111l1l_opy_.bstack1ll1l1111ll_opy_(bs_config, framework),
    bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝯ"): bstack1ll111llll_opy_.bstack111llll1l1_opy_(bs_config),
    bstack1lll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᝰ"): bs_config.get(bstack1lll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ᝱"), False),
    bstack1lll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᝲ"): bstack1l111l11l1_opy_,
    bstack1lll1l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᝳ"): bstack1llll11111_opy_
  }
  return bstack1l1ll1lll1_opy_
@bstack11ll1l1lll_opy_(class_method=False)
def bstack1ll1l111l11_opy_():
  try:
    bstack1ll11lll1ll_opy_ = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᝴"), bstack1lll1l_opy_ (u"࠭ࡻࡾࠩ᝵")))
    return {
        bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ᝶"): bstack1ll11lll1ll_opy_
    }
  except Exception as error:
    logger.error(bstack1lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ᝷").format(str(error)))
    return {}
def bstack1ll1ll111l1_opy_(array, bstack1ll1l11111l_opy_, bstack1ll11llll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l11111l_opy_]
    result[key] = o[bstack1ll11llll1l_opy_]
  return result
def bstack1ll1l111ll1_opy_(bstack1lll111l1l_opy_=bstack1lll1l_opy_ (u"ࠩࠪ᝸")):
  bstack1ll1l111111_opy_ = bstack1ll111llll_opy_.on()
  bstack1ll11llllll_opy_ = bstack11l111l1l_opy_.on()
  bstack1ll11lllll1_opy_ = percy.bstack11ll1lll_opy_()
  if bstack1ll11lllll1_opy_ and not bstack1ll11llllll_opy_ and not bstack1ll1l111111_opy_:
    return bstack1lll111l1l_opy_ not in [bstack1lll1l_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ᝹"), bstack1lll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ᝺")]
  elif bstack1ll1l111111_opy_ and not bstack1ll11llllll_opy_:
    return bstack1lll111l1l_opy_ not in [bstack1lll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᝻"), bstack1lll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᝼"), bstack1lll1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᝽")]
  return bstack1ll1l111111_opy_ or bstack1ll11llllll_opy_ or bstack1ll11lllll1_opy_
@bstack11ll1l1lll_opy_(class_method=False)
def bstack1ll1l1l1111_opy_(bstack1lll111l1l_opy_, test=None):
  bstack1ll1l1111l1_opy_ = bstack1ll111llll_opy_.on()
  if not bstack1ll1l1111l1_opy_ or bstack1lll111l1l_opy_ not in [bstack1lll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᝾")] or test == None:
    return None
  return {
    bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᝿"): bstack1ll1l1111l1_opy_ and bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩក"), None) == True and bstack1ll111llll_opy_.bstack1l1l1lll11_opy_(test[bstack1lll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩខ")])
  }