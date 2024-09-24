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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l11lll1_opy_, bstack1l1l11l1_opy_
class bstack1ll111111l_opy_:
  working_dir = os.getcwd()
  bstack11l111l11_opy_ = False
  config = {}
  binary_path = bstack1lll1l_opy_ (u"ࠩࠪᔞ")
  bstack1lll1llllll_opy_ = bstack1lll1l_opy_ (u"ࠪࠫᔟ")
  bstack1ll11l11ll_opy_ = False
  bstack1llll1l1l11_opy_ = None
  bstack1llll11l1l1_opy_ = {}
  bstack1lll1lllll1_opy_ = 300
  bstack1llll1l111l_opy_ = False
  logger = None
  bstack1lllll11111_opy_ = False
  bstack1l11lll11_opy_ = False
  bstack111l11ll1_opy_ = None
  bstack1llll111lll_opy_ = bstack1lll1l_opy_ (u"ࠫࠬᔠ")
  bstack1llll1l1ll1_opy_ = {
    bstack1lll1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᔡ") : 1,
    bstack1lll1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᔢ") : 2,
    bstack1lll1l_opy_ (u"ࠧࡦࡦࡪࡩࠬᔣ") : 3,
    bstack1lll1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᔤ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1llll111111_opy_(self):
    bstack1llll1ll1l1_opy_ = bstack1lll1l_opy_ (u"ࠩࠪᔥ")
    bstack1llll1l1l1l_opy_ = sys.platform
    bstack1lll1ll1l11_opy_ = bstack1lll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᔦ")
    if re.match(bstack1lll1l_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᔧ"), bstack1llll1l1l1l_opy_) != None:
      bstack1llll1ll1l1_opy_ = bstack111ll11lll_opy_ + bstack1lll1l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᔨ")
      self.bstack1llll111lll_opy_ = bstack1lll1l_opy_ (u"࠭࡭ࡢࡥࠪᔩ")
    elif re.match(bstack1lll1l_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᔪ"), bstack1llll1l1l1l_opy_) != None:
      bstack1llll1ll1l1_opy_ = bstack111ll11lll_opy_ + bstack1lll1l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᔫ")
      bstack1lll1ll1l11_opy_ = bstack1lll1l_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᔬ")
      self.bstack1llll111lll_opy_ = bstack1lll1l_opy_ (u"ࠪࡻ࡮ࡴࠧᔭ")
    else:
      bstack1llll1ll1l1_opy_ = bstack111ll11lll_opy_ + bstack1lll1l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᔮ")
      self.bstack1llll111lll_opy_ = bstack1lll1l_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᔯ")
    return bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_
  def bstack1lll1ll1lll_opy_(self):
    try:
      bstack1lll1ll1ll1_opy_ = [os.path.join(expanduser(bstack1lll1l_opy_ (u"ࠨࡾࠣᔰ")), bstack1lll1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᔱ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll1ll1ll1_opy_:
        if(self.bstack1llll1l1111_opy_(path)):
          return path
      raise bstack1lll1l_opy_ (u"ࠣࡗࡱࡥࡱࡨࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᔲ")
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᔳ").format(e))
  def bstack1llll1l1111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lll1llll1l_opy_(self, bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_):
    try:
      bstack1llll111ll1_opy_ = self.bstack1lll1ll1lll_opy_()
      bstack1lllll111ll_opy_ = os.path.join(bstack1llll111ll1_opy_, bstack1lll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ᔴ"))
      bstack1llll1lll1l_opy_ = os.path.join(bstack1llll111ll1_opy_, bstack1lll1ll1l11_opy_)
      if os.path.exists(bstack1llll1lll1l_opy_):
        self.logger.info(bstack1lll1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᔵ").format(bstack1llll1lll1l_opy_))
        return bstack1llll1lll1l_opy_
      if os.path.exists(bstack1lllll111ll_opy_):
        self.logger.info(bstack1lll1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᔶ").format(bstack1lllll111ll_opy_))
        return self.bstack1llll1llll1_opy_(bstack1lllll111ll_opy_, bstack1lll1ll1l11_opy_)
      self.logger.info(bstack1lll1l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᔷ").format(bstack1llll1ll1l1_opy_))
      response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"ࠧࡈࡇࡗࠫᔸ"), bstack1llll1ll1l1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lllll111ll_opy_, bstack1lll1l_opy_ (u"ࠨࡹࡥࠫᔹ")) as file:
          file.write(response.content)
        self.logger.info(bstack1lll1l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢᔺ").format(bstack1lllll111ll_opy_))
        return self.bstack1llll1llll1_opy_(bstack1lllll111ll_opy_, bstack1lll1ll1l11_opy_)
      else:
        raise(bstack1lll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨᔻ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᔼ").format(e))
  def bstack1llll11l1ll_opy_(self, bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_):
    try:
      retry = 2
      bstack1llll1lll1l_opy_ = None
      bstack1llll1111l1_opy_ = False
      while retry > 0:
        bstack1llll1lll1l_opy_ = self.bstack1lll1llll1l_opy_(bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_)
        bstack1llll1111l1_opy_ = self.bstack1llll1ll11l_opy_(bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_, bstack1llll1lll1l_opy_)
        if bstack1llll1111l1_opy_:
          break
        retry -= 1
      return bstack1llll1lll1l_opy_, bstack1llll1111l1_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤᔽ").format(e))
    return bstack1llll1lll1l_opy_, False
  def bstack1llll1ll11l_opy_(self, bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_, bstack1llll1lll1l_opy_, bstack1lll1lll1ll_opy_ = 0):
    if bstack1lll1lll1ll_opy_ > 1:
      return False
    if bstack1llll1lll1l_opy_ == None or os.path.exists(bstack1llll1lll1l_opy_) == False:
      self.logger.warn(bstack1lll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᔾ"))
      return False
    bstack1llll1111ll_opy_ = bstack1lll1l_opy_ (u"ࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࡟࠳ࡨࡲࡩࠡ࡞ࡧ࠲ࡡࡪࠫ࠯࡞ࡧ࠯ࠧᔿ")
    command = bstack1lll1l_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧᕀ").format(bstack1llll1lll1l_opy_)
    bstack1llll11111l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1llll1111ll_opy_, bstack1llll11111l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1lll1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᕁ"))
      return False
  def bstack1llll1llll1_opy_(self, bstack1lllll111ll_opy_, bstack1lll1ll1l11_opy_):
    try:
      working_dir = os.path.dirname(bstack1lllll111ll_opy_)
      shutil.unpack_archive(bstack1lllll111ll_opy_, working_dir)
      bstack1llll1lll1l_opy_ = os.path.join(working_dir, bstack1lll1ll1l11_opy_)
      os.chmod(bstack1llll1lll1l_opy_, 0o755)
      return bstack1llll1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᕂ"))
  def bstack1llll1lllll_opy_(self):
    try:
      bstack1lllll11l11_opy_ = self.config.get(bstack1lll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᕃ"))
      bstack1llll1lllll_opy_ = bstack1lllll11l11_opy_ or (bstack1lllll11l11_opy_ is None and self.bstack11l111l11_opy_)
      if not bstack1llll1lllll_opy_ or self.config.get(bstack1lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᕄ"), None) not in bstack111ll1l111_opy_:
        return False
      self.bstack1ll11l11ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᕅ").format(e))
  def bstack1lllll1111l_opy_(self):
    try:
      bstack1lllll1111l_opy_ = self.bstack1llll1l11l1_opy_
      return bstack1lllll1111l_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᕆ").format(e))
  def init(self, bstack11l111l11_opy_, config, logger):
    self.bstack11l111l11_opy_ = bstack11l111l11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll1lllll_opy_():
      return
    self.bstack1llll11l1l1_opy_ = config.get(bstack1lll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᕇ"), {})
    self.bstack1llll1l11l1_opy_ = config.get(bstack1lll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᕈ"))
    try:
      bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_ = self.bstack1llll111111_opy_()
      bstack1llll1lll1l_opy_, bstack1llll1111l1_opy_ = self.bstack1llll11l1ll_opy_(bstack1llll1ll1l1_opy_, bstack1lll1ll1l11_opy_)
      if bstack1llll1111l1_opy_:
        self.binary_path = bstack1llll1lll1l_opy_
        thread = Thread(target=self.bstack1lll1lll11l_opy_)
        thread.start()
      else:
        self.bstack1lllll11111_opy_ = True
        self.logger.error(bstack1lll1l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢᕉ").format(bstack1llll1lll1l_opy_))
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᕊ").format(e))
  def bstack1llll11l11l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1lll1l_opy_ (u"ࠬࡲ࡯ࡨࠩᕋ"), bstack1lll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩᕌ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦᕍ").format(logfile))
      self.bstack1lll1llllll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᕎ").format(e))
  def bstack1lll1lll11l_opy_(self):
    bstack1lllll111l1_opy_ = self.bstack1llll111l1l_opy_()
    if bstack1lllll111l1_opy_ == None:
      self.bstack1lllll11111_opy_ = True
      self.logger.error(bstack1lll1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧᕏ"))
      return False
    command_args = [bstack1lll1l_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦᕐ") if self.bstack11l111l11_opy_ else bstack1lll1l_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨᕑ")]
    bstack1llll111l11_opy_ = self.bstack1llll1ll111_opy_()
    if bstack1llll111l11_opy_ != None:
      command_args.append(bstack1lll1l_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦᕒ").format(bstack1llll111l11_opy_))
    env = os.environ.copy()
    env[bstack1lll1l_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦᕓ")] = bstack1lllll111l1_opy_
    env[bstack1lll1l_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢᕔ")] = os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᕕ"), bstack1lll1l_opy_ (u"ࠩࠪᕖ"))
    bstack1llll1lll11_opy_ = [self.binary_path]
    self.bstack1llll11l11l_opy_()
    self.bstack1llll1l1l11_opy_ = self.bstack1lll1llll11_opy_(bstack1llll1lll11_opy_ + command_args, env)
    self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦᕗ"))
    bstack1lll1lll1ll_opy_ = 0
    while self.bstack1llll1l1l11_opy_.poll() == None:
      bstack1lll1ll111l_opy_ = self.bstack1lll1ll11ll_opy_()
      if bstack1lll1ll111l_opy_:
        self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢᕘ"))
        self.bstack1llll1l111l_opy_ = True
        return True
      bstack1lll1lll1ll_opy_ += 1
      self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣᕙ").format(bstack1lll1lll1ll_opy_))
      time.sleep(2)
    self.logger.error(bstack1lll1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦᕚ").format(bstack1lll1lll1ll_opy_))
    self.bstack1lllll11111_opy_ = True
    return False
  def bstack1lll1ll11ll_opy_(self, bstack1lll1lll1ll_opy_ = 0):
    if bstack1lll1lll1ll_opy_ > 10:
      return False
    try:
      bstack1lll1lll111_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧᕛ"), bstack1lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩᕜ"))
      bstack1llll11ll11_opy_ = bstack1lll1lll111_opy_ + bstack111ll111ll_opy_
      response = requests.get(bstack1llll11ll11_opy_)
      data = response.json()
      self.bstack111l11ll1_opy_ = getattr(data.get(bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᕝ"), {}), bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭ᕞ"), None)
      return True
    except:
      self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤᕟ"))
      return False
  def bstack1llll111l1l_opy_(self):
    bstack1llll1l11ll_opy_ = bstack1lll1l_opy_ (u"ࠬࡧࡰࡱࠩᕠ") if self.bstack11l111l11_opy_ else bstack1lll1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᕡ")
    bstack1llll11l111_opy_ = bstack1lll1l_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥᕢ") if self.config.get(bstack1lll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᕣ")) is None else True
    bstack111l1ll111_opy_ = bstack1lll1l_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥᕤ").format(self.config[bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᕥ")], bstack1llll1l11ll_opy_, bstack1llll11l111_opy_)
    if self.bstack1llll1l11l1_opy_:
      bstack111l1ll111_opy_ += bstack1lll1l_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨᕦ").format(self.bstack1llll1l11l1_opy_)
    uri = bstack1l11lll1_opy_(bstack111l1ll111_opy_)
    try:
      response = bstack1l1l11l1_opy_(bstack1lll1l_opy_ (u"ࠬࡍࡅࡕࠩᕧ"), uri, {}, {bstack1lll1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᕨ"): (self.config[bstack1lll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᕩ")], self.config[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᕪ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1ll11l11ll_opy_ = data.get(bstack1lll1l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᕫ"))
        self.bstack1llll1l11l1_opy_ = data.get(bstack1lll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨᕬ"))
        os.environ[bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᕭ")] = str(self.bstack1ll11l11ll_opy_)
        os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩᕮ")] = str(self.bstack1llll1l11l1_opy_)
        if bstack1llll11l111_opy_ == bstack1lll1l_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᕯ") and str(self.bstack1ll11l11ll_opy_).lower() == bstack1lll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᕰ"):
          self.bstack1l11lll11_opy_ = True
        if bstack1lll1l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᕱ") in data:
          return data[bstack1lll1l_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣᕲ")]
        else:
          raise bstack1lll1l_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪᕳ").format(data)
      else:
        raise bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦᕴ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨᕵ").format(e))
  def bstack1llll1ll111_opy_(self):
    bstack1lll1ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤᕶ"))
    try:
      if bstack1lll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕷ") not in self.bstack1llll11l1l1_opy_:
        self.bstack1llll11l1l1_opy_[bstack1lll1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᕸ")] = 2
      with open(bstack1lll1ll1l1l_opy_, bstack1lll1l_opy_ (u"ࠩࡺࠫᕹ")) as fp:
        json.dump(self.bstack1llll11l1l1_opy_, fp)
      return bstack1lll1ll1l1l_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᕺ").format(e))
  def bstack1lll1llll11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll111lll_opy_ == bstack1lll1l_opy_ (u"ࠫࡼ࡯࡮ࠨᕻ"):
        bstack1lll1ll11l1_opy_ = [bstack1lll1l_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭ᕼ"), bstack1lll1l_opy_ (u"࠭࠯ࡤࠩᕽ")]
        cmd = bstack1lll1ll11l1_opy_ + cmd
      cmd = bstack1lll1l_opy_ (u"ࠧࠡࠩᕾ").join(cmd)
      self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧᕿ").format(cmd))
      with open(self.bstack1lll1llllll_opy_, bstack1lll1l_opy_ (u"ࠤࡤࠦᖀ")) as bstack1llll11lll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll11lll1_opy_, text=True, stderr=bstack1llll11lll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lllll11111_opy_ = True
      self.logger.error(bstack1lll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᖁ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll1l111l_opy_:
        self.logger.info(bstack1lll1l_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧᖂ"))
        cmd = [self.binary_path, bstack1lll1l_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣᖃ")]
        self.bstack1lll1llll11_opy_(cmd)
        self.bstack1llll1l111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᖄ").format(cmd, e))
  def bstack1l1l11ll11_opy_(self):
    if not self.bstack1ll11l11ll_opy_:
      return
    try:
      bstack1llll1l1lll_opy_ = 0
      while not self.bstack1llll1l111l_opy_ and bstack1llll1l1lll_opy_ < self.bstack1lll1lllll1_opy_:
        if self.bstack1lllll11111_opy_:
          self.logger.info(bstack1lll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧᖅ"))
          return
        time.sleep(1)
        bstack1llll1l1lll_opy_ += 1
      os.environ[bstack1lll1l_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧᖆ")] = str(self.bstack1lll1lll1l1_opy_())
      self.logger.info(bstack1lll1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥᖇ"))
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᖈ").format(e))
  def bstack1lll1lll1l1_opy_(self):
    if self.bstack11l111l11_opy_:
      return
    try:
      bstack1llll11ll1l_opy_ = [platform[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᖉ")].lower() for platform in self.config.get(bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᖊ"), [])]
      bstack1llll11llll_opy_ = sys.maxsize
      bstack1lll1ll1111_opy_ = bstack1lll1l_opy_ (u"࠭ࠧᖋ")
      for browser in bstack1llll11ll1l_opy_:
        if browser in self.bstack1llll1l1ll1_opy_:
          bstack1llll1ll1ll_opy_ = self.bstack1llll1l1ll1_opy_[browser]
        if bstack1llll1ll1ll_opy_ < bstack1llll11llll_opy_:
          bstack1llll11llll_opy_ = bstack1llll1ll1ll_opy_
          bstack1lll1ll1111_opy_ = browser
      return bstack1lll1ll1111_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᖌ").format(e))
  @classmethod
  def bstack11ll1lll_opy_(self):
    return os.getenv(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ᖍ"), bstack1lll1l_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨᖎ")).lower()
  @classmethod
  def bstack1l1lll1l11_opy_(self):
    return os.getenv(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᖏ"), bstack1lll1l_opy_ (u"ࠫࠬᖐ"))