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
class bstack111lll11ll_opy_(object):
  bstack111l111l_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠬࢄࠧྩ")), bstack1lll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ྪ"))
  bstack111lll1l11_opy_ = os.path.join(bstack111l111l_opy_, bstack1lll1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧྫ"))
  bstack111lll1lll_opy_ = None
  perform_scan = None
  bstack1ll11llll_opy_ = None
  bstack1lll1111ll_opy_ = None
  bstack11l1111l1l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1lll1l_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪྫྷ")):
      cls.instance = super(bstack111lll11ll_opy_, cls).__new__(cls)
      cls.instance.bstack111lll11l1_opy_()
    return cls.instance
  def bstack111lll11l1_opy_(self):
    try:
      with open(self.bstack111lll1l11_opy_, bstack1lll1l_opy_ (u"ࠩࡵࠫྭ")) as bstack1l111l111l_opy_:
        bstack111lll1ll1_opy_ = bstack1l111l111l_opy_.read()
        data = json.loads(bstack111lll1ll1_opy_)
        if bstack1lll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬྮ") in data:
          self.bstack11l111l1l1_opy_(data[bstack1lll1l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ྯ")])
        if bstack1lll1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ྰ") in data:
          self.bstack11l11l11l1_opy_(data[bstack1lll1l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧྱ")])
    except:
      pass
  def bstack11l11l11l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1lll1l_opy_ (u"ࠧࡴࡥࡤࡲࠬྲ")]
      self.bstack1ll11llll_opy_ = scripts[bstack1lll1l_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬླ")]
      self.bstack1lll1111ll_opy_ = scripts[bstack1lll1l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ྴ")]
      self.bstack11l1111l1l_opy_ = scripts[bstack1lll1l_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨྵ")]
  def bstack11l111l1l1_opy_(self, bstack111lll1lll_opy_):
    if bstack111lll1lll_opy_ != None and len(bstack111lll1lll_opy_) != 0:
      self.bstack111lll1lll_opy_ = bstack111lll1lll_opy_
  def store(self):
    try:
      with open(self.bstack111lll1l11_opy_, bstack1lll1l_opy_ (u"ࠫࡼ࠭ྶ")) as file:
        json.dump({
          bstack1lll1l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢྷ"): self.bstack111lll1lll_opy_,
          bstack1lll1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢྸ"): {
            bstack1lll1l_opy_ (u"ࠢࡴࡥࡤࡲࠧྐྵ"): self.perform_scan,
            bstack1lll1l_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧྺ"): self.bstack1ll11llll_opy_,
            bstack1lll1l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨྻ"): self.bstack1lll1111ll_opy_,
            bstack1lll1l_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣྼ"): self.bstack11l1111l1l_opy_
          }
        }, file)
    except:
      pass
  def bstack1llll111l1_opy_(self, bstack111lll1l1l_opy_):
    try:
      return any(command.get(bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ྽")) == bstack111lll1l1l_opy_ for command in self.bstack111lll1lll_opy_)
    except:
      return False
bstack1l111111l1_opy_ = bstack111lll11ll_opy_()