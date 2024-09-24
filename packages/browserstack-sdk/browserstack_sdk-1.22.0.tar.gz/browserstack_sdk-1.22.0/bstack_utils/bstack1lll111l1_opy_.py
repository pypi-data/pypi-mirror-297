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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111l1lll11_opy_, bstack111ll11ll1_opy_
import tempfile
import json
bstack1llllll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠬᒯ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1lll1l_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᒰ"),
      datefmt=bstack1lll1l_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧᒱ"),
      stream=sys.stdout
    )
  return logger
def bstack1llllll1lll_opy_():
  global bstack1llllll1l1l_opy_
  if os.path.exists(bstack1llllll1l1l_opy_):
    os.remove(bstack1llllll1l1l_opy_)
def bstack11llllll1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l1ll11l_opy_(config, log_level):
  bstack1lllll1lll1_opy_ = log_level
  if bstack1lll1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᒲ") in config and config[bstack1lll1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᒳ")] in bstack111l1lll11_opy_:
    bstack1lllll1lll1_opy_ = bstack111l1lll11_opy_[config[bstack1lll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᒴ")]]
  if config.get(bstack1lll1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᒵ"), False):
    logging.getLogger().setLevel(bstack1lllll1lll1_opy_)
    return bstack1lllll1lll1_opy_
  global bstack1llllll1l1l_opy_
  bstack11llllll1l_opy_()
  bstack1lllll1l1ll_opy_ = logging.Formatter(
    fmt=bstack1lll1l_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᒶ"),
    datefmt=bstack1lll1l_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᒷ")
  )
  bstack1llllll1l11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1llllll1l1l_opy_)
  file_handler.setFormatter(bstack1lllll1l1ll_opy_)
  bstack1llllll1l11_opy_.setFormatter(bstack1lllll1l1ll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1llllll1l11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1lll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧᒸ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1llllll1l11_opy_.setLevel(bstack1lllll1lll1_opy_)
  logging.getLogger().addHandler(bstack1llllll1l11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllll1lll1_opy_
def bstack1lllll1ll1l_opy_(config):
  try:
    bstack1lllll1ll11_opy_ = set(bstack111ll11ll1_opy_)
    bstack1llllll1ll1_opy_ = bstack1lll1l_opy_ (u"࠭ࠧᒹ")
    with open(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᒺ")) as bstack1lllll1l1l1_opy_:
      bstack1lllll1llll_opy_ = bstack1lllll1l1l1_opy_.read()
      bstack1llllll1ll1_opy_ = re.sub(bstack1lll1l_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᒻ"), bstack1lll1l_opy_ (u"ࠩࠪᒼ"), bstack1lllll1llll_opy_, flags=re.M)
      bstack1llllll1ll1_opy_ = re.sub(
        bstack1lll1l_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭ᒽ") + bstack1lll1l_opy_ (u"ࠫࢁ࠭ᒾ").join(bstack1lllll1ll11_opy_) + bstack1lll1l_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᒿ"),
        bstack1lll1l_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᓀ"),
        bstack1llllll1ll1_opy_, flags=re.M | re.I
      )
    def bstack1llllll11l1_opy_(dic):
      bstack1llllll11ll_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lllll1ll11_opy_:
          bstack1llllll11ll_opy_[key] = bstack1lll1l_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᓁ")
        else:
          if isinstance(value, dict):
            bstack1llllll11ll_opy_[key] = bstack1llllll11l1_opy_(value)
          else:
            bstack1llllll11ll_opy_[key] = value
      return bstack1llllll11ll_opy_
    bstack1llllll11ll_opy_ = bstack1llllll11l1_opy_(config)
    return {
      bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᓂ"): bstack1llllll1ll1_opy_,
      bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᓃ"): json.dumps(bstack1llllll11ll_opy_)
    }
  except Exception as e:
    return {}
def bstack1l11llll_opy_(config):
  global bstack1llllll1l1l_opy_
  try:
    if config.get(bstack1lll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᓄ"), False):
      return
    uuid = os.getenv(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᓅ"))
    if not uuid or uuid == bstack1lll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᓆ"):
      return
    bstack1llllll111l_opy_ = [bstack1lll1l_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩᓇ"), bstack1lll1l_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨᓈ"), bstack1lll1l_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩᓉ"), bstack1llllll1l1l_opy_]
    bstack11llllll1l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨᓊ") + uuid + bstack1lll1l_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫᓋ"))
    with tarfile.open(output_file, bstack1lll1l_opy_ (u"ࠦࡼࡀࡧࡻࠤᓌ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llllll111l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll1ll1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llllll1111_opy_ = data.encode()
        tarinfo.size = len(bstack1llllll1111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llllll1111_opy_))
    bstack1ll1l1l1ll_opy_ = MultipartEncoder(
      fields= {
        bstack1lll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪᓍ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1lll1l_opy_ (u"࠭ࡲࡣࠩᓎ")), bstack1lll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬᓏ")),
        bstack1lll1l_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᓐ"): uuid
      }
    )
    response = requests.post(
      bstack1lll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡹࡵࡲ࡯ࡢࡦ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦᓑ"),
      data=bstack1ll1l1l1ll_opy_,
      headers={bstack1lll1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᓒ"): bstack1ll1l1l1ll_opy_.content_type},
      auth=(config[bstack1lll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᓓ")], config[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᓔ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1lll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬᓕ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1lll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭ᓖ") + str(e))
  finally:
    try:
      bstack1llllll1lll_opy_()
    except:
      pass