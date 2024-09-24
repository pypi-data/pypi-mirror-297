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
from uuid import uuid4
from bstack_utils.helper import bstack11l111ll1_opy_, bstack1111l1l1l1_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack1lll11l11ll_opy_
class bstack11ll11l1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11llll1111_opy_=None, framework=None, tags=[], scope=[], bstack1ll1lll11ll_opy_=None, bstack1ll1ll1l111_opy_=True, bstack1ll1ll1l1l1_opy_=None, bstack1lll111l1l_opy_=None, result=None, duration=None, bstack11l1ll11ll_opy_=None, meta={}):
        self.bstack11l1ll11ll_opy_ = bstack11l1ll11ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1ll1l111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11llll1111_opy_ = bstack11llll1111_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
        self.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1l1l1_opy_
        self.bstack1lll111l1l_opy_ = bstack1lll111l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11ll1ll11l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11llll11ll_opy_(self, meta):
        self.meta = meta
    def bstack1ll1lll1111_opy_(self):
        bstack1ll1ll1ll11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᘡ"): bstack1ll1ll1ll11_opy_,
            bstack1lll1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᘢ"): bstack1ll1ll1ll11_opy_,
            bstack1lll1l_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᘣ"): bstack1ll1ll1ll11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1lll1l_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨᘤ") + key)
            setattr(self, key, val)
    def bstack1ll1ll11lll_opy_(self):
        return {
            bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᘥ"): self.name,
            bstack1lll1l_opy_ (u"ࠧࡣࡱࡧࡽࠬᘦ"): {
                bstack1lll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᘧ"): bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᘨ"),
                bstack1lll1l_opy_ (u"ࠪࡧࡴࡪࡥࠨᘩ"): self.code
            },
            bstack1lll1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᘪ"): self.scope,
            bstack1lll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪᘫ"): self.tags,
            bstack1lll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᘬ"): self.framework,
            bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᘭ"): self.bstack11llll1111_opy_
        }
    def bstack1ll1ll1ll1l_opy_(self):
        return {
         bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᘮ"): self.meta
        }
    def bstack1ll1ll11ll1_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᘯ"): {
                bstack1lll1l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᘰ"): self.bstack1ll1lll11ll_opy_
            }
        }
    def bstack1ll1ll11l1l_opy_(self, bstack1ll1ll1l1ll_opy_, details):
        step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧᘱ")] == bstack1ll1ll1l1ll_opy_, self.meta[bstack1lll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᘲ")]), None)
        step.update(details)
    def bstack1ll11lll11_opy_(self, bstack1ll1ll1l1ll_opy_):
        step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"࠭ࡩࡥࠩᘳ")] == bstack1ll1ll1l1ll_opy_, self.meta[bstack1lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᘴ")]), None)
        step.update({
            bstack1lll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘵ"): bstack11l111ll1_opy_()
        })
    def bstack11lll111l1_opy_(self, bstack1ll1ll1l1ll_opy_, result, duration=None):
        bstack1ll1ll1l1l1_opy_ = bstack11l111ll1_opy_()
        if bstack1ll1ll1l1ll_opy_ is not None and self.meta.get(bstack1lll1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᘶ")):
            step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭ᘷ")] == bstack1ll1ll1l1ll_opy_, self.meta[bstack1lll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᘸ")]), None)
            step.update({
                bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘹ"): bstack1ll1ll1l1l1_opy_,
                bstack1lll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᘺ"): duration if duration else bstack1111l1l1l1_opy_(step[bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᘻ")], bstack1ll1ll1l1l1_opy_),
                bstack1lll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘼ"): result.result,
                bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᘽ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1lll1ll1_opy_):
        if self.meta.get(bstack1lll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᘾ")):
            self.meta[bstack1lll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᘿ")].append(bstack1ll1lll1ll1_opy_)
        else:
            self.meta[bstack1lll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᙀ")] = [ bstack1ll1lll1ll1_opy_ ]
    def bstack1ll1lll1lll_opy_(self):
        return {
            bstack1lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙁ"): self.bstack11ll1ll11l_opy_(),
            **self.bstack1ll1ll11lll_opy_(),
            **self.bstack1ll1lll1111_opy_(),
            **self.bstack1ll1ll1ll1l_opy_()
        }
    def bstack1ll1ll1llll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1lll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙂ"): self.bstack1ll1ll1l1l1_opy_,
            bstack1lll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᙃ"): self.duration,
            bstack1lll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙄ"): self.result.result
        }
        if data[bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙅ")] == bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᙆ"):
            data[bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᙇ")] = self.result.bstack11l11ll111_opy_()
            data[bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᙈ")] = [{bstack1lll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᙉ"): self.result.bstack1111111lll_opy_()}]
        return data
    def bstack1ll1lll11l1_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᙊ"): self.bstack11ll1ll11l_opy_(),
            **self.bstack1ll1ll11lll_opy_(),
            **self.bstack1ll1lll1111_opy_(),
            **self.bstack1ll1ll1llll_opy_(),
            **self.bstack1ll1ll1ll1l_opy_()
        }
    def bstack11ll111l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1lll1l_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪᙋ") in event:
            return self.bstack1ll1lll1lll_opy_()
        elif bstack1lll1l_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᙌ") in event:
            return self.bstack1ll1lll11l1_opy_()
    def bstack11ll1l11l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1ll1l1l1_opy_ = time if time else bstack11l111ll1_opy_()
        self.duration = duration if duration else bstack1111l1l1l1_opy_(self.bstack11llll1111_opy_, self.bstack1ll1ll1l1l1_opy_)
        if result:
            self.result = result
class bstack11lll1l111_opy_(bstack11ll11l1ll_opy_):
    def __init__(self, hooks=[], bstack11ll1l1111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11ll1l1111_opy_ = bstack11ll1l1111_opy_
        super().__init__(*args, **kwargs, bstack1lll111l1l_opy_=bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᙍ"))
    @classmethod
    def bstack1ll1ll1lll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨᙎ"): id(step),
                bstack1lll1l_opy_ (u"࠭ࡴࡦࡺࡷࠫᙏ"): step.name,
                bstack1lll1l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᙐ"): step.keyword,
            })
        return bstack11lll1l111_opy_(
            **kwargs,
            meta={
                bstack1lll1l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᙑ"): {
                    bstack1lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᙒ"): feature.name,
                    bstack1lll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨᙓ"): feature.filename,
                    bstack1lll1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᙔ"): feature.description
                },
                bstack1lll1l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᙕ"): {
                    bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙖ"): scenario.name
                },
                bstack1lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᙗ"): steps,
                bstack1lll1l_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᙘ"): bstack1lll11l11ll_opy_(test)
            }
        )
    def bstack1ll1lll1l11_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᙙ"): self.hooks
        }
    def bstack1ll1lll111l_opy_(self):
        if self.bstack11ll1l1111_opy_:
            return {
                bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᙚ"): self.bstack11ll1l1111_opy_
            }
        return {}
    def bstack1ll1lll11l1_opy_(self):
        return {
            **super().bstack1ll1lll11l1_opy_(),
            **self.bstack1ll1lll1l11_opy_()
        }
    def bstack1ll1lll1lll_opy_(self):
        return {
            **super().bstack1ll1lll1lll_opy_(),
            **self.bstack1ll1lll111l_opy_()
        }
    def bstack11ll1l11l1_opy_(self):
        return bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᙛ")
class bstack11lll111ll_opy_(bstack11ll11l1ll_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1lll1l1l_opy_ = None
        super().__init__(*args, **kwargs, bstack1lll111l1l_opy_=bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᙜ"))
    def bstack11ll1l111l_opy_(self):
        return self.hook_type
    def bstack1ll1ll1l11l_opy_(self):
        return {
            bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᙝ"): self.hook_type
        }
    def bstack1ll1lll11l1_opy_(self):
        return {
            **super().bstack1ll1lll11l1_opy_(),
            **self.bstack1ll1ll1l11l_opy_()
        }
    def bstack1ll1lll1lll_opy_(self):
        return {
            **super().bstack1ll1lll1lll_opy_(),
            bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᙞ"): self.bstack1ll1lll1l1l_opy_,
            **self.bstack1ll1ll1l11l_opy_()
        }
    def bstack11ll1l11l1_opy_(self):
        return bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᙟ")
    def bstack11lll11l11_opy_(self, bstack1ll1lll1l1l_opy_):
        self.bstack1ll1lll1l1l_opy_ = bstack1ll1lll1l1l_opy_