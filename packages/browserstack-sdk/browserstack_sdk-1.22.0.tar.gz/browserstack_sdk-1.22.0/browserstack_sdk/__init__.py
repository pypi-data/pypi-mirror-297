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
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1l1ll1lll_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1l1l1l1l_opy_ import bstack1l1l1111ll_opy_
import time
import requests
def bstack1ll1l11l11_opy_():
  global CONFIG
  headers = {
        bstack1lll1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1lll1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1l1111_opy_(CONFIG, bstack1llllllll_opy_)
  try:
    response = requests.get(bstack1llllllll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l111llll1_opy_ = response.json()[bstack1lll1l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11lll111l_opy_.format(response.json()))
      return bstack1l111llll1_opy_
    else:
      logger.debug(bstack1l1l1lll1l_opy_.format(bstack1lll1l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l1l1lll1l_opy_.format(e))
def bstack1l1ll1l11_opy_(hub_url):
  global CONFIG
  url = bstack1lll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1lll1l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1lll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1lll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1l1111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1ll111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l1l11l_opy_.format(hub_url, e))
def bstack1l1l1111l_opy_():
  try:
    global bstack1l1lll1l_opy_
    bstack1l111llll1_opy_ = bstack1ll1l11l11_opy_()
    bstack1l1l1l111l_opy_ = []
    results = []
    for bstack11ll1l1l_opy_ in bstack1l111llll1_opy_:
      bstack1l1l1l111l_opy_.append(bstack1lll1lll1l_opy_(target=bstack1l1ll1l11_opy_,args=(bstack11ll1l1l_opy_,)))
    for t in bstack1l1l1l111l_opy_:
      t.start()
    for t in bstack1l1l1l111l_opy_:
      results.append(t.join())
    bstack1lllll1lll_opy_ = {}
    for item in results:
      hub_url = item[bstack1lll1l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1lll1l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1lllll1lll_opy_[hub_url] = latency
    bstack1l111lll_opy_ = min(bstack1lllll1lll_opy_, key= lambda x: bstack1lllll1lll_opy_[x])
    bstack1l1lll1l_opy_ = bstack1l111lll_opy_
    logger.debug(bstack11111l11l_opy_.format(bstack1l111lll_opy_))
  except Exception as e:
    logger.debug(bstack1lllll11l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1lll111l1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1lll1ll1l1_opy_, bstack1l1l11l1_opy_, bstack1l11lll1_opy_, bstack1ll111lll1_opy_, bstack1l11l1l111_opy_, \
  Notset, bstack1lll1lll1_opy_, \
  bstack1lll1ll1_opy_, bstack111ll111_opy_, bstack1llll11ll_opy_, bstack11ll11l1_opy_, bstack11ll1111_opy_, bstack11lllll1l_opy_, \
  bstack11lllll11_opy_, \
  bstack1llll111l_opy_, bstack1llll11ll1_opy_, bstack1l1l1ll11_opy_, bstack1l1l1ll1l1_opy_, \
  bstack1lll1l1ll_opy_, bstack1l11ll1lll_opy_, bstack1l1lllll1l_opy_, bstack1ll1l1ll_opy_
from bstack_utils.bstack111lll11_opy_ import bstack11ll1ll1_opy_
from bstack_utils.bstack1l1111ll_opy_ import bstack111lll1l_opy_
from bstack_utils.bstack1ll1l11111_opy_ import bstack1l1111l111_opy_, bstack1ll1l11ll1_opy_
from bstack_utils.bstack11lll1l1_opy_ import bstack1111ll111_opy_
from bstack_utils.bstack1l11llll11_opy_ import bstack11l111l1l_opy_
from bstack_utils.bstack1l111111l1_opy_ import bstack1l111111l1_opy_
from bstack_utils.proxy import bstack1llll111ll_opy_, bstack1l1l1111_opy_, bstack1l1l1lll1_opy_, bstack1llll1ll11_opy_
import bstack_utils.bstack1l111lll11_opy_ as bstack1ll111llll_opy_
from browserstack_sdk.bstack1ll1llll11_opy_ import *
from browserstack_sdk.bstack1ll1lll11l_opy_ import *
from bstack_utils.bstack1l111l1ll_opy_ import bstack1l1l11l1ll_opy_
from browserstack_sdk.bstack1l1ll11ll1_opy_ import *
import bstack_utils.bstack11l1lll1l_opy_ as bstack1llllllll1_opy_
import bstack_utils.bstack11l11lll_opy_ as bstack111111lll_opy_
bstack111lll111_opy_ = bstack1lll1l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1l11l1l1ll_opy_ = bstack1lll1l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1ll11111l1_opy_ = None
CONFIG = {}
bstack11ll1llll_opy_ = {}
bstack111l1ll1_opy_ = {}
bstack1l11ll11l_opy_ = None
bstack111ll111l_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack1llll11lll_opy_ = -1
bstack1llll11l1l_opy_ = 0
bstack1lll111ll1_opy_ = bstack1l1l1llll1_opy_
bstack11lll11ll_opy_ = 1
bstack1lll111111_opy_ = False
bstack1l1l1l111_opy_ = False
bstack1ll1lllll_opy_ = bstack1lll1l_opy_ (u"ࠨࠩࢂ")
bstack11lll1111_opy_ = bstack1lll1l_opy_ (u"ࠩࠪࢃ")
bstack1111ll11l_opy_ = False
bstack1lll111l_opy_ = True
bstack1ll1l1l11_opy_ = bstack1lll1l_opy_ (u"ࠪࠫࢄ")
bstack111ll1ll_opy_ = []
bstack1l1lll1l_opy_ = bstack1lll1l_opy_ (u"ࠫࠬࢅ")
bstack1ll1lll111_opy_ = False
bstack1ll1l11l1l_opy_ = None
bstack1lll11l111_opy_ = None
bstack1lll1111l_opy_ = None
bstack111l1l1l1_opy_ = -1
bstack1l1lll11_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠬࢄࠧࢆ")), bstack1lll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1lll1l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1l1llllll_opy_ = 0
bstack1l1l1ll1_opy_ = 0
bstack1l1l1l1ll1_opy_ = []
bstack1llllll11_opy_ = []
bstack1l1l11l11l_opy_ = []
bstack11ll111ll_opy_ = []
bstack1lll11l1l_opy_ = bstack1lll1l_opy_ (u"ࠨࠩࢉ")
bstack1l1lll1l1l_opy_ = bstack1lll1l_opy_ (u"ࠩࠪࢊ")
bstack111l11l1l_opy_ = False
bstack1lll1l1l_opy_ = False
bstack1ll1ll1l_opy_ = {}
bstack1lll11l11l_opy_ = None
bstack11l1l11ll_opy_ = None
bstack1ll1lllll1_opy_ = None
bstack1ll1l1l1_opy_ = None
bstack1llll11l_opy_ = None
bstack11ll1l111_opy_ = None
bstack1ll111l1_opy_ = None
bstack11l11lll1_opy_ = None
bstack1ll11ll1_opy_ = None
bstack111111111_opy_ = None
bstack1l1l1llll_opy_ = None
bstack1l1l111l1l_opy_ = None
bstack1ll1l1111l_opy_ = None
bstack1ll11l1l11_opy_ = None
bstack11l1l1ll1_opy_ = None
bstack11l1l1ll_opy_ = None
bstack1l11111l1l_opy_ = None
bstack1l1l11ll1l_opy_ = None
bstack1111l1l11_opy_ = None
bstack1111111ll_opy_ = None
bstack1lll1l1ll1_opy_ = None
bstack11ll11l1l_opy_ = None
bstack1ll1l11ll_opy_ = False
bstack11l1111ll_opy_ = bstack1lll1l_opy_ (u"ࠥࠦࢋ")
logger = bstack1lll111l1_opy_.get_logger(__name__, bstack1lll111ll1_opy_)
bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
percy = bstack1ll111111l_opy_()
bstack1ll11l11ll_opy_ = bstack1l1l1111ll_opy_()
bstack11l1llll1_opy_ = bstack1l1ll11ll1_opy_()
def bstack1ll111lll_opy_():
  global CONFIG
  global bstack111l11l1l_opy_
  global bstack1l1l111l_opy_
  bstack1111111l1_opy_ = bstack1ll11ll1l_opy_(CONFIG)
  if bstack1l11l1l111_opy_(CONFIG):
    if (bstack1lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1111111l1_opy_ and str(bstack1111111l1_opy_[bstack1lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack1lll1l_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
      bstack111l11l1l_opy_ = True
    bstack1l1l111l_opy_.bstack1l1ll1l1_opy_(bstack1111111l1_opy_.get(bstack1lll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
  else:
    bstack111l11l1l_opy_ = True
    bstack1l1l111l_opy_.bstack1l1ll1l1_opy_(True)
def bstack11111l1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1111l1l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11l11ll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1lll1l_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1lll1l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll1l1l11_opy_
      bstack1ll1l1l11_opy_ += bstack1lll1l_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1l1ll1l111_opy_ = re.compile(bstack1lll1l_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1l1llllll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1ll1l111_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1lll1l_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1lll1l_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1llll11l1_opy_():
  bstack111l1llll_opy_ = bstack1l11l11ll1_opy_()
  if bstack111l1llll_opy_ and os.path.exists(os.path.abspath(bstack111l1llll_opy_)):
    fileName = bstack111l1llll_opy_
  if bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack1l1lll1_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1lll1_opy_ = bstack1lll1l_opy_ (u"࢛ࠬ࠭")
  bstack1ll1111lll_opy_ = os.getcwd()
  bstack1l1l1l11ll_opy_ = bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack111lllll1_opy_ = bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack1l1lll1_opy_)) and bstack1ll1111lll_opy_ != bstack1lll1l_opy_ (u"ࠣࠤ࢞"):
    bstack1l1lll1_opy_ = os.path.join(bstack1ll1111lll_opy_, bstack1l1l1l11ll_opy_)
    if not os.path.exists(bstack1l1lll1_opy_):
      bstack1l1lll1_opy_ = os.path.join(bstack1ll1111lll_opy_, bstack111lllll1_opy_)
    if bstack1ll1111lll_opy_ != os.path.dirname(bstack1ll1111lll_opy_):
      bstack1ll1111lll_opy_ = os.path.dirname(bstack1ll1111lll_opy_)
    else:
      bstack1ll1111lll_opy_ = bstack1lll1l_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack1l1lll1_opy_):
    bstack11ll1l11l_opy_(
      bstack1ll11l11l1_opy_.format(os.getcwd()))
  try:
    with open(bstack1l1lll1_opy_, bstack1lll1l_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1lll1l_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1l1ll1l111_opy_)
      yaml.add_constructor(bstack1lll1l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1l1llllll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l1lll1_opy_, bstack1lll1l_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11ll1l11l_opy_(bstack111111l1l_opy_.format(str(exc)))
def bstack1l11lll111_opy_(config):
  bstack1ll1l11lll_opy_ = bstack111l1lll_opy_(config)
  for option in list(bstack1ll1l11lll_opy_):
    if option.lower() in bstack1l1ll1111l_opy_ and option != bstack1l1ll1111l_opy_[option.lower()]:
      bstack1ll1l11lll_opy_[bstack1l1ll1111l_opy_[option.lower()]] = bstack1ll1l11lll_opy_[option]
      del bstack1ll1l11lll_opy_[option]
  return config
def bstack1l11ll1ll1_opy_():
  global bstack111l1ll1_opy_
  for key, bstack111111ll1_opy_ in bstack11l11l1l1_opy_.items():
    if isinstance(bstack111111ll1_opy_, list):
      for var in bstack111111ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack111l1ll1_opy_[key] = os.environ[var]
          break
    elif bstack111111ll1_opy_ in os.environ and os.environ[bstack111111ll1_opy_] and str(os.environ[bstack111111ll1_opy_]).strip():
      bstack111l1ll1_opy_[key] = os.environ[bstack111111ll1_opy_]
  if bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack111l1ll1_opy_[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack111l1ll1_opy_[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1lll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1ll1ll11_opy_():
  global bstack11ll1llll_opy_
  global bstack1ll1l1l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack11ll1llll_opy_[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack11ll1llll_opy_[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1lll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1llll1l1l1_opy_ in bstack1ll11111_opy_.items():
    if isinstance(bstack1llll1l1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1llll1l1l1_opy_:
          if idx < len(sys.argv) and bstack1lll1l_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack11ll1llll_opy_:
            bstack11ll1llll_opy_[key] = sys.argv[idx + 1]
            bstack1ll1l1l11_opy_ += bstack1lll1l_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1lll1l_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1lll1l_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1llll1l1l1_opy_.lower() == val.lower() and not key in bstack11ll1llll_opy_:
          bstack11ll1llll_opy_[key] = sys.argv[idx + 1]
          bstack1ll1l1l11_opy_ += bstack1lll1l_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1llll1l1l1_opy_ + bstack1lll1l_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1ll1ll_opy_(config):
  bstack1llll1ll1l_opy_ = config.keys()
  for bstack1lll1l11l_opy_, bstack1lll1ll11_opy_ in bstack1llll1l111_opy_.items():
    if bstack1lll1ll11_opy_ in bstack1llll1ll1l_opy_:
      config[bstack1lll1l11l_opy_] = config[bstack1lll1ll11_opy_]
      del config[bstack1lll1ll11_opy_]
  for bstack1lll1l11l_opy_, bstack1lll1ll11_opy_ in bstack1lll1ll1l_opy_.items():
    if isinstance(bstack1lll1ll11_opy_, list):
      for bstack1l11l1ll_opy_ in bstack1lll1ll11_opy_:
        if bstack1l11l1ll_opy_ in bstack1llll1ll1l_opy_:
          config[bstack1lll1l11l_opy_] = config[bstack1l11l1ll_opy_]
          del config[bstack1l11l1ll_opy_]
          break
    elif bstack1lll1ll11_opy_ in bstack1llll1ll1l_opy_:
      config[bstack1lll1l11l_opy_] = config[bstack1lll1ll11_opy_]
      del config[bstack1lll1ll11_opy_]
  for bstack1l11l1ll_opy_ in list(config):
    for bstack11llllll_opy_ in bstack1l11111l11_opy_:
      if bstack1l11l1ll_opy_.lower() == bstack11llllll_opy_.lower() and bstack1l11l1ll_opy_ != bstack11llllll_opy_:
        config[bstack11llllll_opy_] = config[bstack1l11l1ll_opy_]
        del config[bstack1l11l1ll_opy_]
  bstack1l1l111111_opy_ = [{}]
  if not config.get(bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ")):
    config[bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")] = [{}]
  bstack1l1l111111_opy_ = config[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ")]
  for platform in bstack1l1l111111_opy_:
    for bstack1l11l1ll_opy_ in list(platform):
      for bstack11llllll_opy_ in bstack1l11111l11_opy_:
        if bstack1l11l1ll_opy_.lower() == bstack11llllll_opy_.lower() and bstack1l11l1ll_opy_ != bstack11llllll_opy_:
          platform[bstack11llllll_opy_] = platform[bstack1l11l1ll_opy_]
          del platform[bstack1l11l1ll_opy_]
  for bstack1lll1l11l_opy_, bstack1lll1ll11_opy_ in bstack1lll1ll1l_opy_.items():
    for platform in bstack1l1l111111_opy_:
      if isinstance(bstack1lll1ll11_opy_, list):
        for bstack1l11l1ll_opy_ in bstack1lll1ll11_opy_:
          if bstack1l11l1ll_opy_ in platform:
            platform[bstack1lll1l11l_opy_] = platform[bstack1l11l1ll_opy_]
            del platform[bstack1l11l1ll_opy_]
            break
      elif bstack1lll1ll11_opy_ in platform:
        platform[bstack1lll1l11l_opy_] = platform[bstack1lll1ll11_opy_]
        del platform[bstack1lll1ll11_opy_]
  for bstack1lllll11_opy_ in bstack1lll1ll111_opy_:
    if bstack1lllll11_opy_ in config:
      if not bstack1lll1ll111_opy_[bstack1lllll11_opy_] in config:
        config[bstack1lll1ll111_opy_[bstack1lllll11_opy_]] = {}
      config[bstack1lll1ll111_opy_[bstack1lllll11_opy_]].update(config[bstack1lllll11_opy_])
      del config[bstack1lllll11_opy_]
  for platform in bstack1l1l111111_opy_:
    for bstack1lllll11_opy_ in bstack1lll1ll111_opy_:
      if bstack1lllll11_opy_ in list(platform):
        if not bstack1lll1ll111_opy_[bstack1lllll11_opy_] in platform:
          platform[bstack1lll1ll111_opy_[bstack1lllll11_opy_]] = {}
        platform[bstack1lll1ll111_opy_[bstack1lllll11_opy_]].update(platform[bstack1lllll11_opy_])
        del platform[bstack1lllll11_opy_]
  config = bstack1l11lll111_opy_(config)
  return config
def bstack11l11ll11_opy_(config):
  global bstack11lll1111_opy_
  if bstack1l11l1l111_opy_(config) and bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ") in config and str(config[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ")]).lower() != bstack1lll1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢸ"):
    if not bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ") in config:
      config[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ")] = {}
    if not config[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")].get(bstack1lll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧࢼ")) and not bstack1lll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack11l111ll1_opy_ = datetime.datetime.now()
      bstack1ll1lll1ll_opy_ = bstack11l111ll1_opy_.strftime(bstack1lll1l_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack1l1l11l1l_opy_ = bstack1lll1l_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1lll1l_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1ll1lll1ll_opy_, hostname, bstack1l1l11l1l_opy_)
      config[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack1lll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack11lll1111_opy_ = config[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")].get(bstack1lll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ"))
  return config
def bstack11l1111l1_opy_():
  bstack11ll1111l_opy_ =  bstack11ll11l1_opy_()[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack11ll1111l_opy_ if bstack11ll1111l_opy_ else -1
def bstack1l1l1l1ll_opy_(bstack11ll1111l_opy_):
  global CONFIG
  if not bstack1lll1l_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack1lll1l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack11ll1111l_opy_)
  )
def bstack1l111111l_opy_():
  global CONFIG
  if not bstack1lll1l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack11l111ll1_opy_ = datetime.datetime.now()
  bstack1ll1lll1ll_opy_ = bstack11l111ll1_opy_.strftime(bstack1lll1l_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack1lll1l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1ll1lll1ll_opy_
  )
def bstack1l11ll1l_opy_():
  global CONFIG
  if bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack1lll1l_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack1lll1l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack1l111111l_opy_()
    os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack1lll1l_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack11ll1111l_opy_ = bstack1lll1l_opy_ (u"ࠩࠪࣞ")
  bstack1l1ll1l1l_opy_ = bstack11l1111l1_opy_()
  if bstack1l1ll1l1l_opy_ != -1:
    bstack11ll1111l_opy_ = bstack1lll1l_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1l1ll1l1l_opy_)
  if bstack11ll1111l_opy_ == bstack1lll1l_opy_ (u"ࠫࠬ࣠"):
    bstack1l1111l1l_opy_ = bstack1l1111l1_opy_(CONFIG[bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack1l1111l1l_opy_ != -1:
      bstack11ll1111l_opy_ = str(bstack1l1111l1l_opy_)
  if bstack11ll1111l_opy_:
    bstack1l1l1l1ll_opy_(bstack11ll1111l_opy_)
    os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack1lll1l1l11_opy_(bstack1ll1l1ll11_opy_, bstack1l1l1l1l11_opy_, path):
  bstack11111ll1_opy_ = {
    bstack1lll1l_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack1l1l1l1l11_opy_
  }
  if os.path.exists(path):
    bstack1l11111ll1_opy_ = json.load(open(path, bstack1lll1l_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack1l11111ll1_opy_ = {}
  bstack1l11111ll1_opy_[bstack1ll1l1ll11_opy_] = bstack11111ll1_opy_
  with open(path, bstack1lll1l_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack1l11111ll1_opy_, outfile)
def bstack1l1111l1_opy_(bstack1ll1l1ll11_opy_):
  bstack1ll1l1ll11_opy_ = str(bstack1ll1l1ll11_opy_)
  bstack111l111l_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠫࢃ࠭ࣧ")), bstack1lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack111l111l_opy_):
      os.makedirs(bstack111l111l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"࠭ࡾࠨࣩ")), bstack1lll1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack1lll1l_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1lll1l_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack1lll1l_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1lll1l_opy_ (u"ࠫࡷ࣮࠭")) as bstack1l111l111l_opy_:
      bstack11llll1l1_opy_ = json.load(bstack1l111l111l_opy_)
    if bstack1ll1l1ll11_opy_ in bstack11llll1l1_opy_:
      bstack1l1l111l1_opy_ = bstack11llll1l1_opy_[bstack1ll1l1ll11_opy_][bstack1lll1l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack11llll111_opy_ = int(bstack1l1l111l1_opy_) + 1
      bstack1lll1l1l11_opy_(bstack1ll1l1ll11_opy_, bstack11llll111_opy_, file_path)
      return bstack11llll111_opy_
    else:
      bstack1lll1l1l11_opy_(bstack1ll1l1ll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1llll1l1_opy_.format(str(e)))
    return -1
def bstack1l111l1lll_opy_(config):
  if not config[bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack111l1lll1_opy_(config, index=0):
  global bstack1111ll11l_opy_
  bstack111111l1_opy_ = {}
  caps = bstack1l1lll1111_opy_ + bstack1l1111l1ll_opy_
  if bstack1111ll11l_opy_:
    caps += bstack11l111l1_opy_
  for key in config:
    if key in caps + [bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack111111l1_opy_[key] = config[key]
  if bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack11llll11l_opy_ in config[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack11llll11l_opy_ in caps:
        continue
      bstack111111l1_opy_[bstack11llll11l_opy_] = config[bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index][bstack11llll11l_opy_]
  bstack111111l1_opy_[bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࣶࠧ")] = socket.gethostname()
  if bstack1lll1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ") in bstack111111l1_opy_:
    del (bstack111111l1_opy_[bstack1lll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ")])
  return bstack111111l1_opy_
def bstack1lll11lll_opy_(config):
  global bstack1111ll11l_opy_
  bstack1l1l11llll_opy_ = {}
  caps = bstack1l1111l1ll_opy_
  if bstack1111ll11l_opy_:
    caps += bstack11l111l1_opy_
  for key in caps:
    if key in config:
      bstack1l1l11llll_opy_[key] = config[key]
  return bstack1l1l11llll_opy_
def bstack11lll1ll_opy_(bstack111111l1_opy_, bstack1l1l11llll_opy_):
  bstack1l111l111_opy_ = {}
  for key in bstack111111l1_opy_.keys():
    if key in bstack1llll1l111_opy_:
      bstack1l111l111_opy_[bstack1llll1l111_opy_[key]] = bstack111111l1_opy_[key]
    else:
      bstack1l111l111_opy_[key] = bstack111111l1_opy_[key]
  for key in bstack1l1l11llll_opy_:
    if key in bstack1llll1l111_opy_:
      bstack1l111l111_opy_[bstack1llll1l111_opy_[key]] = bstack1l1l11llll_opy_[key]
    else:
      bstack1l111l111_opy_[key] = bstack1l1l11llll_opy_[key]
  return bstack1l111l111_opy_
def bstack1l11lllll_opy_(config, index=0):
  global bstack1111ll11l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1ll11111l_opy_ = bstack1lll1ll1l1_opy_(bstack1ll11ll111_opy_, config, logger)
  bstack1l1l11llll_opy_ = bstack1lll11lll_opy_(config)
  bstack111ll1l1_opy_ = bstack1l1111l1ll_opy_
  bstack111ll1l1_opy_ += bstack111l1111_opy_
  bstack1l1l11llll_opy_ = update(bstack1l1l11llll_opy_, bstack1ll11111l_opy_)
  if bstack1111ll11l_opy_:
    bstack111ll1l1_opy_ += bstack11l111l1_opy_
  if bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ") in config:
    if bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࣺࠧ") in config[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")][index]:
      caps[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ")] = config[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index][bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")]
    if bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣿ") in config[bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index]:
      caps[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ")] = str(config[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index][bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")])
    bstack1ll1111ll1_opy_ = bstack1lll1ll1l1_opy_(bstack1ll11ll111_opy_, config[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index], logger)
    bstack111ll1l1_opy_ += list(bstack1ll1111ll1_opy_.keys())
    for bstack1ll11lll_opy_ in bstack111ll1l1_opy_:
      if bstack1ll11lll_opy_ in config[bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1ll11lll_opy_ == bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack1ll1111ll1_opy_[bstack1ll11lll_opy_] = str(config[bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1ll11lll_opy_] * 1.0)
          except:
            bstack1ll1111ll1_opy_[bstack1ll11lll_opy_] = str(config[bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1ll11lll_opy_])
        else:
          bstack1ll1111ll1_opy_[bstack1ll11lll_opy_] = config[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1ll11lll_opy_]
        del (config[bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1ll11lll_opy_])
    bstack1l1l11llll_opy_ = update(bstack1l1l11llll_opy_, bstack1ll1111ll1_opy_)
  bstack111111l1_opy_ = bstack111l1lll1_opy_(config, index)
  for bstack1l11l1ll_opy_ in bstack1l1111l1ll_opy_ + list(bstack1ll11111l_opy_.keys()):
    if bstack1l11l1ll_opy_ in bstack111111l1_opy_:
      bstack1l1l11llll_opy_[bstack1l11l1ll_opy_] = bstack111111l1_opy_[bstack1l11l1ll_opy_]
      del (bstack111111l1_opy_[bstack1l11l1ll_opy_])
  if bstack1lll1lll1_opy_(config):
    bstack111111l1_opy_[bstack1lll1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1l1l11llll_opy_)
    caps[bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack111111l1_opy_
  else:
    bstack111111l1_opy_[bstack1lll1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack11lll1ll_opy_(bstack111111l1_opy_, bstack1l1l11llll_opy_))
    if bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1ll11l1l1_opy_():
  global bstack1l1lll1l_opy_
  if bstack1111l1l1l_opy_() <= version.parse(bstack1lll1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack1l1lll1l_opy_ != bstack1lll1l_opy_ (u"ࠪࠫग"):
      return bstack1lll1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack1l1lll1l_opy_ + bstack1lll1l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack111l111l1_opy_
  if bstack1l1lll1l_opy_ != bstack1lll1l_opy_ (u"࠭ࠧच"):
    return bstack1lll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack1l1lll1l_opy_ + bstack1lll1l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack11l1l11l1_opy_
def bstack1l1l1111l1_opy_(options):
  return hasattr(options, bstack1lll1l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll1llll1l_opy_(options, bstack1111lll11_opy_):
  for bstack1l1ll11l11_opy_ in bstack1111lll11_opy_:
    if bstack1l1ll11l11_opy_ in [bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1lll1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack1l1ll11l11_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1ll11l11_opy_] = update(options._experimental_options[bstack1l1ll11l11_opy_],
                                                         bstack1111lll11_opy_[bstack1l1ll11l11_opy_])
    else:
      options.add_experimental_option(bstack1l1ll11l11_opy_, bstack1111lll11_opy_[bstack1l1ll11l11_opy_])
  if bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack1111lll11_opy_:
    for arg in bstack1111lll11_opy_[bstack1lll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack1111lll11_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1lll1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack1111lll11_opy_:
    for ext in bstack1111lll11_opy_[bstack1lll1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack1111lll11_opy_[bstack1lll1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1l111lll1l_opy_(options, bstack1lllll11l1_opy_):
  if bstack1lll1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1lllll11l1_opy_:
    for bstack11l111ll_opy_ in bstack1lllll11l1_opy_[bstack1lll1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack11l111ll_opy_ in options._preferences:
        options._preferences[bstack11l111ll_opy_] = update(options._preferences[bstack11l111ll_opy_], bstack1lllll11l1_opy_[bstack1lll1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack11l111ll_opy_])
      else:
        options.set_preference(bstack11l111ll_opy_, bstack1lllll11l1_opy_[bstack1lll1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack11l111ll_opy_])
  if bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1lllll11l1_opy_:
    for arg in bstack1lllll11l1_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1ll1llllll_opy_(options, bstack1ll1ll1l1l_opy_):
  if bstack1lll1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack1ll1ll1l1l_opy_:
    options.use_webview(bool(bstack1ll1ll1l1l_opy_[bstack1lll1l_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1ll1llll1l_opy_(options, bstack1ll1ll1l1l_opy_)
def bstack111l1111l_opy_(options, bstack1l111l1l11_opy_):
  for bstack1lll11ll_opy_ in bstack1l111l1l11_opy_:
    if bstack1lll11ll_opy_ in [bstack1lll1l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1lll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack1lll11ll_opy_, bstack1l111l1l11_opy_[bstack1lll11ll_opy_])
  if bstack1lll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1l111l1l11_opy_:
    for arg in bstack1l111l1l11_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1lll1l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1l111l1l11_opy_:
    options.bstack1ll1l11l1_opy_(bool(bstack1l111l1l11_opy_[bstack1lll1l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack11l1lll1_opy_(options, bstack1llll1lll1_opy_):
  for bstack1llll1lll_opy_ in bstack1llll1lll1_opy_:
    if bstack1llll1lll_opy_ in [bstack1lll1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack1llll1lll_opy_] = bstack1llll1lll1_opy_[bstack1llll1lll_opy_]
  if bstack1lll1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1llll1lll1_opy_:
    for bstack1ll11l1l1l_opy_ in bstack1llll1lll1_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1l1l1l11l1_opy_(
        bstack1ll11l1l1l_opy_, bstack1llll1lll1_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1ll11l1l1l_opy_])
  if bstack1lll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1llll1lll1_opy_:
    for arg in bstack1llll1lll1_opy_[bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1ll1l1ll1_opy_(options, caps):
  if not hasattr(options, bstack1lll1l_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1lll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1ll1llll1l_opy_(options, caps[bstack1lll1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1lll1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1l111lll1l_opy_(options, caps[bstack1lll1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1lll1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack111l1111l_opy_(options, caps[bstack1lll1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1lll1l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1ll1llllll_opy_(options, caps[bstack1lll1l_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1lll1l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack11l1lll1_opy_(options, caps[bstack1lll1l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1ll1l1ll1l_opy_(caps):
  global bstack1111ll11l_opy_
  if isinstance(os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1111ll11l_opy_ = eval(os.getenv(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1111ll11l_opy_:
    if bstack11111l1l1_opy_() < version.parse(bstack1lll1l_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1lll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1lll1l_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1lll1l_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1lll1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1lll1l_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1lll1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1lll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1lll1l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1lll1l_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1lll1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1lll1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1lll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1lll1l_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l1111l1_opy_(options):
        return None
      for bstack1l11l1ll_opy_ in caps.keys():
        options.set_capability(bstack1l11l1ll_opy_, caps[bstack1l11l1ll_opy_])
      bstack1ll1l1ll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111ll11l1_opy_(options, bstack1l1l111lll_opy_):
  if not bstack1l1l1111l1_opy_(options):
    return
  for bstack1l11l1ll_opy_ in bstack1l1l111lll_opy_.keys():
    if bstack1l11l1ll_opy_ in bstack111l1111_opy_:
      continue
    if bstack1l11l1ll_opy_ in options._caps and type(options._caps[bstack1l11l1ll_opy_]) in [dict, list]:
      options._caps[bstack1l11l1ll_opy_] = update(options._caps[bstack1l11l1ll_opy_], bstack1l1l111lll_opy_[bstack1l11l1ll_opy_])
    else:
      options.set_capability(bstack1l11l1ll_opy_, bstack1l1l111lll_opy_[bstack1l11l1ll_opy_])
  bstack1ll1l1ll1_opy_(options, bstack1l1l111lll_opy_)
  if bstack1lll1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1lll1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack111llll1l_opy_(proxy_config):
  if bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1lll1l_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1lll1l_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1lll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1lll1l_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1lll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1lll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1lll1l_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack1l111111ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1lll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack111llll1l_opy_(config[bstack1lll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1lll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack11l11111l_opy_(self):
  global CONFIG
  global bstack1l1l111l1l_opy_
  try:
    proxy = bstack1l1l1lll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1lll1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack1llll111ll_opy_(proxy, bstack1ll11l1l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1111111_opy_ = proxies.popitem()
          if bstack1lll1l_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1ll1111111_opy_:
            return bstack1ll1111111_opy_
          else:
            return bstack1lll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1ll1111111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1l1l111l1l_opy_(self)
def bstack11111l1l_opy_():
  global CONFIG
  return bstack1llll1ll11_opy_(CONFIG) and bstack11lllll1l_opy_() and bstack1111l1l1l_opy_() >= version.parse(bstack11llllllll_opy_)
def bstack1ll1l1llll_opy_():
  global CONFIG
  return (bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack11lllll11_opy_()
def bstack111l1lll_opy_(config):
  bstack1ll1l11lll_opy_ = {}
  if bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack1ll1l11lll_opy_ = config[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack1lll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack1ll1l11lll_opy_ = config[bstack1lll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack1l1l1lll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1lll1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack1ll1l11lll_opy_[bstack1lll1l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1lll1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack1l1l1111_opy_(config, bstack1ll11l1l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1111111_opy_ = proxies.popitem()
          if bstack1lll1l_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack1ll1111111_opy_:
            parsed_url = urlparse(bstack1ll1111111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1lll1l_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack1ll1111111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1l11lll_opy_[bstack1lll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1l11lll_opy_[bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1l11lll_opy_[bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1l11lll_opy_[bstack1lll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack1ll1l11lll_opy_
def bstack1ll11ll1l_opy_(config):
  if bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack1l11lll1l_opy_(caps):
  global bstack11lll1111_opy_
  if bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1lll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack11lll1111_opy_:
      caps[bstack1lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack1lll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack11lll1111_opy_
  else:
    caps[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack11lll1111_opy_:
      caps[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack11lll1111_opy_
def bstack1111ll1ll_opy_():
  global CONFIG
  if not bstack1l11l1l111_opy_(CONFIG):
    return
  if bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack1l1lllll1l_opy_(CONFIG[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    if (
      bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍") in CONFIG
      and bstack1l1lllll1l_opy_(CONFIG[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")].get(bstack1lll1l_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨএ")))
    ):
      logger.debug(bstack1lll1l_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨঐ"))
      return
    bstack1ll1l11lll_opy_ = bstack111l1lll_opy_(CONFIG)
    bstack1l1lll1lll_opy_(CONFIG[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1ll1l11lll_opy_)
def bstack1l1lll1lll_opy_(key, bstack1ll1l11lll_opy_):
  global bstack1ll11111l1_opy_
  logger.info(bstack11lll11l_opy_)
  try:
    bstack1ll11111l1_opy_ = Local()
    bstack1l111l1111_opy_ = {bstack1lll1l_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1l111l1111_opy_.update(bstack1ll1l11lll_opy_)
    logger.debug(bstack1l1111l1l1_opy_.format(str(bstack1l111l1111_opy_)))
    bstack1ll11111l1_opy_.start(**bstack1l111l1111_opy_)
    if bstack1ll11111l1_opy_.isRunning():
      logger.info(bstack1llll1l1l_opy_)
  except Exception as e:
    bstack11ll1l11l_opy_(bstack1lll11l1l1_opy_.format(str(e)))
def bstack111l111ll_opy_():
  global bstack1ll11111l1_opy_
  if bstack1ll11111l1_opy_.isRunning():
    logger.info(bstack1l111ll111_opy_)
    bstack1ll11111l1_opy_.stop()
  bstack1ll11111l1_opy_ = None
def bstack1l11ll1111_opy_(bstack1l1lll111l_opy_=[]):
  global CONFIG
  bstack1ll1l111l_opy_ = []
  bstack11111111l_opy_ = [bstack1lll1l_opy_ (u"ࠨࡱࡶࠫও"), bstack1lll1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1lll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1l1lll111l_opy_:
      bstack1l1ll111ll_opy_ = {}
      for k in bstack11111111l_opy_:
        val = CONFIG[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1lll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1l1ll111ll_opy_[k] = val
      if(err[bstack1lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1lll1l_opy_ (u"ࠪࠫজ")):
        bstack1l1ll111ll_opy_[bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1ll1l111l_opy_.append(bstack1l1ll111ll_opy_)
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1ll1l111l_opy_
def bstack111llllll_opy_(file_name):
  bstack1l11111l_opy_ = []
  try:
    bstack1l1lllll11_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1lllll11_opy_):
      with open(bstack1l1lllll11_opy_) as f:
        bstack11ll11ll_opy_ = json.load(f)
        bstack1l11111l_opy_ = bstack11ll11ll_opy_
      os.remove(bstack1l1lllll11_opy_)
    return bstack1l11111l_opy_
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
    return bstack1l11111l_opy_
def bstack1l11lllll1_opy_():
  global bstack11l1111ll_opy_
  global bstack111ll1ll_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1llllll11_opy_
  global bstack1l1l11l11l_opy_
  global bstack1l1lll1l1l_opy_
  global CONFIG
  bstack1l11lll11l_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1l11lll11l_opy_ in [bstack1lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1lll1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1lll11111_opy_()
  percy.shutdown()
  if bstack11l1111ll_opy_:
    logger.warning(bstack1l1l11l1l1_opy_.format(str(bstack11l1111ll_opy_)))
  else:
    try:
      bstack1l11111ll1_opy_ = bstack1lll1ll1_opy_(bstack1lll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l11111ll1_opy_.get(bstack1lll1l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l11111ll1_opy_.get(bstack1lll1l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1lll1l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1l1l11l1l1_opy_.format(str(bstack1l11111ll1_opy_[bstack1lll1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1l1l11111_opy_)
  global bstack1ll11111l1_opy_
  if bstack1ll11111l1_opy_:
    bstack111l111ll_opy_()
  try:
    for driver in bstack111ll1ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l111lll1_opy_)
  if bstack1l1lll1l1l_opy_ == bstack1lll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1l1l11l11l_opy_ = bstack111llllll_opy_(bstack1lll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1l1lll1l1l_opy_ == bstack1lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1llllll11_opy_) == 0:
    bstack1llllll11_opy_ = bstack111llllll_opy_(bstack1lll1l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1llllll11_opy_) == 0:
      bstack1llllll11_opy_ = bstack111llllll_opy_(bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1lll1111_opy_ = bstack1lll1l_opy_ (u"ࠩࠪর")
  if len(bstack1l1l1l1ll1_opy_) > 0:
    bstack1lll1111_opy_ = bstack1l11ll1111_opy_(bstack1l1l1l1ll1_opy_)
  elif len(bstack1llllll11_opy_) > 0:
    bstack1lll1111_opy_ = bstack1l11ll1111_opy_(bstack1llllll11_opy_)
  elif len(bstack1l1l11l11l_opy_) > 0:
    bstack1lll1111_opy_ = bstack1l11ll1111_opy_(bstack1l1l11l11l_opy_)
  elif len(bstack11ll111ll_opy_) > 0:
    bstack1lll1111_opy_ = bstack1l11ll1111_opy_(bstack11ll111ll_opy_)
  if bool(bstack1lll1111_opy_):
    bstack1ll111ll11_opy_(bstack1lll1111_opy_)
  else:
    bstack1ll111ll11_opy_()
  bstack111ll111_opy_(bstack1ll1l1l11l_opy_, logger)
  bstack1lll111l1_opy_.bstack1l11llll_opy_(CONFIG)
  if len(bstack1l1l11l11l_opy_) > 0:
    sys.exit(len(bstack1l1l11l11l_opy_))
def bstack1ll1l111ll_opy_(bstack1l1ll11ll_opy_, frame):
  global bstack1l1l111l_opy_
  logger.error(bstack1lllll1111_opy_)
  bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭঱"), bstack1l1ll11ll_opy_)
  if hasattr(signal, bstack1lll1l_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬল")):
    bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ঳"), signal.Signals(bstack1l1ll11ll_opy_).name)
  else:
    bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭঴"), bstack1lll1l_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫ঵"))
  bstack1l11lll11l_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩশ"))
  if bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩষ"):
    bstack1111ll111_opy_.stop(bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪস")))
  bstack1l11lllll1_opy_()
  sys.exit(1)
def bstack11ll1l11l_opy_(err):
  logger.critical(bstack11lll11l1_opy_.format(str(err)))
  bstack1ll111ll11_opy_(bstack11lll11l1_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11lllll1_opy_)
  bstack1lll11111_opy_()
  sys.exit(1)
def bstack11111l1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll111ll11_opy_(message, True)
  atexit.unregister(bstack1l11lllll1_opy_)
  bstack1lll11111_opy_()
  sys.exit(1)
def bstack11l111111_opy_():
  global CONFIG
  global bstack11ll1llll_opy_
  global bstack111l1ll1_opy_
  global bstack1lll111l_opy_
  CONFIG = bstack1llll11l1_opy_()
  load_dotenv(CONFIG.get(bstack1lll1l_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬহ")))
  bstack1l11ll1ll1_opy_()
  bstack1ll1ll11_opy_()
  CONFIG = bstack1l1ll1ll_opy_(CONFIG)
  update(CONFIG, bstack111l1ll1_opy_)
  update(CONFIG, bstack11ll1llll_opy_)
  CONFIG = bstack11l11ll11_opy_(CONFIG)
  bstack1lll111l_opy_ = bstack1l11l1l111_opy_(CONFIG)
  os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ঺")] = bstack1lll111l_opy_.__str__()
  bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ঻"), bstack1lll111l_opy_)
  if (bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") in CONFIG and bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫঽ") in bstack11ll1llll_opy_) or (
          bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬা") in CONFIG and bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ি") not in bstack111l1ll1_opy_):
    if os.getenv(bstack1lll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨী")):
      CONFIG[bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧু")] = os.getenv(bstack1lll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪূ"))
    else:
      bstack1l11ll1l_opy_()
  elif (bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪৃ") not in CONFIG and bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৄ") in CONFIG) or (
          bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৅") in bstack111l1ll1_opy_ and bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭৆") not in bstack11ll1llll_opy_):
    del (CONFIG[bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ে")])
  if bstack1l111l1lll_opy_(CONFIG):
    bstack11ll1l11l_opy_(bstack1lll1lllll_opy_)
  bstack1lll1l1111_opy_()
  bstack1ll1l111l1_opy_()
  if bstack1111ll11l_opy_:
    CONFIG[bstack1lll1l_opy_ (u"ࠬࡧࡰࡱࠩৈ")] = bstack1l1lllll_opy_(CONFIG)
    logger.info(bstack11111lll1_opy_.format(CONFIG[bstack1lll1l_opy_ (u"࠭ࡡࡱࡲࠪ৉")]))
  if not bstack1lll111l_opy_:
    CONFIG[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৊")] = [{}]
def bstack1lllll1ll1_opy_(config, bstack11l111l11_opy_):
  global CONFIG
  global bstack1111ll11l_opy_
  CONFIG = config
  bstack1111ll11l_opy_ = bstack11l111l11_opy_
def bstack1ll1l111l1_opy_():
  global CONFIG
  global bstack1111ll11l_opy_
  if bstack1lll1l_opy_ (u"ࠨࡣࡳࡴࠬো") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11l1l1lll_opy_)
    bstack1111ll11l_opy_ = True
    bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨৌ"), True)
def bstack1l1lllll_opy_(config):
  bstack1lllllll1_opy_ = bstack1lll1l_opy_ (u"্ࠪࠫ")
  app = config[bstack1lll1l_opy_ (u"ࠫࡦࡶࡰࠨৎ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1ll11l1_opy_:
      if os.path.exists(app):
        bstack1lllllll1_opy_ = bstack1l1ll1l1l1_opy_(config, app)
      elif bstack1ll11l11l_opy_(app):
        bstack1lllllll1_opy_ = app
      else:
        bstack11ll1l11l_opy_(bstack1lll111l11_opy_.format(app))
    else:
      if bstack1ll11l11l_opy_(app):
        bstack1lllllll1_opy_ = app
      elif os.path.exists(app):
        bstack1lllllll1_opy_ = bstack1l1ll1l1l1_opy_(app)
      else:
        bstack11ll1l11l_opy_(bstack1ll111111_opy_)
  else:
    if len(app) > 2:
      bstack11ll1l11l_opy_(bstack1l111l1l_opy_)
    elif len(app) == 2:
      if bstack1lll1l_opy_ (u"ࠬࡶࡡࡵࡪࠪ৏") in app and bstack1lll1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐") in app:
        if os.path.exists(app[bstack1lll1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৑")]):
          bstack1lllllll1_opy_ = bstack1l1ll1l1l1_opy_(config, app[bstack1lll1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭৒")], app[bstack1lll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৓")])
        else:
          bstack11ll1l11l_opy_(bstack1lll111l11_opy_.format(app))
      else:
        bstack11ll1l11l_opy_(bstack1l111l1l_opy_)
    else:
      for key in app:
        if key in bstack11lll1lll_opy_:
          if key == bstack1lll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৔"):
            if os.path.exists(app[key]):
              bstack1lllllll1_opy_ = bstack1l1ll1l1l1_opy_(config, app[key])
            else:
              bstack11ll1l11l_opy_(bstack1lll111l11_opy_.format(app))
          else:
            bstack1lllllll1_opy_ = app[key]
        else:
          bstack11ll1l11l_opy_(bstack111lll11l_opy_)
  return bstack1lllllll1_opy_
def bstack1ll11l11l_opy_(bstack1lllllll1_opy_):
  import re
  bstack11l11111_opy_ = re.compile(bstack1lll1l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৕"))
  bstack1lllll1l11_opy_ = re.compile(bstack1lll1l_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ৖"))
  if bstack1lll1l_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬৗ") in bstack1lllllll1_opy_ or re.fullmatch(bstack11l11111_opy_, bstack1lllllll1_opy_) or re.fullmatch(bstack1lllll1l11_opy_, bstack1lllllll1_opy_):
    return True
  else:
    return False
def bstack1l1ll1l1l1_opy_(config, path, bstack1llllll1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1lll1l_opy_ (u"ࠧࡳࡤࠪ৘")).read()).hexdigest()
  bstack11l11l111_opy_ = bstack1lllllllll_opy_(md5_hash)
  bstack1lllllll1_opy_ = None
  if bstack11l11l111_opy_:
    logger.info(bstack11lllllll_opy_.format(bstack11l11l111_opy_, md5_hash))
    return bstack11l11l111_opy_
  bstack1ll1l1l1ll_opy_ = MultipartEncoder(
    fields={
      bstack1lll1l_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭৙"): (os.path.basename(path), open(os.path.abspath(path), bstack1lll1l_opy_ (u"ࠩࡵࡦࠬ৚")), bstack1lll1l_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧ৛")),
      bstack1lll1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧড়"): bstack1llllll1l_opy_
    }
  )
  response = requests.post(bstack1l1l1ll1l_opy_, data=bstack1ll1l1l1ll_opy_,
                           headers={bstack1lll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫঢ়"): bstack1ll1l1l1ll_opy_.content_type},
                           auth=(config[bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ৞")], config[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪয়")]))
  try:
    res = json.loads(response.text)
    bstack1lllllll1_opy_ = res[bstack1lll1l_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩৠ")]
    logger.info(bstack11l1l111l_opy_.format(bstack1lllllll1_opy_))
    bstack1l11lll1ll_opy_(md5_hash, bstack1lllllll1_opy_)
  except ValueError as err:
    bstack11ll1l11l_opy_(bstack1111l11ll_opy_.format(str(err)))
  return bstack1lllllll1_opy_
def bstack1lll1l1111_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11lll11ll_opy_
  bstack1l1l11l11_opy_ = 1
  bstack11l1111l_opy_ = 1
  if bstack1lll1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩৡ") in CONFIG:
    bstack11l1111l_opy_ = CONFIG[bstack1lll1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪৢ")]
  else:
    bstack11l1111l_opy_ = bstack1llll111_opy_(framework_name, args) or 1
  if bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ") in CONFIG:
    bstack1l1l11l11_opy_ = len(CONFIG[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৤")])
  bstack11lll11ll_opy_ = int(bstack11l1111l_opy_) * int(bstack1l1l11l11_opy_)
def bstack1llll111_opy_(framework_name, args):
  if framework_name == bstack1l11ll1ll_opy_ and args and bstack1lll1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ৥") in args:
      bstack1l1lll11ll_opy_ = args.index(bstack1lll1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ০"))
      return int(args[bstack1l1lll11ll_opy_ + 1]) or 1
  return 1
def bstack1lllllllll_opy_(md5_hash):
  bstack1ll1l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠨࢀࠪ১")), bstack1lll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ২"), bstack1lll1l_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৩"))
  if os.path.exists(bstack1ll1l1l1l1_opy_):
    bstack1l1lll1ll1_opy_ = json.load(open(bstack1ll1l1l1l1_opy_, bstack1lll1l_opy_ (u"ࠫࡷࡨࠧ৪")))
    if md5_hash in bstack1l1lll1ll1_opy_:
      bstack111l1ll1l_opy_ = bstack1l1lll1ll1_opy_[md5_hash]
      bstack1llll1ll_opy_ = datetime.datetime.now()
      bstack1ll1lll1l_opy_ = datetime.datetime.strptime(bstack111l1ll1l_opy_[bstack1lll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৫")], bstack1lll1l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৬"))
      if (bstack1llll1ll_opy_ - bstack1ll1lll1l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack111l1ll1l_opy_[bstack1lll1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৭")]):
        return None
      return bstack111l1ll1l_opy_[bstack1lll1l_opy_ (u"ࠨ࡫ࡧࠫ৮")]
  else:
    return None
def bstack1l11lll1ll_opy_(md5_hash, bstack1lllllll1_opy_):
  bstack111l111l_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠩࢁࠫ৯")), bstack1lll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৰ"))
  if not os.path.exists(bstack111l111l_opy_):
    os.makedirs(bstack111l111l_opy_)
  bstack1ll1l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠫࢃ࠭ৱ")), bstack1lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৲"), bstack1lll1l_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৳"))
  bstack111ll11l_opy_ = {
    bstack1lll1l_opy_ (u"ࠧࡪࡦࠪ৴"): bstack1lllllll1_opy_,
    bstack1lll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ৵"): datetime.datetime.strftime(datetime.datetime.now(), bstack1lll1l_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭৶")),
    bstack1lll1l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৷"): str(__version__)
  }
  if os.path.exists(bstack1ll1l1l1l1_opy_):
    bstack1l1lll1ll1_opy_ = json.load(open(bstack1ll1l1l1l1_opy_, bstack1lll1l_opy_ (u"ࠫࡷࡨࠧ৸")))
  else:
    bstack1l1lll1ll1_opy_ = {}
  bstack1l1lll1ll1_opy_[md5_hash] = bstack111ll11l_opy_
  with open(bstack1ll1l1l1l1_opy_, bstack1lll1l_opy_ (u"ࠧࡽࠫࠣ৹")) as outfile:
    json.dump(bstack1l1lll1ll1_opy_, outfile)
def bstack11ll11111_opy_(self):
  return
def bstack1l11l11l1l_opy_(self):
  return
def bstack1ll1111l1l_opy_(self):
  global bstack1ll1l1111l_opy_
  bstack1ll1l1111l_opy_(self)
def bstack1llll1llll_opy_():
  global bstack1lll1111l_opy_
  bstack1lll1111l_opy_ = True
def bstack11l1ll111_opy_(self):
  global bstack1ll1lllll_opy_
  global bstack1l11ll11l_opy_
  global bstack11l1l11ll_opy_
  try:
    if bstack1lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৺") in bstack1ll1lllll_opy_ and self.session_id != None and bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৻"), bstack1lll1l_opy_ (u"ࠨࠩৼ")) != bstack1lll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৽"):
      bstack1l1lllll1_opy_ = bstack1lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ৾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৿")
      if bstack1l1lllll1_opy_ == bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ਀"):
        bstack1lll1l1ll_opy_(logger)
      if self != None:
        bstack1l1111l111_opy_(self, bstack1l1lllll1_opy_, bstack1lll1l_opy_ (u"࠭ࠬࠡࠩਁ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1lll1l_opy_ (u"ࠧࠨਂ")
    if bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ") in bstack1ll1lllll_opy_ and getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ਄"), None):
      bstack1111l11l_opy_.bstack1lllllll1l_opy_(self, bstack1ll1ll1l_opy_, logger, wait=True)
    if bstack1lll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪਅ") in bstack1ll1lllll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l1111l111_opy_(self, bstack1lll1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦਆ"))
      bstack111111lll_opy_.bstack1111l1111_opy_(self)
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨਇ") + str(e))
  bstack11l1l11ll_opy_(self)
  self.session_id = None
def bstack11ll1l1l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1l1l11_opy_
    global bstack1ll1lllll_opy_
    command_executor = kwargs.get(bstack1lll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩਈ"), bstack1lll1l_opy_ (u"ࠧࠨਉ"))
    bstack1ll1ll11l_opy_ = False
    if type(command_executor) == str and bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਊ") in command_executor:
      bstack1ll1ll11l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ਋") in str(getattr(command_executor, bstack1lll1l_opy_ (u"ࠪࡣࡺࡸ࡬ࠨ਌"), bstack1lll1l_opy_ (u"ࠫࠬ਍"))):
      bstack1ll1ll11l_opy_ = True
    else:
      return bstack1lll11l11l_opy_(self, *args, **kwargs)
    if bstack1ll1ll11l_opy_:
      if kwargs.get(bstack1lll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭਎")):
        kwargs[bstack1lll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧਏ")] = bstack1l1l1l11_opy_(kwargs[bstack1lll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨਐ")], bstack1ll1lllll_opy_)
      elif kwargs.get(bstack1lll1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ਑")):
        kwargs[bstack1lll1l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ਒")] = bstack1l1l1l11_opy_(kwargs[bstack1lll1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪਓ")], bstack1ll1lllll_opy_)
  except Exception as e:
    logger.error(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦਔ").format(str(e)))
  return bstack1lll11l11l_opy_(self, *args, **kwargs)
def bstack1ll1ll1lll_opy_(self, command_executor=bstack1lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨਕ"), *args, **kwargs):
  bstack1l11l1111l_opy_ = bstack11ll1l1l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11l111l1l_opy_.on():
    return bstack1l11l1111l_opy_
  try:
    logger.debug(bstack1lll1l_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪਖ").format(str(command_executor)))
    logger.debug(bstack1lll1l_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩਗ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਘ") in command_executor._url:
      bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਙ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ਚ") in command_executor):
    bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬਛ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1111ll111_opy_.bstack111l1l1l_opy_(self)
  return bstack1l11l1111l_opy_
def bstack1l11llll1_opy_(args):
  return bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ਜ") in str(args)
def bstack1llllll1ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1111111ll_opy_
  global bstack1ll1l11ll_opy_
  bstack11l1ll11_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪਝ"), None) and bstack1ll111lll1_opy_(
          threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ਞ"), None)
  bstack1l11ll1l11_opy_ = getattr(self, bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਟ"), None) != None and getattr(self, bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩਠ"), None) == True
  if not bstack1ll1l11ll_opy_ and bstack1lll111l_opy_ and bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਡ") in CONFIG and CONFIG[bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫਢ")] == True and bstack1l111111l1_opy_.bstack1llll111l1_opy_(driver_command) and (bstack1l11ll1l11_opy_ or bstack11l1ll11_opy_) and not bstack1l11llll1_opy_(args):
    try:
      bstack1ll1l11ll_opy_ = True
      logger.debug(bstack1lll1l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧਣ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1lll1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫਤ").format(str(err)))
    bstack1ll1l11ll_opy_ = False
  response = bstack1111111ll_opy_(self, driver_command, *args, **kwargs)
  if (bstack1lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in str(bstack1ll1lllll_opy_).lower() or bstack1lll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਦ") in str(bstack1ll1lllll_opy_).lower()) and bstack11l111l1l_opy_.on():
    try:
      if driver_command == bstack1lll1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ਧ"):
        bstack1111ll111_opy_.bstack1lll11ll1l_opy_({
            bstack1lll1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩਨ"): response[bstack1lll1l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ਩")],
            bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬਪ"): bstack1111ll111_opy_.current_test_uuid() if bstack1111ll111_opy_.current_test_uuid() else bstack11l111l1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1lll1l111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11ll11l_opy_
  global bstack1llll11lll_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1lll111111_opy_
  global bstack1l1l1l111_opy_
  global bstack1ll1lllll_opy_
  global bstack1lll11l11l_opy_
  global bstack111ll1ll_opy_
  global bstack111l1l1l1_opy_
  global bstack1ll1ll1l_opy_
  CONFIG[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1ll1lllll_opy_) + str(__version__)
  command_executor = bstack1ll11l1l1_opy_()
  logger.debug(bstack11l111lll_opy_.format(command_executor))
  proxy = bstack1l111111ll_opy_(CONFIG, proxy)
  bstack1llllll1l1_opy_ = 0 if bstack1llll11lll_opy_ < 0 else bstack1llll11lll_opy_
  try:
    if bstack1lll111111_opy_ is True:
      bstack1llllll1l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1l1l111_opy_ is True:
      bstack1llllll1l1_opy_ = int(threading.current_thread().name)
  except:
    bstack1llllll1l1_opy_ = 0
  bstack1l1l111lll_opy_ = bstack1l11lllll_opy_(CONFIG, bstack1llllll1l1_opy_)
  logger.debug(bstack111l11ll_opy_.format(str(bstack1l1l111lll_opy_)))
  if bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ") in CONFIG and bstack1l1lllll1l_opy_(CONFIG[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")]):
    bstack1l11lll1l_opy_(bstack1l1l111lll_opy_)
  if bstack1ll111llll_opy_.bstack11l1lllll_opy_(CONFIG, bstack1llllll1l1_opy_) and bstack1ll111llll_opy_.bstack11ll1l11_opy_(bstack1l1l111lll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1ll111llll_opy_.set_capabilities(bstack1l1l111lll_opy_, CONFIG)
  if desired_capabilities:
    bstack11l1lll11_opy_ = bstack1l1ll1ll_opy_(desired_capabilities)
    bstack11l1lll11_opy_[bstack1lll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩਮ")] = bstack1lll1lll1_opy_(CONFIG)
    bstack1l11l111l_opy_ = bstack1l11lllll_opy_(bstack11l1lll11_opy_)
    if bstack1l11l111l_opy_:
      bstack1l1l111lll_opy_ = update(bstack1l11l111l_opy_, bstack1l1l111lll_opy_)
    desired_capabilities = None
  if options:
    bstack111ll11l1_opy_(options, bstack1l1l111lll_opy_)
  if not options:
    options = bstack1ll1l1ll1l_opy_(bstack1l1l111lll_opy_)
  bstack1ll1ll1l_opy_ = CONFIG.get(bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ"))[bstack1llllll1l1_opy_]
  if proxy and bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਰ")):
    options.proxy(proxy)
  if options and bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ਱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1111l1l1l_opy_() < version.parse(bstack1lll1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਲ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1l111lll_opy_)
  logger.info(bstack1llll1l11l_opy_)
  if bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਲ਼")):
    bstack1lll11l11l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ਴")):
    bstack1lll11l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩਵ")):
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
    bstack1l11l11111_opy_ = bstack1lll1l_opy_ (u"ࠪࠫਸ਼")
    if bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ਷")):
      bstack1l11l11111_opy_ = self.caps.get(bstack1lll1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਸ"))
    else:
      bstack1l11l11111_opy_ = self.capabilities.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਹ"))
    if bstack1l11l11111_opy_:
      bstack1l1l1ll11_opy_(bstack1l11l11111_opy_)
      if bstack1111l1l1l_opy_() <= version.parse(bstack1lll1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ਺")):
        self.command_executor._url = bstack1lll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ਻") + bstack1l1lll1l_opy_ + bstack1lll1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ਼")
      else:
        self.command_executor._url = bstack1lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ਽") + bstack1l11l11111_opy_ + bstack1lll1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਾ")
      logger.debug(bstack1lllll1l1_opy_.format(bstack1l11l11111_opy_))
    else:
      logger.debug(bstack1l1l11lll_opy_.format(bstack1lll1l_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਿ")))
  except Exception as e:
    logger.debug(bstack1l1l11lll_opy_.format(e))
  if bstack1lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬੀ") in bstack1ll1lllll_opy_:
    bstack11llll11_opy_(bstack1llll11lll_opy_, bstack111l1l1l1_opy_)
  bstack1l11ll11l_opy_ = self.session_id
  if bstack1lll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧੁ") in bstack1ll1lllll_opy_ or bstack1lll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨੂ") in bstack1ll1lllll_opy_ or bstack1lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃") in bstack1ll1lllll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1111ll111_opy_.bstack111l1l1l_opy_(self)
  bstack111ll1ll_opy_.append(self)
  if bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄") in CONFIG and bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੅") in CONFIG[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆")][bstack1llllll1l1_opy_]:
    bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ")][bstack1llllll1l1_opy_][bstack1lll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ")]
  logger.debug(bstack1l1l1lll_opy_.format(bstack1l11ll11l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll1lll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1lll111_opy_
      if(bstack1lll1l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ੉") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠩࢁࠫ੊")), bstack1lll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪੋ"), bstack1lll1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ੌ")), bstack1lll1l_opy_ (u"ࠬࡽ੍ࠧ")) as fp:
          fp.write(bstack1lll1l_opy_ (u"ࠨࠢ੎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1lll1l_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ੏")))):
          with open(args[1], bstack1lll1l_opy_ (u"ࠨࡴࠪ੐")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1lll1l_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨੑ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111lll111_opy_)
            lines.insert(1, bstack1l11l1l1ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1lll1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੒")), bstack1lll1l_opy_ (u"ࠫࡼ࠭੓")) as bstack1l111ll1l_opy_:
              bstack1l111ll1l_opy_.writelines(lines)
        CONFIG[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੔")] = str(bstack1ll1lllll_opy_) + str(__version__)
        bstack1llllll1l1_opy_ = 0 if bstack1llll11lll_opy_ < 0 else bstack1llll11lll_opy_
        try:
          if bstack1lll111111_opy_ is True:
            bstack1llllll1l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1l1l111_opy_ is True:
            bstack1llllll1l1_opy_ = int(threading.current_thread().name)
        except:
          bstack1llllll1l1_opy_ = 0
        CONFIG[bstack1lll1l_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ੕")] = False
        CONFIG[bstack1lll1l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ੖")] = True
        bstack1l1l111lll_opy_ = bstack1l11lllll_opy_(CONFIG, bstack1llllll1l1_opy_)
        logger.debug(bstack111l11ll_opy_.format(str(bstack1l1l111lll_opy_)))
        if CONFIG.get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ੗")):
          bstack1l11lll1l_opy_(bstack1l1l111lll_opy_)
        if bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੘") in CONFIG and bstack1lll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਖ਼") in CONFIG[bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")][bstack1llllll1l1_opy_]:
          bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")][bstack1llllll1l1_opy_][bstack1lll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੜ")]
        args.append(os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠧࡿࠩ੝")), bstack1lll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack1lll1l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੟")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1l111lll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1lll1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੠"))
      bstack1ll1lll111_opy_ = True
      return bstack11l1l1ll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1llll1111l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1llll11lll_opy_
    global bstack1l1ll1ll1_opy_
    global bstack1lll111111_opy_
    global bstack1l1l1l111_opy_
    global bstack1ll1lllll_opy_
    CONFIG[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭੡")] = str(bstack1ll1lllll_opy_) + str(__version__)
    bstack1llllll1l1_opy_ = 0 if bstack1llll11lll_opy_ < 0 else bstack1llll11lll_opy_
    try:
      if bstack1lll111111_opy_ is True:
        bstack1llllll1l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1l1l111_opy_ is True:
        bstack1llllll1l1_opy_ = int(threading.current_thread().name)
    except:
      bstack1llllll1l1_opy_ = 0
    CONFIG[bstack1lll1l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ੢")] = True
    bstack1l1l111lll_opy_ = bstack1l11lllll_opy_(CONFIG, bstack1llllll1l1_opy_)
    logger.debug(bstack111l11ll_opy_.format(str(bstack1l1l111lll_opy_)))
    if CONFIG.get(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੣")):
      bstack1l11lll1l_opy_(bstack1l1l111lll_opy_)
    if bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG and bstack1lll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੥") in CONFIG[bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੦")][bstack1llllll1l1_opy_]:
      bstack1l1ll1ll1_opy_ = CONFIG[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧")][bstack1llllll1l1_opy_][bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੨")]
    import urllib
    import json
    bstack1l111ll1_opy_ = bstack1lll1l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ੩") + urllib.parse.quote(json.dumps(bstack1l1l111lll_opy_))
    browser = self.connect(bstack1l111ll1_opy_)
    return browser
except Exception as e:
    pass
def bstack1l11ll11_opy_():
    global bstack1ll1lll111_opy_
    global bstack1ll1lllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l111l11_opy_
        if not bstack1lll111l_opy_:
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
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1lll1_opy_
      bstack1ll1lll111_opy_ = True
    except Exception as e:
      pass
def bstack11l1ll1l_opy_(context, bstack1ll1ll11ll_opy_):
  try:
    context.page.evaluate(bstack1lll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ੪"), bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ੫")+ json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l_opy_ (u"ࠣࡿࢀࠦ੬"))
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ੭"), e)
def bstack1l11l1l1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1lll1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੮"), bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ੯") + json.dumps(message) + bstack1lll1l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨੰ") + json.dumps(level) + bstack1lll1l_opy_ (u"࠭ࡽࡾࠩੱ"))
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥੲ"), e)
def bstack1111l1ll1_opy_(self, url):
  global bstack1ll11l1l11_opy_
  try:
    bstack11111ll11_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll111ll_opy_.format(str(err)))
  try:
    bstack1ll11l1l11_opy_(self, url)
  except Exception as e:
    try:
      bstack11llll1l_opy_ = str(e)
      if any(err_msg in bstack11llll1l_opy_ for err_msg in bstack1llllll111_opy_):
        bstack11111ll11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll111ll_opy_.format(str(err)))
    raise e
def bstack1l11l1ll1_opy_(self):
  global bstack1lll11l111_opy_
  bstack1lll11l111_opy_ = self
  return
def bstack1l11111lll_opy_(self):
  global bstack1ll1l11l1l_opy_
  bstack1ll1l11l1l_opy_ = self
  return
def bstack1l1l1ll1ll_opy_(test_name, bstack1ll1111ll_opy_):
  global CONFIG
  if percy.bstack11ll1lll_opy_() == bstack1lll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨੳ"):
    bstack1l111ll1ll_opy_ = os.path.relpath(bstack1ll1111ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l111ll1ll_opy_)
    bstack1l11l1l11_opy_ = suite_name + bstack1lll1l_opy_ (u"ࠤ࠰ࠦੴ") + test_name
    threading.current_thread().percySessionName = bstack1l11l1l11_opy_
def bstack1l11l1l1l_opy_(self, test, *args, **kwargs):
  global bstack1ll1lllll1_opy_
  test_name = None
  bstack1ll1111ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll1111ll_opy_ = str(test.source)
  bstack1l1l1ll1ll_opy_(test_name, bstack1ll1111ll_opy_)
  bstack1ll1lllll1_opy_(self, test, *args, **kwargs)
def bstack1ll11ll11l_opy_(driver, bstack1l11l1l11_opy_):
  if not bstack111l11l1l_opy_ and bstack1l11l1l11_opy_:
      bstack11l1l111_opy_ = {
          bstack1lll1l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪੵ"): bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੶"),
          bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੷"): {
              bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸"): bstack1l11l1l11_opy_
          }
      }
      bstack1111lll1_opy_ = bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੹").format(json.dumps(bstack11l1l111_opy_))
      driver.execute_script(bstack1111lll1_opy_)
  if bstack111ll111l_opy_:
      bstack1lll1l11ll_opy_ = {
          bstack1lll1l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੺"): bstack1lll1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ੻"),
          bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੼"): {
              bstack1lll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩ੽"): bstack1l11l1l11_opy_ + bstack1lll1l_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ੾"),
              bstack1lll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੿"): bstack1lll1l_opy_ (u"ࠧࡪࡰࡩࡳࠬ઀")
          }
      }
      if bstack111ll111l_opy_.status == bstack1lll1l_opy_ (u"ࠨࡒࡄࡗࡘ࠭ઁ"):
          bstack1l1ll1111_opy_ = bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧં").format(json.dumps(bstack1lll1l11ll_opy_))
          driver.execute_script(bstack1l1ll1111_opy_)
          bstack1l1111l111_opy_(driver, bstack1lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪઃ"))
      elif bstack111ll111l_opy_.status == bstack1lll1l_opy_ (u"ࠫࡋࡇࡉࡍࠩ઄"):
          reason = bstack1lll1l_opy_ (u"ࠧࠨઅ")
          bstack1111ll11_opy_ = bstack1l11l1l11_opy_ + bstack1lll1l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧઆ")
          if bstack111ll111l_opy_.message:
              reason = str(bstack111ll111l_opy_.message)
              bstack1111ll11_opy_ = bstack1111ll11_opy_ + bstack1lll1l_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧઇ") + reason
          bstack1lll1l11ll_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫઈ")] = {
              bstack1lll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨઉ"): bstack1lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩઊ"),
              bstack1lll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩઋ"): bstack1111ll11_opy_
          }
          bstack1l1ll1111_opy_ = bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪઌ").format(json.dumps(bstack1lll1l11ll_opy_))
          driver.execute_script(bstack1l1ll1111_opy_)
          bstack1l1111l111_opy_(driver, bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ઍ"), reason)
          bstack1l11ll1lll_opy_(reason, str(bstack111ll111l_opy_), str(bstack1llll11lll_opy_), logger)
def bstack1lllll1ll_opy_(driver, test):
  if percy.bstack11ll1lll_opy_() == bstack1lll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧ઎") and percy.bstack1l1lll1l11_opy_() == bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥએ"):
      bstack1l11111111_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઐ"), None)
      bstack11l11l11l_opy_(driver, bstack1l11111111_opy_, test)
  if bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧઑ"), None) and bstack1ll111lll1_opy_(
          threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ઒"), None):
      logger.info(bstack1lll1l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧઓ"))
      bstack1ll111llll_opy_.bstack1lll1l1l1l_opy_(driver, name=test.name, path=test.source)
def bstack11l11llll_opy_(test, bstack1l11l1l11_opy_):
    try:
      data = {}
      if test:
        data[bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫઔ")] = bstack1l11l1l11_opy_
      if bstack111ll111l_opy_:
        if bstack111ll111l_opy_.status == bstack1lll1l_opy_ (u"ࠧࡑࡃࡖࡗࠬક"):
          data[bstack1lll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ")] = bstack1lll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩગ")
        elif bstack111ll111l_opy_.status == bstack1lll1l_opy_ (u"ࠪࡊࡆࡏࡌࠨઘ"):
          data[bstack1lll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઙ")] = bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬચ")
          if bstack111ll111l_opy_.message:
            data[bstack1lll1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭છ")] = str(bstack111ll111l_opy_.message)
      user = CONFIG[bstack1lll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩજ")]
      key = CONFIG[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઝ")]
      url = bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧઞ").format(user, key, bstack1l11ll11l_opy_)
      headers = {
        bstack1lll1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩટ"): bstack1lll1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧઠ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1111llll_opy_.format(str(e)))
def bstack1ll11l1ll1_opy_(test, bstack1l11l1l11_opy_):
  global CONFIG
  global bstack1ll1l11l1l_opy_
  global bstack1lll11l111_opy_
  global bstack1l11ll11l_opy_
  global bstack111ll111l_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1ll1l1l1_opy_
  global bstack1llll11l_opy_
  global bstack11ll1l111_opy_
  global bstack1lll1l1ll1_opy_
  global bstack111ll1ll_opy_
  global bstack1ll1ll1l_opy_
  try:
    if not bstack1l11ll11l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠬࢄࠧડ")), bstack1lll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઢ"), bstack1lll1l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩણ"))) as f:
        bstack1llll1ll1_opy_ = json.loads(bstack1lll1l_opy_ (u"ࠣࡽࠥત") + f.read().strip() + bstack1lll1l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫથ") + bstack1lll1l_opy_ (u"ࠥࢁࠧદ"))
        bstack1l11ll11l_opy_ = bstack1llll1ll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack111ll1ll_opy_:
    for driver in bstack111ll1ll_opy_:
      if bstack1l11ll11l_opy_ == driver.session_id:
        if test:
          bstack1lllll1ll_opy_(driver, test)
        bstack1ll11ll11l_opy_(driver, bstack1l11l1l11_opy_)
  elif bstack1l11ll11l_opy_:
    bstack11l11llll_opy_(test, bstack1l11l1l11_opy_)
  if bstack1ll1l11l1l_opy_:
    bstack1llll11l_opy_(bstack1ll1l11l1l_opy_)
  if bstack1lll11l111_opy_:
    bstack11ll1l111_opy_(bstack1lll11l111_opy_)
  if bstack1lll1111l_opy_:
    bstack1lll1l1ll1_opy_()
def bstack1lll1lll11_opy_(self, test, *args, **kwargs):
  bstack1l11l1l11_opy_ = None
  if test:
    bstack1l11l1l11_opy_ = str(test.name)
  bstack1ll11l1ll1_opy_(test, bstack1l11l1l11_opy_)
  bstack1ll1l1l1_opy_(self, test, *args, **kwargs)
def bstack1ll11lll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll111l1_opy_
  global CONFIG
  global bstack111ll1ll_opy_
  global bstack1l11ll11l_opy_
  bstack1111l111_opy_ = None
  try:
    if bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪધ"), None):
      try:
        if not bstack1l11ll11l_opy_:
          with open(os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠬࢄࠧન")), bstack1lll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭઩"), bstack1lll1l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩપ"))) as f:
            bstack1llll1ll1_opy_ = json.loads(bstack1lll1l_opy_ (u"ࠣࡽࠥફ") + f.read().strip() + bstack1lll1l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫબ") + bstack1lll1l_opy_ (u"ࠥࢁࠧભ"))
            bstack1l11ll11l_opy_ = bstack1llll1ll1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack111ll1ll_opy_:
        for driver in bstack111ll1ll_opy_:
          if bstack1l11ll11l_opy_ == driver.session_id:
            bstack1111l111_opy_ = driver
    bstack111l11lll_opy_ = bstack1ll111llll_opy_.bstack1l1l1lll11_opy_(test.tags)
    if bstack1111l111_opy_:
      threading.current_thread().isA11yTest = bstack1ll111llll_opy_.bstack1lllllll11_opy_(bstack1111l111_opy_, bstack111l11lll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack111l11lll_opy_
  except:
    pass
  bstack1ll111l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111ll111l_opy_
  bstack111ll111l_opy_ = self._test
def bstack11l11ll1_opy_():
  global bstack1l1lll11_opy_
  try:
    if os.path.exists(bstack1l1lll11_opy_):
      os.remove(bstack1l1lll11_opy_)
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧમ") + str(e))
def bstack1111l1l1_opy_():
  global bstack1l1lll11_opy_
  bstack1l11111ll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1lll11_opy_):
      with open(bstack1l1lll11_opy_, bstack1lll1l_opy_ (u"ࠬࡽࠧય")):
        pass
      with open(bstack1l1lll11_opy_, bstack1lll1l_opy_ (u"ࠨࡷࠬࠤર")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1lll11_opy_):
      bstack1l11111ll1_opy_ = json.load(open(bstack1l1lll11_opy_, bstack1lll1l_opy_ (u"ࠧࡳࡤࠪ઱")))
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪલ") + str(e))
  finally:
    return bstack1l11111ll1_opy_
def bstack11llll11_opy_(platform_index, item_index):
  global bstack1l1lll11_opy_
  try:
    bstack1l11111ll1_opy_ = bstack1111l1l1_opy_()
    bstack1l11111ll1_opy_[item_index] = platform_index
    with open(bstack1l1lll11_opy_, bstack1lll1l_opy_ (u"ࠤࡺ࠯ࠧળ")) as outfile:
      json.dump(bstack1l11111ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ઴") + str(e))
def bstack11llllll1_opy_(bstack111ll1l1l_opy_):
  global CONFIG
  bstack1l111ll11l_opy_ = bstack1lll1l_opy_ (u"ࠫࠬવ")
  if not bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ") in CONFIG:
    logger.info(bstack1lll1l_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪષ"))
  try:
    platform = CONFIG[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")][bstack111ll1l1l_opy_]
    if bstack1lll1l_opy_ (u"ࠨࡱࡶࠫહ") in platform:
      bstack1l111ll11l_opy_ += str(platform[bstack1lll1l_opy_ (u"ࠩࡲࡷࠬ઺")]) + bstack1lll1l_opy_ (u"ࠪ࠰ࠥ࠭઻")
    if bstack1lll1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴ઼ࠧ") in platform:
      bstack1l111ll11l_opy_ += str(platform[bstack1lll1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઽ")]) + bstack1lll1l_opy_ (u"࠭ࠬࠡࠩા")
    if bstack1lll1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫિ") in platform:
      bstack1l111ll11l_opy_ += str(platform[bstack1lll1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬી")]) + bstack1lll1l_opy_ (u"ࠩ࠯ࠤࠬુ")
    if bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬૂ") in platform:
      bstack1l111ll11l_opy_ += str(platform[bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ૃ")]) + bstack1lll1l_opy_ (u"ࠬ࠲ࠠࠨૄ")
    if bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫૅ") in platform:
      bstack1l111ll11l_opy_ += str(platform[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૆")]) + bstack1lll1l_opy_ (u"ࠨ࠮ࠣࠫે")
    if bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪૈ") in platform:
      bstack1l111ll11l_opy_ += str(platform[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫૉ")]) + bstack1lll1l_opy_ (u"ࠫ࠱ࠦࠧ૊")
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬો") + str(e))
  finally:
    if bstack1l111ll11l_opy_[len(bstack1l111ll11l_opy_) - 2:] == bstack1lll1l_opy_ (u"࠭ࠬࠡࠩૌ"):
      bstack1l111ll11l_opy_ = bstack1l111ll11l_opy_[:-2]
    return bstack1l111ll11l_opy_
def bstack1l11ll11ll_opy_(path, bstack1l111ll11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1111lllll_opy_ = ET.parse(path)
    bstack1l1111l11l_opy_ = bstack1111lllll_opy_.getroot()
    bstack1lll1ll11l_opy_ = None
    for suite in bstack1l1111l11l_opy_.iter(bstack1lll1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ્࠭")):
      if bstack1lll1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ૎") in suite.attrib:
        suite.attrib[bstack1lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ૏")] += bstack1lll1l_opy_ (u"ࠪࠤࠬૐ") + bstack1l111ll11l_opy_
        bstack1lll1ll11l_opy_ = suite
    bstack11lllllll1_opy_ = None
    for robot in bstack1l1111l11l_opy_.iter(bstack1lll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑")):
      bstack11lllllll1_opy_ = robot
    bstack1lll1lll_opy_ = len(bstack11lllllll1_opy_.findall(bstack1lll1l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૒")))
    if bstack1lll1lll_opy_ == 1:
      bstack11lllllll1_opy_.remove(bstack11lllllll1_opy_.findall(bstack1lll1l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ૓"))[0])
      bstack11ll11l11_opy_ = ET.Element(bstack1lll1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭૔"), attrib={bstack1lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭૕"): bstack1lll1l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ૖"), bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭૗"): bstack1lll1l_opy_ (u"ࠫࡸ࠶ࠧ૘")})
      bstack11lllllll1_opy_.insert(1, bstack11ll11l11_opy_)
      bstack11ll111l_opy_ = None
      for suite in bstack11lllllll1_opy_.iter(bstack1lll1l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૙")):
        bstack11ll111l_opy_ = suite
      bstack11ll111l_opy_.append(bstack1lll1ll11l_opy_)
      bstack1lll111ll_opy_ = None
      for status in bstack1lll1ll11l_opy_.iter(bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭૚")):
        bstack1lll111ll_opy_ = status
      bstack11ll111l_opy_.append(bstack1lll111ll_opy_)
    bstack1111lllll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬ૛") + str(e))
def bstack111ll11ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l11ll1l_opy_
  global CONFIG
  if bstack1lll1l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ૜") in options:
    del options[bstack1lll1l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ૝")]
  bstack11111ll1_opy_ = bstack1111l1l1_opy_()
  for bstack1l1lll11l_opy_ in bstack11111ll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1lll1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪ૞"), str(bstack1l1lll11l_opy_), bstack1lll1l_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨ૟"))
    bstack1l11ll11ll_opy_(path, bstack11llllll1_opy_(bstack11111ll1_opy_[bstack1l1lll11l_opy_]))
  bstack11l11ll1_opy_()
  return bstack1l1l11ll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l11ll111_opy_(self, ff_profile_dir):
  global bstack11l11lll1_opy_
  if not ff_profile_dir:
    return None
  return bstack11l11lll1_opy_(self, ff_profile_dir)
def bstack1l1lll11l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11lll1111_opy_
  bstack1lllll11ll_opy_ = []
  if bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ") in CONFIG:
    bstack1lllll11ll_opy_ = CONFIG[bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣૢ")],
      pabot_args[bstack1lll1l_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤૣ")],
      argfile,
      pabot_args.get(bstack1lll1l_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢ૤")),
      pabot_args[bstack1lll1l_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨ૥")],
      platform[0],
      bstack11lll1111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1lll1l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૦")] or [(bstack1lll1l_opy_ (u"ࠧࠨ૧"), None)]
    for platform in enumerate(bstack1lllll11ll_opy_)
  ]
def bstack1ll1ll1ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1llll1_opy_=bstack1lll1l_opy_ (u"࠭ࠧ૨")):
  global bstack111111111_opy_
  self.platform_index = platform_index
  self.bstack1ll1ll111_opy_ = bstack1ll1llll1_opy_
  bstack111111111_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1llll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l1llll_opy_
  global bstack1ll1l1l11_opy_
  bstack1l11l1llll_opy_ = copy.deepcopy(item)
  if not bstack1lll1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૩") in item.options:
    bstack1l11l1llll_opy_.options[bstack1lll1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૪")] = []
  bstack11lll1l1l_opy_ = bstack1l11l1llll_opy_.options[bstack1lll1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૫")].copy()
  for v in bstack1l11l1llll_opy_.options[bstack1lll1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૬")]:
    if bstack1lll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ૭") in v:
      bstack11lll1l1l_opy_.remove(v)
    if bstack1lll1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૮") in v:
      bstack11lll1l1l_opy_.remove(v)
    if bstack1lll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ૯") in v:
      bstack11lll1l1l_opy_.remove(v)
  bstack11lll1l1l_opy_.insert(0, bstack1lll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩ૰").format(bstack1l11l1llll_opy_.platform_index))
  bstack11lll1l1l_opy_.insert(0, bstack1lll1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨ૱").format(bstack1l11l1llll_opy_.bstack1ll1ll111_opy_))
  bstack1l11l1llll_opy_.options[bstack1lll1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૲")] = bstack11lll1l1l_opy_
  if bstack1ll1l1l11_opy_:
    bstack1l11l1llll_opy_.options[bstack1lll1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૳")].insert(0, bstack1lll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧ૴").format(bstack1ll1l1l11_opy_))
  return bstack1l1l1llll_opy_(caller_id, datasources, is_last, bstack1l11l1llll_opy_, outs_dir)
def bstack11ll1ll11_opy_(command, item_index):
  if bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૵")):
    os.environ[bstack1lll1l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ૶")] = json.dumps(CONFIG[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૷")][item_index % bstack1llll11l1l_opy_])
  global bstack1ll1l1l11_opy_
  if bstack1ll1l1l11_opy_:
    command[0] = command[0].replace(bstack1lll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૸"), bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ૹ") + str(
      item_index) + bstack1lll1l_opy_ (u"ࠪࠤࠬૺ") + bstack1ll1l1l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1lll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪૻ"),
                                    bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩૼ") + str(item_index), 1)
def bstack1lll1l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll11ll1_opy_
  bstack11ll1ll11_opy_(command, item_index)
  return bstack1ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l11l1l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll11ll1_opy_
  bstack11ll1ll11_opy_(command, item_index)
  return bstack1ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack111llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll11ll1_opy_
  bstack11ll1ll11_opy_(command, item_index)
  return bstack1ll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l111ll1l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1111111_opy_
  bstack1l11l11lll_opy_ = bstack1l1111111_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1lll1l_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭૽")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1lll1l_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ૾")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l11l11lll_opy_
def bstack1l1l1ll11l_opy_(runner, hook_name, context, element, bstack1l11l11l1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11l1llll1_opy_.bstack1lll11l1_opy_(hook_name, element)
    bstack1l11l11l1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11l1llll1_opy_.bstack111l11111_opy_(element)
      if hook_name not in [bstack1lll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ૿"), bstack1lll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ଀")] and args and hasattr(args[0], bstack1lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪଁ")):
        args[0].error_message = bstack1lll1l_opy_ (u"ࠫࠬଂ")
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧଃ").format(str(e)))
def bstack11ll11ll1_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
    bstack1l1l1ll11l_opy_(runner, name, context, runner, bstack1l11l11l1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111ll1111_opy_(bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ଄")) else context.browser
      runner.driver_initialised = bstack1lll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦଅ")
    except Exception as e:
      logger.debug(bstack1lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥ࠻ࠢࡾࢁࠬଆ").format(str(e)))
def bstack1l1l111ll1_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
    bstack1l1l1ll11l_opy_(runner, name, context, context.feature, bstack1l11l11l1_opy_, *args)
    try:
      if not bstack111l11l1l_opy_:
        bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1111_opy_(bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨଇ")) else context.browser
        if is_driver_active(bstack1111l111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1lll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦଈ")
          bstack1ll1ll11ll_opy_ = str(runner.feature.name)
          bstack11l1ll1l_opy_(context, bstack1ll1ll11ll_opy_)
          bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩଉ") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l_opy_ (u"ࠬࢃࡽࠨଊ"))
    except Exception as e:
      logger.debug(bstack1lll1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ଋ").format(str(e)))
def bstack1lll1l111l_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
    bstack1l1l1ll11l_opy_(runner, name, context, context.scenario, bstack1l11l11l1_opy_, *args)
def bstack1111ll1l_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
    bstack11l1llll1_opy_.start_test(args[0].name, args[0])
    bstack1l1l1ll11l_opy_(runner, name, context, context.scenario, bstack1l11l11l1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack111111lll_opy_.bstack1l1111l11_opy_(context, *args)
    try:
      bstack1111l111_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଌ"), context.browser)
      if is_driver_active(bstack1111l111_opy_):
        bstack1111ll111_opy_.bstack111l1l1l_opy_(bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ଍"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1lll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ଎")
        if (not bstack111l11l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll1ll11ll_opy_ = str(runner.feature.name)
          bstack1ll1ll11ll_opy_ = feature_name + bstack1lll1l_opy_ (u"ࠪࠤ࠲ࠦࠧଏ") + scenario_name
          if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨଐ"):
            bstack11l1ll1l_opy_(context, bstack1ll1ll11ll_opy_)
            bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ଑") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l_opy_ (u"࠭ࡽࡾࠩ଒"))
    except Exception as e:
      logger.debug(bstack1lll1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨଓ").format(str(e)))
def bstack11lllll1ll_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
    bstack1l1l1ll11l_opy_(runner, name, context, args[0], bstack1l11l11l1_opy_, *args)
    try:
      bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1111_opy_(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧଔ")) else context.browser
      if is_driver_active(bstack1111l111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1lll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢକ")
        bstack11l1llll1_opy_.bstack1ll11lll11_opy_(args[0])
        if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣଖ"):
          feature_name = bstack1ll1ll11ll_opy_ = str(runner.feature.name)
          bstack1ll1ll11ll_opy_ = feature_name + bstack1lll1l_opy_ (u"ࠫࠥ࠳ࠠࠨଗ") + context.scenario.name
          bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪଘ") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l_opy_ (u"࠭ࡽࡾࠩଙ"))
    except Exception as e:
      logger.debug(bstack1lll1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫଚ").format(str(e)))
def bstack11l11ll1l_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
  bstack11l1llll1_opy_.bstack1ll1llll_opy_(args[0])
  try:
    bstack1l111l11_opy_ = args[0].status.name
    bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧଛ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1111l111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1lll1l_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩଜ")
        feature_name = bstack1ll1ll11ll_opy_ = str(runner.feature.name)
        bstack1ll1ll11ll_opy_ = feature_name + bstack1lll1l_opy_ (u"ࠪࠤ࠲ࠦࠧଝ") + context.scenario.name
        bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩଞ") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l_opy_ (u"ࠬࢃࡽࠨଟ"))
    if str(bstack1l111l11_opy_).lower() == bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ଠ"):
      bstack1ll1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠧࠨଡ")
      bstack1llll1111_opy_ = bstack1lll1l_opy_ (u"ࠨࠩଢ")
      bstack1l1llll11l_opy_ = bstack1lll1l_opy_ (u"ࠩࠪଣ")
      try:
        import traceback
        bstack1ll1l1lll_opy_ = runner.exception.__class__.__name__
        bstack1l11ll1l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1llll1111_opy_ = bstack1lll1l_opy_ (u"ࠪࠤࠬତ").join(bstack1l11ll1l1l_opy_)
        bstack1l1llll11l_opy_ = bstack1l11ll1l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1l11ll1_opy_.format(str(e)))
      bstack1ll1l1lll_opy_ += bstack1l1llll11l_opy_
      bstack1l11l1l1_opy_(context, json.dumps(str(args[0].name) + bstack1lll1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥଥ") + str(bstack1llll1111_opy_)),
                          bstack1lll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦଦ"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦଧ"):
        bstack1ll1l11ll1_opy_(getattr(context, bstack1lll1l_opy_ (u"ࠧࡱࡣࡪࡩࠬନ"), None), bstack1lll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ଩"), bstack1ll1l1lll_opy_)
        bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧପ") + json.dumps(str(args[0].name) + bstack1lll1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤଫ") + str(bstack1llll1111_opy_)) + bstack1lll1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫବ"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥଭ"):
        bstack1l1111l111_opy_(bstack1111l111_opy_, bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ମ"), bstack1lll1l_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦଯ") + str(bstack1ll1l1lll_opy_))
    else:
      bstack1l11l1l1_opy_(context, bstack1lll1l_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤର"), bstack1lll1l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ଱"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣଲ"):
        bstack1ll1l11ll1_opy_(getattr(context, bstack1lll1l_opy_ (u"ࠫࡵࡧࡧࡦࠩଳ"), None), bstack1lll1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ଴"))
      bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫଵ") + json.dumps(str(args[0].name) + bstack1lll1l_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦଶ")) + bstack1lll1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧଷ"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢସ"):
        bstack1l1111l111_opy_(bstack1111l111_opy_, bstack1lll1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥହ"))
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪ଺").format(str(e)))
  bstack1l1l1ll11l_opy_(runner, name, context, args[0], bstack1l11l11l1_opy_, *args)
def bstack1ll1l1l111_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
  bstack11l1llll1_opy_.end_test(args[0])
  try:
    bstack111l1l11l_opy_ = args[0].status.name
    bstack1111l111_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ଻"), context.browser)
    bstack111111lll_opy_.bstack1111l1111_opy_(bstack1111l111_opy_)
    if str(bstack111l1l11l_opy_).lower() == bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ଼࠭"):
      bstack1ll1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠧࠨଽ")
      bstack1llll1111_opy_ = bstack1lll1l_opy_ (u"ࠨࠩା")
      bstack1l1llll11l_opy_ = bstack1lll1l_opy_ (u"ࠩࠪି")
      try:
        import traceback
        bstack1ll1l1lll_opy_ = runner.exception.__class__.__name__
        bstack1l11ll1l1l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1llll1111_opy_ = bstack1lll1l_opy_ (u"ࠪࠤࠬୀ").join(bstack1l11ll1l1l_opy_)
        bstack1l1llll11l_opy_ = bstack1l11ll1l1l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1l11ll1_opy_.format(str(e)))
      bstack1ll1l1lll_opy_ += bstack1l1llll11l_opy_
      bstack1l11l1l1_opy_(context, json.dumps(str(args[0].name) + bstack1lll1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥୁ") + str(bstack1llll1111_opy_)),
                          bstack1lll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦୂ"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣୃ") or runner.driver_initialised == bstack1lll1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧୄ"):
        bstack1ll1l11ll1_opy_(getattr(context, bstack1lll1l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭୅"), None), bstack1lll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ୆"), bstack1ll1l1lll_opy_)
        bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨେ") + json.dumps(str(args[0].name) + bstack1lll1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥୈ") + str(bstack1llll1111_opy_)) + bstack1lll1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ୉"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ୊") or runner.driver_initialised == bstack1lll1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧୋ"):
        bstack1l1111l111_opy_(bstack1111l111_opy_, bstack1lll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨୌ"), bstack1lll1l_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ୍") + str(bstack1ll1l1lll_opy_))
    else:
      bstack1l11l1l1_opy_(context, bstack1lll1l_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ୎"), bstack1lll1l_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ୏"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ୐") or runner.driver_initialised == bstack1lll1l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭୑"):
        bstack1ll1l11ll1_opy_(getattr(context, bstack1lll1l_opy_ (u"ࠧࡱࡣࡪࡩࠬ୒"), None), bstack1lll1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ୓"))
      bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ୔") + json.dumps(str(args[0].name) + bstack1lll1l_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ୕")) + bstack1lll1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪୖ"))
      if runner.driver_initialised == bstack1lll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢୗ") or runner.driver_initialised == bstack1lll1l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭୘"):
        bstack1l1111l111_opy_(bstack1111l111_opy_, bstack1lll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ୙"))
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ୚").format(str(e)))
  bstack1l1l1ll11l_opy_(runner, name, context, context.scenario, bstack1l11l11l1_opy_, *args)
  threading.current_thread().current_test_uuid = None
def bstack1lll11ll1_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
    bstack1l1l1ll11l_opy_(runner, name, context, context.scenario, bstack1l11l11l1_opy_, *args)
def bstack1l11ll11l1_opy_(runner, name, context, bstack1l11l11l1_opy_, *args):
    try:
      bstack1111l111_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ୛"), context.browser)
      if context.failed is True:
        bstack1l11lll1l1_opy_ = []
        bstack1llll1l1_opy_ = []
        bstack111ll1lll_opy_ = []
        bstack1l1llll1l_opy_ = bstack1lll1l_opy_ (u"ࠪࠫଡ଼")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l11lll1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11ll1l1l_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11l111_opy_ = bstack1lll1l_opy_ (u"ࠫࠥ࠭ଢ଼").join(bstack1l11ll1l1l_opy_)
            bstack1llll1l1_opy_.append(bstack1ll11l111_opy_)
            bstack111ll1lll_opy_.append(bstack1l11ll1l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l11ll1_opy_.format(str(e)))
        bstack1ll1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠬ࠭୞")
        for i in range(len(bstack1l11lll1l1_opy_)):
          bstack1ll1l1lll_opy_ += bstack1l11lll1l1_opy_[i] + bstack111ll1lll_opy_[i] + bstack1lll1l_opy_ (u"࠭࡜࡯ࠩୟ")
        bstack1l1llll1l_opy_ = bstack1lll1l_opy_ (u"ࠧࠡࠩୠ").join(bstack1llll1l1_opy_)
        if runner.driver_initialised in [bstack1lll1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤୡ"), bstack1lll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨୢ")]:
          bstack1l11l1l1_opy_(context, bstack1l1llll1l_opy_, bstack1lll1l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤୣ"))
          bstack1ll1l11ll1_opy_(getattr(context, bstack1lll1l_opy_ (u"ࠫࡵࡧࡧࡦࠩ୤"), None), bstack1lll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ୥"), bstack1ll1l1lll_opy_)
          bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ୦") + json.dumps(bstack1l1llll1l_opy_) + bstack1lll1l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ୧"))
          bstack1l1111l111_opy_(bstack1111l111_opy_, bstack1lll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ୨"), bstack1lll1l_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢ୩") + str(bstack1ll1l1lll_opy_))
          bstack1ll11111ll_opy_ = bstack1l1l1ll1l1_opy_(bstack1l1llll1l_opy_, runner.feature.name, logger)
          if (bstack1ll11111ll_opy_ != None):
            bstack11ll111ll_opy_.append(bstack1ll11111ll_opy_)
      else:
        if runner.driver_initialised in [bstack1lll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ୪"), bstack1lll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ୫")]:
          bstack1l11l1l1_opy_(context, bstack1lll1l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ୬") + str(runner.feature.name) + bstack1lll1l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ୭"), bstack1lll1l_opy_ (u"ࠢࡪࡰࡩࡳࠧ୮"))
          bstack1ll1l11ll1_opy_(getattr(context, bstack1lll1l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭୯"), None), bstack1lll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ୰"))
          bstack1111l111_opy_.execute_script(bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨୱ") + json.dumps(bstack1lll1l_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢ୲") + str(runner.feature.name) + bstack1lll1l_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ୳")) + bstack1lll1l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ୴"))
          bstack1l1111l111_opy_(bstack1111l111_opy_, bstack1lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ୵"))
          bstack1ll11111ll_opy_ = bstack1l1l1ll1l1_opy_(bstack1l1llll1l_opy_, runner.feature.name, logger)
          if (bstack1ll11111ll_opy_ != None):
            bstack11ll111ll_opy_.append(bstack1ll11111ll_opy_)
    except Exception as e:
      logger.debug(bstack1lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ୶").format(str(e)))
    bstack1l1l1ll11l_opy_(runner, name, context, context.feature, bstack1l11l11l1_opy_, *args)
def bstack1l11l1l11l_opy_(self, name, context, *args):
  if bstack1lll111l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1llll11l1l_opy_
    bstack1l1ll1ll11_opy_ = CONFIG[bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୷")][platform_index]
    os.environ[bstack1lll1l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ୸")] = json.dumps(bstack1l1ll1ll11_opy_)
  global bstack1l11l11l1_opy_
  if not hasattr(self, bstack1lll1l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩ୹")):
    self.driver_initialised = None
  bstack1l11l111l1_opy_ = {
      bstack1lll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ୺"): bstack11ll11ll1_opy_,
      bstack1lll1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ୻"): bstack1l1l111ll1_opy_,
      bstack1lll1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫ୼"): bstack1lll1l111l_opy_,
      bstack1lll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ୽"): bstack1111ll1l_opy_,
      bstack1lll1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧ୾"): bstack11lllll1ll_opy_,
      bstack1lll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧ୿"): bstack11l11ll1l_opy_,
      bstack1lll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ஀"): bstack1ll1l1l111_opy_,
      bstack1lll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨ஁"): bstack1lll11ll1_opy_,
      bstack1lll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ஂ"): bstack1l11ll11l1_opy_,
      bstack1lll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪஃ"): lambda *args: bstack1l1l1ll11l_opy_(*args, self)
  }
  handler = bstack1l11l111l1_opy_.get(name, bstack1l11l11l1_opy_)
  handler(self, name, context, bstack1l11l11l1_opy_, *args)
  if name in [bstack1lll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ஄"), bstack1lll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪஅ"), bstack1lll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ஆ")]:
    try:
      bstack1111l111_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1111_opy_(bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪஇ")) else context.browser
      bstack1ll11ll11_opy_ = (
        (name == bstack1lll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨஈ") and self.driver_initialised == bstack1lll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥஉ")) or
        (name == bstack1lll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧஊ") and self.driver_initialised == bstack1lll1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ஋")) or
        (name == bstack1lll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ஌") and self.driver_initialised in [bstack1lll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ஍"), bstack1lll1l_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦஎ")]) or
        (name == bstack1lll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩஏ") and self.driver_initialised == bstack1lll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦஐ"))
      )
      if bstack1ll11ll11_opy_:
        self.driver_initialised = None
        bstack1111l111_opy_.quit()
    except Exception:
      pass
def bstack1lll11l1ll_opy_(config, startdir):
  return bstack1lll1l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧ஑").format(bstack1lll1l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢஒ"))
notset = Notset()
def bstack1ll111l11l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11l1l1ll_opy_
  if str(name).lower() == bstack1lll1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩஓ"):
    return bstack1lll1l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤஔ")
  else:
    return bstack11l1l1ll_opy_(self, name, default, skip)
def bstack1ll1ll1ll1_opy_(item, when):
  global bstack1l11111l1l_opy_
  try:
    bstack1l11111l1l_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1ll111l1_opy_():
  return
def bstack11l1l1l11_opy_(type, name, status, reason, bstack1l1l1ll111_opy_, bstack1l11l1lll1_opy_):
  bstack11l1l111_opy_ = {
    bstack1lll1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫக"): type,
    bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ஖"): {}
  }
  if type == bstack1lll1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ஗"):
    bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ஘")][bstack1lll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧங")] = bstack1l1l1ll111_opy_
    bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬச")][bstack1lll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨ஛")] = json.dumps(str(bstack1l11l1lll1_opy_))
  if type == bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬஜ"):
    bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ஝")][bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫஞ")] = name
  if type == bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪட"):
    bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ஠")][bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ஡")] = status
    if status == bstack1lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ஢"):
      bstack11l1l111_opy_[bstack1lll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧண")][bstack1lll1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬத")] = json.dumps(str(reason))
  bstack1111lll1_opy_ = bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ஥").format(json.dumps(bstack11l1l111_opy_))
  return bstack1111lll1_opy_
def bstack1l11l1ll11_opy_(driver_command, response):
    if driver_command == bstack1lll1l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ஦"):
        bstack1111ll111_opy_.bstack1lll11ll1l_opy_({
            bstack1lll1l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ஧"): response[bstack1lll1l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨந")],
            bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪன"): bstack1111ll111_opy_.current_test_uuid()
        })
def bstack1ll111ll1_opy_(item, call, rep):
  global bstack1111l1l11_opy_
  global bstack111ll1ll_opy_
  global bstack111l11l1l_opy_
  name = bstack1lll1l_opy_ (u"ࠫࠬப")
  try:
    if rep.when == bstack1lll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ஫"):
      bstack1l11ll11l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack111l11l1l_opy_:
          name = str(rep.nodeid)
          bstack1llll1l1ll_opy_ = bstack11l1l1l11_opy_(bstack1lll1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ஬"), name, bstack1lll1l_opy_ (u"ࠧࠨ஭"), bstack1lll1l_opy_ (u"ࠨࠩம"), bstack1lll1l_opy_ (u"ࠩࠪய"), bstack1lll1l_opy_ (u"ࠪࠫர"))
          threading.current_thread().bstack1l1111111l_opy_ = name
          for driver in bstack111ll1ll_opy_:
            if bstack1l11ll11l_opy_ == driver.session_id:
              driver.execute_script(bstack1llll1l1ll_opy_)
      except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫற").format(str(e)))
      try:
        bstack1l1l11l1ll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1lll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ல"):
          status = bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ள") if rep.outcome.lower() == bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧழ") else bstack1lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨவ")
          reason = bstack1lll1l_opy_ (u"ࠩࠪஶ")
          if status == bstack1lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪஷ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1lll1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩஸ") if status == bstack1lll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬஹ") else bstack1lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ஺")
          data = name + bstack1lll1l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ஻") if status == bstack1lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ஼") else name + bstack1lll1l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ஽") + reason
          bstack1l111lllll_opy_ = bstack11l1l1l11_opy_(bstack1lll1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬா"), bstack1lll1l_opy_ (u"ࠫࠬி"), bstack1lll1l_opy_ (u"ࠬ࠭ீ"), bstack1lll1l_opy_ (u"࠭ࠧு"), level, data)
          for driver in bstack111ll1ll_opy_:
            if bstack1l11ll11l_opy_ == driver.session_id:
              driver.execute_script(bstack1l111lllll_opy_)
      except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫூ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1lll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ௃").format(str(e)))
  bstack1111l1l11_opy_(item, call, rep)
def bstack11l11l11l_opy_(driver, bstack11ll1lll1_opy_, test=None):
  global bstack1llll11lll_opy_
  if test != None:
    bstack1111l1ll_opy_ = getattr(test, bstack1lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ௄"), None)
    bstack1l111l11ll_opy_ = getattr(test, bstack1lll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ௅"), None)
    PercySDK.screenshot(driver, bstack11ll1lll1_opy_, bstack1111l1ll_opy_=bstack1111l1ll_opy_, bstack1l111l11ll_opy_=bstack1l111l11ll_opy_, bstack1l1lll111_opy_=bstack1llll11lll_opy_)
  else:
    PercySDK.screenshot(driver, bstack11ll1lll1_opy_)
def bstack11ll11lll_opy_(driver):
  if bstack1ll11l11ll_opy_.bstack11l1l1l1l_opy_() is True or bstack1ll11l11ll_opy_.capturing() is True:
    return
  bstack1ll11l11ll_opy_.bstack1l11l11ll_opy_()
  while not bstack1ll11l11ll_opy_.bstack11l1l1l1l_opy_():
    bstack1lll111lll_opy_ = bstack1ll11l11ll_opy_.bstack1l1111ll1l_opy_()
    bstack11l11l11l_opy_(driver, bstack1lll111lll_opy_)
  bstack1ll11l11ll_opy_.bstack1lll1l11_opy_()
def bstack1l1llll1_opy_(sequence, driver_command, response = None, bstack11lllll1l1_opy_ = None, args = None):
    try:
      if sequence != bstack1lll1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫெ"):
        return
      if percy.bstack11ll1lll_opy_() == bstack1lll1l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦே"):
        return
      bstack1lll111lll_opy_ = bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩை"), None)
      for command in bstack111111ll_opy_:
        if command == driver_command:
          for driver in bstack111ll1ll_opy_:
            bstack11ll11lll_opy_(driver)
      bstack1lll1ll1ll_opy_ = percy.bstack1l1lll1l11_opy_()
      if driver_command in bstack1l1l1l1l_opy_[bstack1lll1ll1ll_opy_]:
        bstack1ll11l11ll_opy_.bstack1ll1ll1l1_opy_(bstack1lll111lll_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1llll111_opy_(framework_name):
  if bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ௉")):
      return
  bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬொ"), True)
  global bstack1ll1lllll_opy_
  global bstack1ll1lll111_opy_
  global bstack1lll1l1l_opy_
  bstack1ll1lllll_opy_ = framework_name
  logger.info(bstack11lll1l11_opy_.format(bstack1ll1lllll_opy_.split(bstack1lll1l_opy_ (u"ࠩ࠰ࠫோ"))[0]))
  bstack1ll111lll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1lll111l_opy_:
      Service.start = bstack11ll11111_opy_
      Service.stop = bstack1l11l11l1l_opy_
      webdriver.Remote.get = bstack1111l1ll1_opy_
      WebDriver.close = bstack1ll1111l1l_opy_
      WebDriver.quit = bstack11l1ll111_opy_
      webdriver.Remote.__init__ = bstack1lll1l111_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1lll111l_opy_:
        webdriver.Remote.__init__ = bstack1ll1ll1lll_opy_
    WebDriver.execute = bstack1llllll1ll_opy_
    bstack1ll1lll111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1lll111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1llll1llll_opy_
  except Exception as e:
    pass
  bstack1l11ll11_opy_()
  if not bstack1ll1lll111_opy_:
    bstack11111l1ll_opy_(bstack1lll1l_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧௌ"), bstack111l1l11_opy_)
  if bstack11111l1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11l11111l_opy_
    except Exception as e:
      logger.error(bstack111llll1_opy_.format(str(e)))
  if bstack1ll1l1llll_opy_():
    bstack1llll111l_opy_(CONFIG, logger)
  if (bstack1lll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ்ࠪ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11ll1lll_opy_() == bstack1lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥ௎"):
          bstack111lll1l_opy_(bstack1l1llll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l11ll111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l11111lll_opy_
      except Exception as e:
        logger.warn(bstack11l11l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l11l1ll1_opy_
      except Exception as e:
        logger.debug(bstack1llll1l11_opy_ + str(e))
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11l11l1l_opy_)
    Output.start_test = bstack1l11l1l1l_opy_
    Output.end_test = bstack1lll1lll11_opy_
    TestStatus.__init__ = bstack1ll11lll1_opy_
    QueueItem.__init__ = bstack1ll1ll1ll_opy_
    pabot._create_items = bstack1l1lll11l1_opy_
    try:
      from pabot import __version__ as bstack1l111111_opy_
      if version.parse(bstack1l111111_opy_) >= version.parse(bstack1lll1l_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭௏")):
        pabot._run = bstack111llll11_opy_
      elif version.parse(bstack1l111111_opy_) >= version.parse(bstack1lll1l_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧௐ")):
        pabot._run = bstack1l11l1l1l1_opy_
      else:
        pabot._run = bstack1lll1l1l1_opy_
    except Exception as e:
      pabot._run = bstack1lll1l1l1_opy_
    pabot._create_command_for_execution = bstack1l1llll11_opy_
    pabot._report_results = bstack111ll11ll_opy_
  if bstack1lll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௑") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack1lll11lll1_opy_)
    Runner.run_hook = bstack1l11l1l11l_opy_
    Step.run = bstack1l111ll1l1_opy_
  if bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௒") in str(framework_name).lower():
    if not bstack1lll111l_opy_:
      return
    try:
      if percy.bstack11ll1lll_opy_() == bstack1lll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣ௓"):
          bstack111lll1l_opy_(bstack1l1llll1_opy_)
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
def bstack1l1l11l111_opy_():
  global CONFIG
  if bstack1lll1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ௔") in CONFIG and int(CONFIG[bstack1lll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ௕")]) > 1:
    logger.warn(bstack1111ll1l1_opy_)
def bstack11111l111_opy_(arg, bstack1l1lll1l1_opy_, bstack1l11111l_opy_=None):
  global CONFIG
  global bstack1l1lll1l_opy_
  global bstack1111ll11l_opy_
  global bstack1lll111l_opy_
  global bstack1l1l111l_opy_
  bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௖")
  if bstack1l1lll1l1_opy_ and isinstance(bstack1l1lll1l1_opy_, str):
    bstack1l1lll1l1_opy_ = eval(bstack1l1lll1l1_opy_)
  CONFIG = bstack1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧௗ")]
  bstack1l1lll1l_opy_ = bstack1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ௘")]
  bstack1111ll11l_opy_ = bstack1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ௙")]
  bstack1lll111l_opy_ = bstack1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭௚")]
  bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ௛"), bstack1lll111l_opy_)
  os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ௜")] = bstack1l11lll11l_opy_
  os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ௝")] = json.dumps(CONFIG)
  os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ௞")] = bstack1l1lll1l_opy_
  os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௟")] = str(bstack1111ll11l_opy_)
  os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨ௠")] = str(True)
  if bstack1llll11ll_opy_(arg, [bstack1lll1l_opy_ (u"ࠪ࠱ࡳ࠭௡"), bstack1lll1l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ௢")]) != -1:
    os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭௣")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1l1111_opy_)
    return
  bstack1lll11ll11_opy_()
  global bstack11lll11ll_opy_
  global bstack1llll11lll_opy_
  global bstack11lll1111_opy_
  global bstack1ll1l1l11_opy_
  global bstack1llllll11_opy_
  global bstack1lll1l1l_opy_
  global bstack1lll111111_opy_
  arg.append(bstack1lll1l_opy_ (u"ࠨ࠭ࡘࠤ௤"))
  arg.append(bstack1lll1l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥ௥"))
  arg.append(bstack1lll1l_opy_ (u"ࠣ࠯࡚ࠦ௦"))
  arg.append(bstack1lll1l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣ௧"))
  global bstack1lll11l11l_opy_
  global bstack11l1l11ll_opy_
  global bstack1111111ll_opy_
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
    bstack1111111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1llll1ll11_opy_(CONFIG) and bstack11lllll1l_opy_():
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
    logger.debug(bstack1lll1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ௨"))
  bstack11lll1111_opy_ = CONFIG.get(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ௩"), {}).get(bstack1lll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௪"))
  bstack1lll111111_opy_ = True
  bstack1l1llll111_opy_(bstack1l111llll_opy_)
  os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ௫")] = CONFIG[bstack1lll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ௬")]
  os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ௭")] = CONFIG[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ௮")]
  os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭௯")] = bstack1lll111l_opy_.__str__()
  from _pytest.config import main as bstack1llllll11l_opy_
  bstack1lll11111l_opy_ = []
  try:
    bstack1111lll1l_opy_ = bstack1llllll11l_opy_(arg)
    if bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ௰") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll11ll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll11111l_opy_.append(bstack1ll11ll1ll_opy_)
    try:
      bstack11l1ll1ll_opy_ = (bstack1lll11111l_opy_, int(bstack1111lll1l_opy_))
      bstack1l11111l_opy_.append(bstack11l1ll1ll_opy_)
    except:
      bstack1l11111l_opy_.append((bstack1lll11111l_opy_, bstack1111lll1l_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1lll11111l_opy_.append({bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௱"): bstack1lll1l_opy_ (u"࠭ࡐࡳࡱࡦࡩࡸࡹࠠࠨ௲") + os.environ.get(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ௳")), bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ௴"): traceback.format_exc(), bstack1lll1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ௵"): int(os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ௶")))})
    bstack1l11111l_opy_.append((bstack1lll11111l_opy_, 1))
def bstack1ll11l111l_opy_(arg):
  global bstack1l1l1ll1_opy_
  bstack1l1llll111_opy_(bstack1ll1l11l_opy_)
  os.environ[bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ௷")] = str(bstack1111ll11l_opy_)
  from behave.__main__ import main as bstack1l1lll1ll_opy_
  status_code = bstack1l1lll1ll_opy_(arg)
  if status_code != 0:
    bstack1l1l1ll1_opy_ = status_code
def bstack11ll111l1_opy_():
  logger.info(bstack1lllll111l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ௸"), help=bstack1lll1l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ௹"))
  parser.add_argument(bstack1lll1l_opy_ (u"ࠧ࠮ࡷࠪ௺"), bstack1lll1l_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ௻"), help=bstack1lll1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ௼"))
  parser.add_argument(bstack1lll1l_opy_ (u"ࠪ࠱ࡰ࠭௽"), bstack1lll1l_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ௾"), help=bstack1lll1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭௿"))
  parser.add_argument(bstack1lll1l_opy_ (u"࠭࠭ࡧࠩఀ"), bstack1lll1l_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬఁ"), help=bstack1lll1l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧం"))
  bstack11l1l1111_opy_ = parser.parse_args()
  try:
    bstack111111l11_opy_ = bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ః")
    if bstack11l1l1111_opy_.framework and bstack11l1l1111_opy_.framework not in (bstack1lll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪఄ"), bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬఅ")):
      bstack111111l11_opy_ = bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫఆ")
    bstack1ll1ll11l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111111l11_opy_)
    bstack1l11llll1l_opy_ = open(bstack1ll1ll11l1_opy_, bstack1lll1l_opy_ (u"࠭ࡲࠨఇ"))
    bstack1111llll1_opy_ = bstack1l11llll1l_opy_.read()
    bstack1l11llll1l_opy_.close()
    if bstack11l1l1111_opy_.username:
      bstack1111llll1_opy_ = bstack1111llll1_opy_.replace(bstack1lll1l_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧఈ"), bstack11l1l1111_opy_.username)
    if bstack11l1l1111_opy_.key:
      bstack1111llll1_opy_ = bstack1111llll1_opy_.replace(bstack1lll1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪఉ"), bstack11l1l1111_opy_.key)
    if bstack11l1l1111_opy_.framework:
      bstack1111llll1_opy_ = bstack1111llll1_opy_.replace(bstack1lll1l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪఊ"), bstack11l1l1111_opy_.framework)
    file_name = bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ఋ")
    file_path = os.path.abspath(file_name)
    bstack11l1l1l1_opy_ = open(file_path, bstack1lll1l_opy_ (u"ࠫࡼ࠭ఌ"))
    bstack11l1l1l1_opy_.write(bstack1111llll1_opy_)
    bstack11l1l1l1_opy_.close()
    logger.info(bstack111l1ll11_opy_)
    try:
      os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ఍")] = bstack11l1l1111_opy_.framework if bstack11l1l1111_opy_.framework != None else bstack1lll1l_opy_ (u"ࠨࠢఎ")
      config = yaml.safe_load(bstack1111llll1_opy_)
      config[bstack1lll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧఏ")] = bstack1lll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧఐ")
      bstack1l11l1ll1l_opy_(bstack1ll111l111_opy_, config)
    except Exception as e:
      logger.debug(bstack1ll111l1l1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1ll1111_opy_.format(str(e)))
def bstack1l11l1ll1l_opy_(bstack1lll111l1l_opy_, config, bstack111l1l1ll_opy_={}):
  global bstack1lll111l_opy_
  global bstack1l1lll1l1l_opy_
  global bstack1l1l111l_opy_
  if not config:
    return
  bstack1l1111lll_opy_ = bstack1ll11l1l_opy_ if not bstack1lll111l_opy_ else (
    bstack1ll11l1lll_opy_ if bstack1lll1l_opy_ (u"ࠩࡤࡴࡵ࠭఑") in config else bstack1ll11l1111_opy_)
  bstack1llll11111_opy_ = False
  bstack1l111l11l1_opy_ = False
  if bstack1lll111l_opy_ is True:
      if bstack1lll1l_opy_ (u"ࠪࡥࡵࡶࠧఒ") in config:
          bstack1llll11111_opy_ = True
      else:
          bstack1l111l11l1_opy_ = True
  bstack1l1ll1lll1_opy_ = bstack1llllllll1_opy_.bstack11llll1ll_opy_(config, bstack1l1lll1l1l_opy_)
  data = {
    bstack1lll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ఓ"): config[bstack1lll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧఔ")],
    bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩక"): config[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪఖ")],
    bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬగ"): bstack1lll111l1l_opy_,
    bstack1lll1l_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ఘ"): os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬఙ"), bstack1l1lll1l1l_opy_),
    bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭చ"): bstack1lll11l1l_opy_,
    bstack1lll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧఛ"): bstack1llll11ll1_opy_(),
    bstack1lll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩజ"): {
      bstack1lll1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬఝ"): str(config[bstack1lll1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨఞ")]) if bstack1lll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩట") in config else bstack1lll1l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦఠ"),
      bstack1lll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࡜ࡥࡳࡵ࡬ࡳࡳ࠭డ"): sys.version,
      bstack1lll1l_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧఢ"): bstack1l1l11ll_opy_(os.getenv(bstack1lll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣణ"), bstack1lll1l_opy_ (u"ࠢࠣత"))),
      bstack1lll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪథ"): bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩద"),
      bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫధ"): bstack1l1111lll_opy_,
      bstack1lll1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩన"): bstack1l1ll1lll1_opy_,
      bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫ఩"): os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫప")],
      bstack1lll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪఫ"): bstack11ll1ll1_opy_(os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪబ"), bstack1l1lll1l1l_opy_)),
      bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬభ"): config[bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭మ")] if config[bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧయ")] else bstack1lll1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨర"),
      bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨఱ"): str(config[bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩల")]) if bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪళ") in config else bstack1lll1l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥఴ"),
      bstack1lll1l_opy_ (u"ࠪࡳࡸ࠭వ"): sys.platform,
      bstack1lll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭శ"): socket.gethostname(),
      bstack1lll1l_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧష"): bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨస"))
    }
  }
  if not bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧహ")) is None:
    data[bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ఺")][bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡑࡪࡺࡡࡥࡣࡷࡥࠬ఻")] = {
      bstack1lll1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰ఼ࠪ"): bstack1lll1l_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩఽ"),
      bstack1lll1l_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬా"): bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ి")),
      bstack1lll1l_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࡎࡶ࡯ࡥࡩࡷ࠭ీ"): bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡐࡲࠫు"))
    }
  if bstack1lll111l1l_opy_ == bstack11ll1l1ll_opy_:
    data[bstack1lll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬూ")][bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࠨృ")] = bstack1ll1l1ll_opy_(config)
    data[bstack1lll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧౄ")][bstack1lll1l_opy_ (u"ࠬ࡯ࡳࡑࡧࡵࡧࡾࡇࡵࡵࡱࡈࡲࡦࡨ࡬ࡦࡦࠪ౅")] = percy.bstack1l11lll11_opy_
    data[bstack1lll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩె")][bstack1lll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡈࡵࡪ࡮ࡧࡍࡩ࠭ే")] = percy.bstack111l11ll1_opy_
    file_path = bstack1lll1l_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦ࠰ࡷࡼࡹ࠭ై")
    with open(file_path, bstack1lll1l_opy_ (u"ࠩࡺࠫ౉")) as file:
        file.write(bstack111l11l1_opy_ (u"ࠥࡘ࡭࡯ࡳࠡ࡫ࡶࠤࡦࠦࡳࡢ࡯ࡳࡰࡪࠦࡻࡥࡣࡷࡥࡠ࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩࡠ࡟ࠬ࡯ࡳࡑࡧࡵࡧࡾࡇࡵࡵࡱࡈࡲࡦࡨ࡬ࡦࡦࠪࡡࢂ࠴࡜࡯ࠤొ"))
        file.write(bstack111l11l1_opy_ (u"ࠦ࡞ࡵࡵࠡࡽࡧࡥࡹࡧ࡛ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫࡢࡡࠧࡱࡧࡵࡧࡾࡈࡵࡪ࡮ࡧࡍࡩ࠭࡝ࡾ࠰࡟ࡲࠧో"))
  update(data[bstack1lll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨౌ")], bstack111l1l1ll_opy_)
  try:
    response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"࠭ࡐࡐࡕࡗ్ࠫ"), bstack1l11lll1_opy_(bstack1lll1l11l1_opy_), data, {
      bstack1lll1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ౎"): (config[bstack1lll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ౏")], config[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ౐")])
    })
    if response:
      logger.debug(bstack1l1l11111l_opy_.format(bstack1lll111l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111lll1ll_opy_.format(str(e)))
def bstack1l1l11ll_opy_(framework):
  return bstack1lll1l_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ౑").format(str(framework), __version__) if framework else bstack1lll1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ౒").format(
    __version__)
def bstack1lll11ll11_opy_():
  global CONFIG
  global bstack1lll111ll1_opy_
  if bool(CONFIG):
    return
  try:
    bstack11l111111_opy_()
    logger.debug(bstack1ll11lllll_opy_.format(str(CONFIG)))
    bstack1lll111ll1_opy_ = bstack1lll111l1_opy_.bstack1l1ll11l_opy_(CONFIG, bstack1lll111ll1_opy_)
    bstack1ll111lll_opy_()
  except Exception as e:
    logger.error(bstack1lll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤ౓") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l111ll11_opy_
  atexit.register(bstack1l11lllll1_opy_)
  signal.signal(signal.SIGINT, bstack1ll1l111ll_opy_)
  signal.signal(signal.SIGTERM, bstack1ll1l111ll_opy_)
def bstack1l111ll11_opy_(exctype, value, traceback):
  global bstack111ll1ll_opy_
  try:
    for driver in bstack111ll1ll_opy_:
      bstack1l1111l111_opy_(driver, bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౔"), bstack1lll1l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰౕࠥ") + str(value))
  except Exception:
    pass
  bstack1ll111ll11_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll111ll11_opy_(message=bstack1lll1l_opy_ (u"ࠨౖࠩ"), bstack1ll1lll1l1_opy_ = False):
  global CONFIG
  bstack1l1l111ll_opy_ = bstack1lll1l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫ౗") if bstack1ll1lll1l1_opy_ else bstack1lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩౘ")
  try:
    if message:
      bstack111l1l1ll_opy_ = {
        bstack1l1l111ll_opy_ : str(message)
      }
      bstack1l11l1ll1l_opy_(bstack11ll1l1ll_opy_, CONFIG, bstack111l1l1ll_opy_)
    else:
      bstack1l11l1ll1l_opy_(bstack11ll1l1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l11l11_opy_.format(str(e)))
def bstack1l111l1l1_opy_(bstack1ll111l1l_opy_, size):
  bstack11111lll_opy_ = []
  while len(bstack1ll111l1l_opy_) > size:
    bstack1l11111ll_opy_ = bstack1ll111l1l_opy_[:size]
    bstack11111lll_opy_.append(bstack1l11111ll_opy_)
    bstack1ll111l1l_opy_ = bstack1ll111l1l_opy_[size:]
  bstack11111lll_opy_.append(bstack1ll111l1l_opy_)
  return bstack11111lll_opy_
def bstack1ll111ll1l_opy_(args):
  if bstack1lll1l_opy_ (u"ࠫ࠲ࡳࠧౙ") in args and bstack1lll1l_opy_ (u"ࠬࡶࡤࡣࠩౚ") in args:
    return True
  return False
def run_on_browserstack(bstack1l1ll111l_opy_=None, bstack1l11111l_opy_=None, bstack1lll1llll1_opy_=False):
  global CONFIG
  global bstack1l1lll1l_opy_
  global bstack1111ll11l_opy_
  global bstack1l1lll1l1l_opy_
  global bstack1l1l111l_opy_
  bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"࠭ࠧ౛")
  bstack111ll111_opy_(bstack1ll1l1l11l_opy_, logger)
  if bstack1l1ll111l_opy_ and isinstance(bstack1l1ll111l_opy_, str):
    bstack1l1ll111l_opy_ = eval(bstack1l1ll111l_opy_)
  if bstack1l1ll111l_opy_:
    CONFIG = bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ౜")]
    bstack1l1lll1l_opy_ = bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩౝ")]
    bstack1111ll11l_opy_ = bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ౞")]
    bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ౟"), bstack1111ll11l_opy_)
    bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫౠ")
  bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧౡ"), uuid4().__str__())
  logger.debug(bstack1lll1l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤ࠾ࠩౢ") + bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩౣ")))
  if not bstack1lll1llll1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1l1111_opy_)
      return
    if sys.argv[1] == bstack1lll1l_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫ౤") or sys.argv[1] == bstack1lll1l_opy_ (u"ࠩ࠰ࡺࠬ౥"):
      logger.info(bstack1lll1l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪ౦").format(__version__))
      return
    if sys.argv[1] == bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ౧"):
      bstack11ll111l1_opy_()
      return
  args = sys.argv
  bstack1lll11ll11_opy_()
  global bstack11lll11ll_opy_
  global bstack1llll11l1l_opy_
  global bstack1lll111111_opy_
  global bstack1l1l1l111_opy_
  global bstack1llll11lll_opy_
  global bstack11lll1111_opy_
  global bstack1ll1l1l11_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1llllll11_opy_
  global bstack1lll1l1l_opy_
  global bstack1l1llllll_opy_
  bstack1llll11l1l_opy_ = len(CONFIG.get(bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౨"), []))
  if not bstack1l11lll11l_opy_:
    if args[1] == bstack1lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭౩") or args[1] == bstack1lll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ౪"):
      bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ౫")
      args = args[2:]
    elif args[1] == bstack1lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౬"):
      bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ౭")
      args = args[2:]
    elif args[1] == bstack1lll1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ౮"):
      bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ౯")
      args = args[2:]
    elif args[1] == bstack1lll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ౰"):
      bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ౱")
      args = args[2:]
    elif args[1] == bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ౲"):
      bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౳")
      args = args[2:]
    elif args[1] == bstack1lll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ౴"):
      bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ౵")
      args = args[2:]
    else:
      if not bstack1lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ౶") in CONFIG or str(CONFIG[bstack1lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ౷")]).lower() in [bstack1lll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౸"), bstack1lll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ౹")]:
        bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ౺")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭౻")]).lower() == bstack1lll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౼"):
        bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ౽")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ౾")]).lower() == bstack1lll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭౿"):
        bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧಀ")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬಁ")]).lower() == bstack1lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪಂ"):
        bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಃ")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ಄")]).lower() == bstack1lll1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ಅ"):
        bstack1l11lll11l_opy_ = bstack1lll1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಆ")
        args = args[1:]
      else:
        os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪಇ")] = bstack1l11lll11l_opy_
        bstack11ll1l11l_opy_(bstack1ll111l11_opy_)
  os.environ[bstack1lll1l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪಈ")] = bstack1l11lll11l_opy_
  bstack1l1lll1l1l_opy_ = bstack1l11lll11l_opy_
  global bstack11l1l1ll1_opy_
  global bstack11ll11l1l_opy_
  if bstack1l1ll111l_opy_:
    try:
      os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬಉ")] = bstack1l11lll11l_opy_
      bstack1l11l1ll1l_opy_(bstack1ll1111l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1111l11l1_opy_.format(str(e)))
  global bstack1lll11l11l_opy_
  global bstack11l1l11ll_opy_
  global bstack1ll1lllll1_opy_
  global bstack1ll1l1l1_opy_
  global bstack11ll1l111_opy_
  global bstack1llll11l_opy_
  global bstack1ll111l1_opy_
  global bstack11l11lll1_opy_
  global bstack1ll11ll1_opy_
  global bstack111111111_opy_
  global bstack1l1l1llll_opy_
  global bstack1ll1l1111l_opy_
  global bstack1l11l11l1_opy_
  global bstack1l1111111_opy_
  global bstack1ll11l1l11_opy_
  global bstack1l1l111l1l_opy_
  global bstack11l1l1ll_opy_
  global bstack1l11111l1l_opy_
  global bstack1l1l11ll1l_opy_
  global bstack1111l1l11_opy_
  global bstack1111111ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll11l11l_opy_ = webdriver.Remote.__init__
    bstack11l1l11ll_opy_ = WebDriver.quit
    bstack1ll1l1111l_opy_ = WebDriver.close
    bstack1ll11l1l11_opy_ = WebDriver.get
    bstack1111111ll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11l1l1ll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1ll1l11l_opy_
    bstack11ll11l1l_opy_ = bstack1l1ll1l11l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1lll1l1ll1_opy_
    from QWeb.keywords import browser
    bstack1lll1l1ll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1llll1ll11_opy_(CONFIG) and bstack11lllll1l_opy_():
    if bstack1111l1l1l_opy_() < version.parse(bstack11llllllll_opy_):
      logger.error(bstack1ll11ll1l1_opy_.format(bstack1111l1l1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l111l1l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack111llll1_opy_.format(str(e)))
  if not CONFIG.get(bstack1lll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ಊ"), False) and not bstack1l1ll111l_opy_:
    logger.info(bstack1l1l11lll1_opy_)
  if bstack1l11lll11l_opy_ != bstack1lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬಋ") or (bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ಌ") and not bstack1l1ll111l_opy_):
    bstack1l1l1111l_opy_()
  if (bstack1l11lll11l_opy_ in [bstack1lll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭಍"), bstack1lll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧಎ"), bstack1lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪಏ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l11ll111_opy_
        bstack1llll11l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l11l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11ll1l111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1llll1l11_opy_ + str(e))
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11l11l1l_opy_)
    if bstack1l11lll11l_opy_ != bstack1lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫಐ"):
      bstack11l11ll1_opy_()
    bstack1ll1lllll1_opy_ = Output.start_test
    bstack1ll1l1l1_opy_ = Output.end_test
    bstack1ll111l1_opy_ = TestStatus.__init__
    bstack1ll11ll1_opy_ = pabot._run
    bstack111111111_opy_ = QueueItem.__init__
    bstack1l1l1llll_opy_ = pabot._create_command_for_execution
    bstack1l1l11ll1l_opy_ = pabot._report_results
  if bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ಑"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack1lll11lll1_opy_)
    bstack1l11l11l1_opy_ = Runner.run_hook
    bstack1l1111111_opy_ = Step.run
  if bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬಒ"):
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
      logger.debug(bstack1lll1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧಓ"))
  try:
    framework_name = bstack1lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಔ") if bstack1l11lll11l_opy_ in [bstack1lll1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧಕ"), bstack1lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಖ"), bstack1lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫಗ")] else bstack11ll1ll1l_opy_(bstack1l11lll11l_opy_)
    bstack1l11ll111l_opy_ = {
      bstack1lll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬಘ"): bstack1lll1l_opy_ (u"ࠬࢁ࠰ࡾ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫಙ").format(framework_name) if bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಚ") and bstack11ll1111_opy_() else framework_name,
      bstack1lll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫಛ"): bstack11ll1ll1_opy_(framework_name),
      bstack1lll1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ಜ"): __version__,
      bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪಝ"): bstack1l11lll11l_opy_
    }
    if bstack1l11lll11l_opy_ in bstack1l11llllll_opy_:
      if bstack1lll111l_opy_ and bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪಞ") in CONFIG and CONFIG[bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫಟ")] == True:
        if bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬಠ") in CONFIG:
          os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧಡ")] = os.getenv(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨಢ"), json.dumps(CONFIG[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨಣ")]))
          CONFIG[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩತ")].pop(bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨಥ"), None)
          CONFIG[bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫದ")].pop(bstack1lll1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪಧ"), None)
        bstack1l11ll111l_opy_[bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ನ")] = {
          bstack1lll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ಩"): bstack1lll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪಪ"),
          bstack1lll1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪಫ"): str(bstack1111l1l1l_opy_())
        }
    if bstack1l11lll11l_opy_ not in [bstack1lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫಬ")]:
      bstack1l111l1l1l_opy_ = bstack1111ll111_opy_.launch(CONFIG, bstack1l11ll111l_opy_)
  except Exception as e:
    logger.debug(bstack1l1111lll1_opy_.format(bstack1lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦࠬಭ"), str(e)))
  if bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬಮ"):
    bstack1lll111111_opy_ = True
    if bstack1l1ll111l_opy_ and bstack1lll1llll1_opy_:
      bstack11lll1111_opy_ = CONFIG.get(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪಯ"), {}).get(bstack1lll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩರ"))
      bstack1l1llll111_opy_(bstack1111l111l_opy_)
    elif bstack1l1ll111l_opy_:
      bstack11lll1111_opy_ = CONFIG.get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬಱ"), {}).get(bstack1lll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫಲ"))
      global bstack111ll1ll_opy_
      try:
        if bstack1ll111ll1l_opy_(bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ಳ")]) and multiprocessing.current_process().name == bstack1lll1l_opy_ (u"ࠫ࠵࠭಴"):
          bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨವ")].remove(bstack1lll1l_opy_ (u"࠭࠭࡮ࠩಶ"))
          bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪಷ")].remove(bstack1lll1l_opy_ (u"ࠨࡲࡧࡦࠬಸ"))
          bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬಹ")] = bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭಺")][0]
          with open(bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ಻")], bstack1lll1l_opy_ (u"ࠬࡸ಼ࠧ")) as f:
            bstack1l1l1lllll_opy_ = f.read()
          bstack1llll11l11_opy_ = bstack1lll1l_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࠣࡁࠥࡹࡴࡳࠪ࡬ࡲࡹ࠮ࡡࡳࡩࠬ࠯࠶࠶ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤಽ").format(str(bstack1l1ll111l_opy_))
          bstack1lllll111_opy_ = bstack1llll11l11_opy_ + bstack1l1l1lllll_opy_
          bstack1l11l111_opy_ = bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪಾ")] + bstack1lll1l_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪಿ")
          with open(bstack1l11l111_opy_, bstack1lll1l_opy_ (u"ࠩࡺࠫೀ")):
            pass
          with open(bstack1l11l111_opy_, bstack1lll1l_opy_ (u"ࠥࡻ࠰ࠨು")) as f:
            f.write(bstack1lllll111_opy_)
          import subprocess
          bstack1l1111ll1_opy_ = subprocess.run([bstack1lll1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦೂ"), bstack1l11l111_opy_])
          if os.path.exists(bstack1l11l111_opy_):
            os.unlink(bstack1l11l111_opy_)
          os._exit(bstack1l1111ll1_opy_.returncode)
        else:
          if bstack1ll111ll1l_opy_(bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨೃ")]):
            bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೄ")].remove(bstack1lll1l_opy_ (u"ࠧ࠮࡯ࠪ೅"))
            bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫೆ")].remove(bstack1lll1l_opy_ (u"ࠩࡳࡨࡧ࠭ೇ"))
            bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ೈ")] = bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೉")][0]
          bstack1l1llll111_opy_(bstack1111l111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨೊ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1lll1l_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨೋ")] = bstack1lll1l_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩೌ")
          mod_globals[bstack1lll1l_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡ್ࠪ")] = os.path.abspath(bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ೎")])
          exec(open(bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭೏")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1lll1l_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫ೐").format(str(e)))
          for driver in bstack111ll1ll_opy_:
            bstack1l11111l_opy_.append({
              bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೑"): bstack1l1ll111l_opy_[bstack1lll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ೒")],
              bstack1lll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭೓"): str(e),
              bstack1lll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ೔"): multiprocessing.current_process().name
            })
            bstack1l1111l111_opy_(driver, bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩೕ"), bstack1lll1l_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨೖ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack111ll1ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1111ll11l_opy_, CONFIG, logger)
      bstack1111ll1ll_opy_()
      bstack1l1l11l111_opy_()
      bstack1l1lll1l1_opy_ = {
        bstack1lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೗"): args[0],
        bstack1lll1l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ೘"): CONFIG,
        bstack1lll1l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ೙"): bstack1l1lll1l_opy_,
        bstack1lll1l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ೚"): bstack1111ll11l_opy_
      }
      percy.bstack1l1l11ll11_opy_()
      if bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೛") in CONFIG:
        bstack11111l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1ll11111_opy_ = manager.list()
        if bstack1ll111ll1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ೜")]):
            if index == 0:
              bstack1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ೝ")] = args
            bstack11111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1lll1l1_opy_, bstack1l1ll11111_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧೞ")]):
            bstack11111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1lll1l1_opy_, bstack1l1ll11111_opy_)))
        for t in bstack11111l11_opy_:
          t.start()
        for t in bstack11111l11_opy_:
          t.join()
        bstack1l1l1l1ll1_opy_ = list(bstack1l1ll11111_opy_)
      else:
        if bstack1ll111ll1l_opy_(args):
          bstack1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ೟")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1lll1l1_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1llll111_opy_(bstack1111l111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1lll1l_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨೠ")] = bstack1lll1l_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩೡ")
          mod_globals[bstack1lll1l_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪೢ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨೣ") or bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ೤"):
    percy.init(bstack1111ll11l_opy_, CONFIG, logger)
    percy.bstack1l1l11ll11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11l11l1l_opy_)
    bstack1111ll1ll_opy_()
    bstack1l1llll111_opy_(bstack1l11ll1ll_opy_)
    if bstack1lll111l_opy_:
      bstack1lll1l1111_opy_(bstack1l11ll1ll_opy_, args)
      if bstack1lll1l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ೥") in args:
        i = args.index(bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ೦"))
        args.pop(i)
        args.pop(i)
      if bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ೧") not in CONFIG:
        CONFIG[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ೨")] = [{}]
        bstack1llll11l1l_opy_ = 1
      if bstack11lll11ll_opy_ == 0:
        bstack11lll11ll_opy_ = 1
      args.insert(0, str(bstack11lll11ll_opy_))
      args.insert(0, str(bstack1lll1l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭೩")))
    if bstack1111ll111_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll11l11_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack111l1l111_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1lll1l_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤ೪"),
        ).parse_args(bstack1ll11l11_opy_)
        bstack1l1lllllll_opy_ = args.index(bstack1ll11l11_opy_[0]) if len(bstack1ll11l11_opy_) > 0 else len(args)
        args.insert(bstack1l1lllllll_opy_, str(bstack1lll1l_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧ೫")))
        args.insert(bstack1l1lllllll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨ೬"))))
        if bstack1l1lllll1l_opy_(os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ೭"))) and str(os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ೮"), bstack1lll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ೯"))) != bstack1lll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭೰"):
          for bstack11lllll1_opy_ in bstack111l1l111_opy_:
            args.remove(bstack11lllll1_opy_)
          bstack1ll111l1ll_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ೱ")).split(bstack1lll1l_opy_ (u"ࠪ࠰ࠬೲ"))
          for bstack1l1l1l1l1_opy_ in bstack1ll111l1ll_opy_:
            args.append(bstack1l1l1l1l1_opy_)
      except Exception as e:
        logger.error(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࠢೳ").format(e))
    pabot.main(args)
  elif bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭೴"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11l11l1l_opy_)
    for a in args:
      if bstack1lll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ೵") in a:
        bstack1llll11lll_opy_ = int(a.split(bstack1lll1l_opy_ (u"ࠧ࠻ࠩ೶"))[1])
      if bstack1lll1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ೷") in a:
        bstack11lll1111_opy_ = str(a.split(bstack1lll1l_opy_ (u"ࠩ࠽ࠫ೸"))[1])
      if bstack1lll1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪ೹") in a:
        bstack1ll1l1l11_opy_ = str(a.split(bstack1lll1l_opy_ (u"ࠫ࠿࠭೺"))[1])
    bstack1ll11lll1l_opy_ = None
    if bstack1lll1l_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫ೻") in args:
      i = args.index(bstack1lll1l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ೼"))
      args.pop(i)
      bstack1ll11lll1l_opy_ = args.pop(i)
    if bstack1ll11lll1l_opy_ is not None:
      global bstack111l1l1l1_opy_
      bstack111l1l1l1_opy_ = bstack1ll11lll1l_opy_
    bstack1l1llll111_opy_(bstack1l11ll1ll_opy_)
    run_cli(args)
    if bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ೽") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll11ll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11111l_opy_.append(bstack1ll11ll1ll_opy_)
  elif bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ೾"):
    percy.init(bstack1111ll11l_opy_, CONFIG, logger)
    percy.bstack1l1l11ll11_opy_()
    bstack1l11ll1l1_opy_ = bstack1111l11l_opy_(args, logger, CONFIG, bstack1lll111l_opy_)
    bstack1l11ll1l1_opy_.bstack11111ll1l_opy_()
    bstack1111ll1ll_opy_()
    bstack1l1l1l111_opy_ = True
    bstack1lll1l1l_opy_ = bstack1l11ll1l1_opy_.bstack11111llll_opy_()
    bstack1l11ll1l1_opy_.bstack1l1lll1l1_opy_(bstack111l11l1l_opy_)
    bstack1lll1l1lll_opy_ = bstack1l11ll1l1_opy_.bstack1l1llll1ll_opy_(bstack11111l111_opy_, {
      bstack1lll1l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ೿"): bstack1l1lll1l_opy_,
      bstack1lll1l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬഀ"): bstack1111ll11l_opy_,
      bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧഁ"): bstack1lll111l_opy_
    })
    try:
      bstack1lll11111l_opy_, bstack1l1ll1l1ll_opy_ = map(list, zip(*bstack1lll1l1lll_opy_))
      bstack1llllll11_opy_ = bstack1lll11111l_opy_[0]
      for status_code in bstack1l1ll1l1ll_opy_:
        if status_code != 0:
          bstack1l1llllll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1lll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥം").format(str(e)))
  elif bstack1l11lll11l_opy_ == bstack1lll1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ഃ"):
    try:
      from behave.__main__ import main as bstack1l1lll1ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack1lll11lll1_opy_)
    bstack1111ll1ll_opy_()
    bstack1l1l1l111_opy_ = True
    bstack11l1ll11l_opy_ = 1
    if bstack1lll1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧഄ") in CONFIG:
      bstack11l1ll11l_opy_ = CONFIG[bstack1lll1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨഅ")]
    if bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬആ") in CONFIG:
      bstack1ll1ll1l11_opy_ = int(bstack11l1ll11l_opy_) * int(len(CONFIG[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ഇ")]))
    else:
      bstack1ll1ll1l11_opy_ = int(bstack11l1ll11l_opy_)
    config = Configuration(args)
    bstack1lll1111l1_opy_ = config.paths
    if len(bstack1lll1111l1_opy_) == 0:
      import glob
      pattern = bstack1lll1l_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪഈ")
      bstack11111111_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11111111_opy_)
      config = Configuration(args)
      bstack1lll1111l1_opy_ = config.paths
    bstack1ll1l1lll1_opy_ = [os.path.normpath(item) for item in bstack1lll1111l1_opy_]
    bstack11l1ll1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1ll1ll1l_opy_ = [item for item in bstack11l1ll1l1_opy_ if item not in bstack1ll1l1lll1_opy_]
    import platform as pf
    if pf.system().lower() == bstack1lll1l_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ഉ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1l1lll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11lll111_opy_)))
                    for bstack11lll111_opy_ in bstack1ll1l1lll1_opy_]
    bstack1l1l1l1lll_opy_ = []
    for spec in bstack1ll1l1lll1_opy_:
      bstack1111llll_opy_ = []
      bstack1111llll_opy_ += bstack1l1ll1ll1l_opy_
      bstack1111llll_opy_.append(spec)
      bstack1l1l1l1lll_opy_.append(bstack1111llll_opy_)
    execution_items = []
    for bstack1111llll_opy_ in bstack1l1l1l1lll_opy_:
      if bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഊ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪഋ")]):
          item = {}
          item[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࠬഌ")] = bstack1lll1l_opy_ (u"ࠩࠣࠫ഍").join(bstack1111llll_opy_)
          item[bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩഎ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1lll1l_opy_ (u"ࠫࡦࡸࡧࠨഏ")] = bstack1lll1l_opy_ (u"ࠬࠦࠧഐ").join(bstack1111llll_opy_)
        item[bstack1lll1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ഑")] = 0
        execution_items.append(item)
    bstack1ll1l111_opy_ = bstack1l111l1l1_opy_(execution_items, bstack1ll1ll1l11_opy_)
    for execution_item in bstack1ll1l111_opy_:
      bstack11111l11_opy_ = []
      for item in execution_item:
        bstack11111l11_opy_.append(bstack1lll1lll1l_opy_(name=str(item[bstack1lll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ഒ")]),
                                             target=bstack1ll11l111l_opy_,
                                             args=(item[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࠬഓ")],)))
      for t in bstack11111l11_opy_:
        t.start()
      for t in bstack11111l11_opy_:
        t.join()
  else:
    bstack11ll1l11l_opy_(bstack1ll111l11_opy_)
  if not bstack1l1ll111l_opy_:
    bstack1lll11111_opy_()
  bstack1lll111l1_opy_.bstack11llllll1l_opy_()
def browserstack_initialize(bstack1ll11llll1_opy_=None):
  run_on_browserstack(bstack1ll11llll1_opy_, None, True)
def bstack1lll11111_opy_():
  global CONFIG
  global bstack1l1lll1l1l_opy_
  global bstack1l1llllll_opy_
  global bstack1l1l1ll1_opy_
  global bstack1l1l111l_opy_
  bstack1111ll111_opy_.stop()
  bstack11l111l1l_opy_.bstack1l11l1lll_opy_()
  [bstack11llllll11_opy_, bstack1l1l1l1111_opy_] = get_build_link()
  if bstack11llllll11_opy_ is not None and bstack11l1111l1_opy_() != -1:
    sessions = bstack1111111l_opy_(bstack11llllll11_opy_)
    bstack1l1ll11lll_opy_(sessions, bstack1l1l1l1111_opy_)
  if bstack1l1lll1l1l_opy_ == bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഔ") and bstack1l1llllll_opy_ != 0:
    sys.exit(bstack1l1llllll_opy_)
  if bstack1l1lll1l1l_opy_ == bstack1lll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪക") and bstack1l1l1ll1_opy_ != 0:
    sys.exit(bstack1l1l1ll1_opy_)
def bstack11ll1ll1l_opy_(bstack111lll1l1_opy_):
  if bstack111lll1l1_opy_:
    return bstack111lll1l1_opy_.capitalize()
  else:
    return bstack1lll1l_opy_ (u"ࠫࠬഖ")
def bstack1l111l11l_opy_(bstack1l1111ll11_opy_):
  if bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪഗ") in bstack1l1111ll11_opy_ and bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫഘ")] != bstack1lll1l_opy_ (u"ࠧࠨങ"):
    return bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ച")]
  else:
    bstack1l11l1l11_opy_ = bstack1lll1l_opy_ (u"ࠤࠥഛ")
    if bstack1lll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪജ") in bstack1l1111ll11_opy_ and bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫഝ")] != None:
      bstack1l11l1l11_opy_ += bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬഞ")] + bstack1lll1l_opy_ (u"ࠨࠬࠡࠤട")
      if bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠧࡰࡵࠪഠ")] == bstack1lll1l_opy_ (u"ࠣ࡫ࡲࡷࠧഡ"):
        bstack1l11l1l11_opy_ += bstack1lll1l_opy_ (u"ࠤ࡬ࡓࡘࠦࠢഢ")
      bstack1l11l1l11_opy_ += (bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧണ")] or bstack1lll1l_opy_ (u"ࠫࠬത"))
      return bstack1l11l1l11_opy_
    else:
      bstack1l11l1l11_opy_ += bstack11ll1ll1l_opy_(bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ഥ")]) + bstack1lll1l_opy_ (u"ࠨࠠࠣദ") + (
              bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩധ")] or bstack1lll1l_opy_ (u"ࠨࠩന")) + bstack1lll1l_opy_ (u"ࠤ࠯ࠤࠧഩ")
      if bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"ࠪࡳࡸ࠭പ")] == bstack1lll1l_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧഫ"):
        bstack1l11l1l11_opy_ += bstack1lll1l_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥബ")
      bstack1l11l1l11_opy_ += bstack1l1111ll11_opy_[bstack1lll1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪഭ")] or bstack1lll1l_opy_ (u"ࠧࠨമ")
      return bstack1l11l1l11_opy_
def bstack1ll1lll11_opy_(bstack1ll1l1l1l_opy_):
  if bstack1ll1l1l1l_opy_ == bstack1lll1l_opy_ (u"ࠣࡦࡲࡲࡪࠨയ"):
    return bstack1lll1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬര")
  elif bstack1ll1l1l1l_opy_ == bstack1lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥറ"):
    return bstack1lll1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧല")
  elif bstack1ll1l1l1l_opy_ == bstack1lll1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧള"):
    return bstack1lll1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ഴ")
  elif bstack1ll1l1l1l_opy_ == bstack1lll1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨവ"):
    return bstack1lll1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪശ")
  elif bstack1ll1l1l1l_opy_ == bstack1lll1l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥഷ"):
    return bstack1lll1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨസ")
  elif bstack1ll1l1l1l_opy_ == bstack1lll1l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧഹ"):
    return bstack1lll1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ഺ")
  else:
    return bstack1lll1l_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀ഻ࠪ") + bstack11ll1ll1l_opy_(
      bstack1ll1l1l1l_opy_) + bstack1lll1l_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ഼࠭")
def bstack1lll1llll_opy_(session):
  return bstack1lll1l_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨഽ").format(
    session[bstack1lll1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ാ")], bstack1l111l11l_opy_(session), bstack1ll1lll11_opy_(session[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩി")]),
    bstack1ll1lll11_opy_(session[bstack1lll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫീ")]),
    bstack11ll1ll1l_opy_(session[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ു")] or session[bstack1lll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ൂ")] or bstack1lll1l_opy_ (u"ࠧࠨൃ")) + bstack1lll1l_opy_ (u"ࠣࠢࠥൄ") + (session[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ൅")] or bstack1lll1l_opy_ (u"ࠪࠫെ")),
    session[bstack1lll1l_opy_ (u"ࠫࡴࡹࠧേ")] + bstack1lll1l_opy_ (u"ࠧࠦࠢൈ") + session[bstack1lll1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ൉")], session[bstack1lll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩൊ")] or bstack1lll1l_opy_ (u"ࠨࠩോ"),
    session[bstack1lll1l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ൌ")] if session[bstack1lll1l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺ്ࠧ")] else bstack1lll1l_opy_ (u"ࠫࠬൎ"))
def bstack1l1ll11lll_opy_(sessions, bstack1l1l1l1111_opy_):
  try:
    bstack1lll11l11_opy_ = bstack1lll1l_opy_ (u"ࠧࠨ൏")
    if not os.path.exists(bstack1lllll1l1l_opy_):
      os.mkdir(bstack1lllll1l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ൐")), bstack1lll1l_opy_ (u"ࠧࡳࠩ൑")) as f:
      bstack1lll11l11_opy_ = f.read()
    bstack1lll11l11_opy_ = bstack1lll11l11_opy_.replace(bstack1lll1l_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬ൒"), str(len(sessions)))
    bstack1lll11l11_opy_ = bstack1lll11l11_opy_.replace(bstack1lll1l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩ൓"), bstack1l1l1l1111_opy_)
    bstack1lll11l11_opy_ = bstack1lll11l11_opy_.replace(bstack1lll1l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫൔ"),
                                              sessions[0].get(bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨൕ")) if sessions[0] else bstack1lll1l_opy_ (u"ࠬ࠭ൖ"))
    with open(os.path.join(bstack1lllll1l1l_opy_, bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪൗ")), bstack1lll1l_opy_ (u"ࠧࡸࠩ൘")) as stream:
      stream.write(bstack1lll11l11_opy_.split(bstack1lll1l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬ൙"))[0])
      for session in sessions:
        stream.write(bstack1lll1llll_opy_(session))
      stream.write(bstack1lll11l11_opy_.split(bstack1lll1l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭൚"))[1])
    logger.info(bstack1lll1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭൛").format(bstack1lllll1l1l_opy_));
  except Exception as e:
    logger.debug(bstack1l11l111ll_opy_.format(str(e)))
def bstack1111111l_opy_(bstack11llllll11_opy_):
  global CONFIG
  try:
    host = bstack1lll1l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ൜") if bstack1lll1l_opy_ (u"ࠬࡧࡰࡱࠩ൝") in CONFIG else bstack1lll1l_opy_ (u"࠭ࡡࡱ࡫ࠪ൞")
    user = CONFIG[bstack1lll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩൟ")]
    key = CONFIG[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫൠ")]
    bstack1lll11llll_opy_ = bstack1lll1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨൡ") if bstack1lll1l_opy_ (u"ࠪࡥࡵࡶࠧൢ") in CONFIG else bstack1lll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ൣ")
    url = bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪ൤").format(user, key, host, bstack1lll11llll_opy_,
                                                                                bstack11llllll11_opy_)
    headers = {
      bstack1lll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ൥"): bstack1lll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ൦"),
    }
    proxies = bstack1l1l1111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1lll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭൧")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11l1ll_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1lll11l1l_opy_
  try:
    if bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ൨") in CONFIG:
      host = bstack1lll1l_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭൩") if bstack1lll1l_opy_ (u"ࠫࡦࡶࡰࠨ൪") in CONFIG else bstack1lll1l_opy_ (u"ࠬࡧࡰࡪࠩ൫")
      user = CONFIG[bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ൬")]
      key = CONFIG[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ൭")]
      bstack1lll11llll_opy_ = bstack1lll1l_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ൮") if bstack1lll1l_opy_ (u"ࠩࡤࡴࡵ࠭൯") in CONFIG else bstack1lll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ൰")
      url = bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫ൱").format(user, key, host, bstack1lll11llll_opy_)
      headers = {
        bstack1lll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ൲"): bstack1lll1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ൳"),
      }
      if bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ൴") in CONFIG:
        params = {bstack1lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭൵"): CONFIG[bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ൶")], bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭൷"): CONFIG[bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭൸")]}
      else:
        params = {bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ൹"): CONFIG[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൺ")]}
      proxies = bstack1l1l1111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack111lllll_opy_ = response.json()[0][bstack1lll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪൻ")]
        if bstack111lllll_opy_:
          bstack1l1l1l1111_opy_ = bstack111lllll_opy_[bstack1lll1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬർ")].split(bstack1lll1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨൽ"))[0] + bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫൾ") + bstack111lllll_opy_[
            bstack1lll1l_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧൿ")]
          logger.info(bstack111ll1ll1_opy_.format(bstack1l1l1l1111_opy_))
          bstack1lll11l1l_opy_ = bstack111lllll_opy_[bstack1lll1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ඀")]
          bstack1l11l11l_opy_ = CONFIG[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩඁ")]
          if bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩං") in CONFIG:
            bstack1l11l11l_opy_ += bstack1lll1l_opy_ (u"ࠨࠢࠪඃ") + CONFIG[bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ඄")]
          if bstack1l11l11l_opy_ != bstack111lllll_opy_[bstack1lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨඅ")]:
            logger.debug(bstack1l1ll11l1l_opy_.format(bstack111lllll_opy_[bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩආ")], bstack1l11l11l_opy_))
          return [bstack111lllll_opy_[bstack1lll1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨඇ")], bstack1l1l1l1111_opy_]
    else:
      logger.warn(bstack1l11l11l11_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll1llll_opy_.format(str(e)))
  return [None, None]
def bstack11111ll11_opy_(url, bstack1ll11l1ll_opy_=False):
  global CONFIG
  global bstack11l1111ll_opy_
  if not bstack11l1111ll_opy_:
    hostname = bstack1ll1111l11_opy_(url)
    is_private = bstack111ll1l11_opy_(hostname)
    if (bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪඈ") in CONFIG and not bstack1l1lllll1l_opy_(CONFIG[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫඉ")])) and (is_private or bstack1ll11l1ll_opy_):
      bstack11l1111ll_opy_ = hostname
def bstack1ll1111l11_opy_(url):
  return urlparse(url).hostname
def bstack111ll1l11_opy_(hostname):
  for bstack11l1llll_opy_ in bstack1l1ll111_opy_:
    regex = re.compile(bstack11l1llll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111ll1111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1llll11lll_opy_
  bstack1l1l1l11l_opy_ = not (bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬඊ"), None) and bstack1ll111lll1_opy_(
          threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨඋ"), None))
  bstack1ll1111l_opy_ = getattr(driver, bstack1lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪඌ"), None) != True
  if not bstack1ll111llll_opy_.bstack11l1lllll_opy_(CONFIG, bstack1llll11lll_opy_) or (bstack1ll1111l_opy_ and bstack1l1l1l11l_opy_):
    logger.warning(bstack1lll1l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢඍ"))
    return {}
  try:
    logger.debug(bstack1lll1l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩඎ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l111111l1_opy_.bstack1ll11llll_opy_)
    return results
  except Exception:
    logger.error(bstack1lll1l_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣඏ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1llll11lll_opy_
  bstack1l1l1l11l_opy_ = not (bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫඐ"), None) and bstack1ll111lll1_opy_(
          threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧඑ"), None))
  bstack1ll1111l_opy_ = getattr(driver, bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩඒ"), None) != True
  if not bstack1ll111llll_opy_.bstack11l1lllll_opy_(CONFIG, bstack1llll11lll_opy_) or (bstack1ll1111l_opy_ and bstack1l1l1l11l_opy_):
    logger.warning(bstack1lll1l_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢඓ"))
    return {}
  try:
    logger.debug(bstack1lll1l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩඔ"))
    logger.debug(perform_scan(driver))
    bstack11lll1ll1_opy_ = driver.execute_async_script(bstack1l111111l1_opy_.bstack1lll1111ll_opy_)
    return bstack11lll1ll1_opy_
  except Exception:
    logger.error(bstack1lll1l_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨඕ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1llll11lll_opy_
  bstack1l1l1l11l_opy_ = not (bstack1ll111lll1_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪඖ"), None) and bstack1ll111lll1_opy_(
          threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭඗"), None))
  bstack1ll1111l_opy_ = getattr(driver, bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ඘"), None) != True
  if not bstack1ll111llll_opy_.bstack11l1lllll_opy_(CONFIG, bstack1llll11lll_opy_) or (bstack1ll1111l_opy_ and bstack1l1l1l11l_opy_):
    logger.warning(bstack1lll1l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡸࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠦ඙"))
    return {}
  try:
    bstack1111l1lll_opy_ = driver.execute_async_script(bstack1l111111l1_opy_.perform_scan, {bstack1lll1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪක"): kwargs.get(bstack1lll1l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬඛ"), None) or bstack1lll1l_opy_ (u"ࠬ࠭ග")})
    return bstack1111l1lll_opy_
  except Exception:
    logger.error(bstack1lll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠧඝ"))
    return {}