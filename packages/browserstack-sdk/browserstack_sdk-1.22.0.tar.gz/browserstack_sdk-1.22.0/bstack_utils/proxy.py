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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll11lll_opy_
bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
def bstack1lll11ll1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll11llll1_opy_(bstack1lll11ll1l1_opy_, bstack1lll1l11111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll11ll1l1_opy_):
        with open(bstack1lll11ll1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll11ll1ll_opy_(bstack1lll11ll1l1_opy_):
        pac = get_pac(url=bstack1lll11ll1l1_opy_)
    else:
        raise Exception(bstack1lll1l_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ᖒ").format(bstack1lll11ll1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lll1l_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣᖓ"), 80))
        bstack1lll11lll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll11lll11_opy_ = bstack1lll1l_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩᖔ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1l11111_opy_, bstack1lll11lll11_opy_)
    return proxy_url
def bstack1llll1ll11_opy_(config):
    return bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᖕ") in config or bstack1lll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᖖ") in config
def bstack1l1l1lll1_opy_(config):
    if not bstack1llll1ll11_opy_(config):
        return
    if config.get(bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᖗ")):
        return config.get(bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᖘ"))
    if config.get(bstack1lll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᖙ")):
        return config.get(bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᖚ"))
def bstack1l1l1111_opy_(config, bstack1lll1l11111_opy_):
    proxy = bstack1l1l1lll1_opy_(config)
    proxies = {}
    if config.get(bstack1lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᖛ")) or config.get(bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᖜ")):
        if proxy.endswith(bstack1lll1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᖝ")):
            proxies = bstack1llll111ll_opy_(proxy, bstack1lll1l11111_opy_)
        else:
            proxies = {
                bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖞ"): proxy
            }
    bstack1l1l111l_opy_.bstack111l11l11_opy_(bstack1lll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬᖟ"), proxies)
    return proxies
def bstack1llll111ll_opy_(bstack1lll11ll1l1_opy_, bstack1lll1l11111_opy_):
    proxies = {}
    global bstack1lll11lllll_opy_
    if bstack1lll1l_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩᖠ") in globals():
        return bstack1lll11lllll_opy_
    try:
        proxy = bstack1lll11llll1_opy_(bstack1lll11ll1l1_opy_, bstack1lll1l11111_opy_)
        if bstack1lll1l_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢᖡ") in proxy:
            proxies = {}
        elif bstack1lll1l_opy_ (u"ࠣࡊࡗࡘࡕࠨᖢ") in proxy or bstack1lll1l_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣᖣ") in proxy or bstack1lll1l_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤᖤ") in proxy:
            bstack1lll11lll1l_opy_ = proxy.split(bstack1lll1l_opy_ (u"ࠦࠥࠨᖥ"))
            if bstack1lll1l_opy_ (u"ࠧࡀ࠯࠰ࠤᖦ") in bstack1lll1l_opy_ (u"ࠨࠢᖧ").join(bstack1lll11lll1l_opy_[1:]):
                proxies = {
                    bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᖨ"): bstack1lll1l_opy_ (u"ࠣࠤᖩ").join(bstack1lll11lll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᖪ"): str(bstack1lll11lll1l_opy_[0]).lower() + bstack1lll1l_opy_ (u"ࠥ࠾࠴࠵ࠢᖫ") + bstack1lll1l_opy_ (u"ࠦࠧᖬ").join(bstack1lll11lll1l_opy_[1:])
                }
        elif bstack1lll1l_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᖭ") in proxy:
            bstack1lll11lll1l_opy_ = proxy.split(bstack1lll1l_opy_ (u"ࠨࠠࠣᖮ"))
            if bstack1lll1l_opy_ (u"ࠢ࠻࠱࠲ࠦᖯ") in bstack1lll1l_opy_ (u"ࠣࠤᖰ").join(bstack1lll11lll1l_opy_[1:]):
                proxies = {
                    bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᖱ"): bstack1lll1l_opy_ (u"ࠥࠦᖲ").join(bstack1lll11lll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖳ"): bstack1lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᖴ") + bstack1lll1l_opy_ (u"ࠨࠢᖵ").join(bstack1lll11lll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᖶ"): proxy
            }
    except Exception as e:
        print(bstack1lll1l_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᖷ"), bstack1lllll11lll_opy_.format(bstack1lll11ll1l1_opy_, str(e)))
    bstack1lll11lllll_opy_ = proxies
    return proxies