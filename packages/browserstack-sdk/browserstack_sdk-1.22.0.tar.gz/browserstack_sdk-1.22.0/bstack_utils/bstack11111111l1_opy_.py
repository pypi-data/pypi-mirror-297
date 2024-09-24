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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111ll1ll1_opy_
from browserstack_sdk.bstack1ll1llll11_opy_ import bstack1111l11l_opy_
def _1lllllllll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111111111_opy_:
    def __init__(self, handler):
        self._1lllllll1l1_opy_ = {}
        self._1llllllllll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1111l11l_opy_.version()
        if bstack1111ll1ll1_opy_(pytest_version, bstack1lll1l_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣᒄ")) >= 0:
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒅ")] = Module._register_setup_function_fixture
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒆ")] = Module._register_setup_module_fixture
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒇ")] = Class._register_setup_class_fixture
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒈ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒉ"))
            Module._register_setup_module_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒊ"))
            Class._register_setup_class_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒋ"))
            Class._register_setup_method_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᒌ"))
        else:
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒍ")] = Module._inject_setup_function_fixture
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒎ")] = Module._inject_setup_module_fixture
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒏ")] = Class._inject_setup_class_fixture
            self._1lllllll1l1_opy_[bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒐ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᒑ"))
            Module._inject_setup_module_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒒ"))
            Class._inject_setup_class_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒓ"))
            Class._inject_setup_method_fixture = self.bstack1lllllll1ll_opy_(bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒔ"))
    def bstack1lllllll111_opy_(self, bstack1llllllll1l_opy_, hook_type):
        meth = getattr(bstack1llllllll1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1llllllllll_opy_[hook_type] = meth
            setattr(bstack1llllllll1l_opy_, hook_type, self.bstack1111111ll1_opy_(hook_type))
    def bstack111111111l_opy_(self, instance, bstack11111111ll_opy_):
        if bstack11111111ll_opy_ == bstack1lll1l_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᒕ"):
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢᒖ"))
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦᒗ"))
        if bstack11111111ll_opy_ == bstack1lll1l_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᒘ"):
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣᒙ"))
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧᒚ"))
        if bstack11111111ll_opy_ == bstack1lll1l_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᒛ"):
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥᒜ"))
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢᒝ"))
        if bstack11111111ll_opy_ == bstack1lll1l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᒞ"):
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢᒟ"))
            self.bstack1lllllll111_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦᒠ"))
    @staticmethod
    def bstack1111111l11_opy_(hook_type, func, args):
        if hook_type in [bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᒡ"), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᒢ")]:
            _1lllllllll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111111ll1_opy_(self, hook_type):
        def bstack1llllllll11_opy_(arg=None):
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᒣ"))
            result = None
            exception = None
            try:
                self.bstack1111111l11_opy_(hook_type, self._1llllllllll_opy_[hook_type], (arg,))
                result = Result(result=bstack1lll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᒤ"))
            except Exception as e:
                result = Result(result=bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᒥ"), exception=e)
                self.handler(hook_type, bstack1lll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᒦ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᒧ"), result)
        def bstack1lllllll11l_opy_(this, arg=None):
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᒨ"))
            result = None
            exception = None
            try:
                self.bstack1111111l11_opy_(hook_type, self._1llllllllll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᒩ"))
            except Exception as e:
                result = Result(result=bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᒪ"), exception=e)
                self.handler(hook_type, bstack1lll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᒫ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᒬ"), result)
        if hook_type in [bstack1lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᒭ"), bstack1lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᒮ")]:
            return bstack1lllllll11l_opy_
        return bstack1llllllll11_opy_
    def bstack1lllllll1ll_opy_(self, bstack11111111ll_opy_):
        def bstack1111111l1l_opy_(this, *args, **kwargs):
            self.bstack111111111l_opy_(this, bstack11111111ll_opy_)
            self._1lllllll1l1_opy_[bstack11111111ll_opy_](this, *args, **kwargs)
        return bstack1111111l1l_opy_