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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111ll11l11_opy_, bstack1l1ll111_opy_, bstack111l111l1_opy_, bstack11l1l11l1_opy_,
                                    bstack111ll1l1ll_opy_, bstack111ll11l1l_opy_, bstack111ll11ll1_opy_, bstack111l1llll1_opy_)
from bstack_utils.messages import bstack1l1llll1l1_opy_, bstack111llll1_opy_
from bstack_utils.proxy import bstack1l1l1111_opy_, bstack1l1l1lll1_opy_
bstack1l1l111l_opy_ = Config.bstack1l11111l1_opy_()
logger = logging.getLogger(__name__)
def bstack11l111lll1_opy_(config):
    return config[bstack1lll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪኼ")]
def bstack111llllll1_opy_(config):
    return config[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬኽ")]
def bstack11lllll11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111111l11l_opy_(obj):
    values = []
    bstack111l111l11_opy_ = re.compile(bstack1lll1l_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢኾ"), re.I)
    for key in obj.keys():
        if bstack111l111l11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1l1ll1_opy_(config):
    tags = []
    tags.extend(bstack111111l11l_opy_(os.environ))
    tags.extend(bstack111111l11l_opy_(config))
    return tags
def bstack1111llll1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111l111lll_opy_(bstack1111l1l1ll_opy_):
    if not bstack1111l1l1ll_opy_:
        return bstack1lll1l_opy_ (u"ࠫࠬ኿")
    return bstack1lll1l_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨዀ").format(bstack1111l1l1ll_opy_.name, bstack1111l1l1ll_opy_.email)
def bstack11l111l11l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l1l1l11_opy_ = repo.common_dir
        info = {
            bstack1lll1l_opy_ (u"ࠨࡳࡩࡣࠥ዁"): repo.head.commit.hexsha,
            bstack1lll1l_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥዂ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1lll1l_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣዃ"): repo.active_branch.name,
            bstack1lll1l_opy_ (u"ࠤࡷࡥ࡬ࠨዄ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨዅ"): bstack111l111lll_opy_(repo.head.commit.committer),
            bstack1lll1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧ዆"): repo.head.commit.committed_datetime.isoformat(),
            bstack1lll1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧ዇"): bstack111l111lll_opy_(repo.head.commit.author),
            bstack1lll1l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦወ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣዉ"): repo.head.commit.message,
            bstack1lll1l_opy_ (u"ࠣࡴࡲࡳࡹࠨዊ"): repo.git.rev_parse(bstack1lll1l_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦዋ")),
            bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦዌ"): bstack111l1l1l11_opy_,
            bstack1lll1l_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢው"): subprocess.check_output([bstack1lll1l_opy_ (u"ࠧ࡭ࡩࡵࠤዎ"), bstack1lll1l_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤዏ"), bstack1lll1l_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥዐ")]).strip().decode(
                bstack1lll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧዑ")),
            bstack1lll1l_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦዒ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧዓ"): repo.git.rev_list(
                bstack1lll1l_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦዔ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l111ll1_opy_ = []
        for remote in remotes:
            bstack1111llllll_opy_ = {
                bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥዕ"): remote.name,
                bstack1lll1l_opy_ (u"ࠨࡵࡳ࡮ࠥዖ"): remote.url,
            }
            bstack111l111ll1_opy_.append(bstack1111llllll_opy_)
        bstack11111ll1l1_opy_ = {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ዗"): bstack1lll1l_opy_ (u"ࠣࡩ࡬ࡸࠧዘ"),
            **info,
            bstack1lll1l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥዙ"): bstack111l111ll1_opy_
        }
        bstack11111ll1l1_opy_ = bstack1111l11l11_opy_(bstack11111ll1l1_opy_)
        return bstack11111ll1l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨዚ").format(err))
        return {}
def bstack1111l11l11_opy_(bstack11111ll1l1_opy_):
    bstack1111l1111l_opy_ = bstack111l11l111_opy_(bstack11111ll1l1_opy_)
    if bstack1111l1111l_opy_ and bstack1111l1111l_opy_ > bstack111ll1l1ll_opy_:
        bstack1111ll1lll_opy_ = bstack1111l1111l_opy_ - bstack111ll1l1ll_opy_
        bstack1111lll1ll_opy_ = bstack1111l11111_opy_(bstack11111ll1l1_opy_[bstack1lll1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧዛ")], bstack1111ll1lll_opy_)
        bstack11111ll1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨዜ")] = bstack1111lll1ll_opy_
        logger.info(bstack1lll1l_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣዝ")
                    .format(bstack111l11l111_opy_(bstack11111ll1l1_opy_) / 1024))
    return bstack11111ll1l1_opy_
def bstack111l11l111_opy_(bstack11111ll1_opy_):
    try:
        if bstack11111ll1_opy_:
            bstack11111l111l_opy_ = json.dumps(bstack11111ll1_opy_)
            bstack11111l11l1_opy_ = sys.getsizeof(bstack11111l111l_opy_)
            return bstack11111l11l1_opy_
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢዞ").format(e))
    return -1
def bstack1111l11111_opy_(field, bstack111l111l1l_opy_):
    try:
        bstack11111l11ll_opy_ = len(bytes(bstack111ll11l1l_opy_, bstack1lll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧዟ")))
        bstack111111ll1l_opy_ = bytes(field, bstack1lll1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨዠ"))
        bstack1111l1lll1_opy_ = len(bstack111111ll1l_opy_)
        bstack111l1ll1ll_opy_ = ceil(bstack1111l1lll1_opy_ - bstack111l111l1l_opy_ - bstack11111l11ll_opy_)
        if bstack111l1ll1ll_opy_ > 0:
            bstack111l1l1111_opy_ = bstack111111ll1l_opy_[:bstack111l1ll1ll_opy_].decode(bstack1lll1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩዡ"), errors=bstack1lll1l_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫዢ")) + bstack111ll11l1l_opy_
            return bstack111l1l1111_opy_
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥዣ").format(e))
    return field
def bstack11ll11l1_opy_():
    env = os.environ
    if (bstack1lll1l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦዤ") in env and len(env[bstack1lll1l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧዥ")]) > 0) or (
            bstack1lll1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢዦ") in env and len(env[bstack1lll1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣዧ")]) > 0):
        return {
            bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣየ"): bstack1lll1l_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧዩ"),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣዪ"): env.get(bstack1lll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤያ")),
            bstack1lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤዬ"): env.get(bstack1lll1l_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥይ")),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣዮ"): env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤዯ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠦࡈࡏࠢደ")) == bstack1lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥዱ") and bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣዲ"))):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዳ"): bstack1lll1l_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥዴ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧድ"): env.get(bstack1lll1l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨዶ")),
            bstack1lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨዷ"): env.get(bstack1lll1l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤዸ")),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧዹ"): env.get(bstack1lll1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥዺ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠣࡅࡌࠦዻ")) == bstack1lll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢዼ") and bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥዽ"))):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤዾ"): bstack1lll1l_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣዿ"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤጀ"): env.get(bstack1lll1l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢጁ")),
            bstack1lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥጂ"): env.get(bstack1lll1l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦጃ")),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤጄ"): env.get(bstack1lll1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥጅ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠧࡉࡉࠣጆ")) == bstack1lll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦጇ") and env.get(bstack1lll1l_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣገ")) == bstack1lll1l_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥጉ"):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጊ"): bstack1lll1l_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧጋ"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጌ"): None,
            bstack1lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢግ"): None,
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧጎ"): None
        }
    if env.get(bstack1lll1l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥጏ")) and env.get(bstack1lll1l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦጐ")):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ጑"): bstack1lll1l_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨጒ"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጓ"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥጔ")),
            bstack1lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጕ"): None,
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ጖"): env.get(bstack1lll1l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ጗"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠤࡆࡍࠧጘ")) == bstack1lll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣጙ") and bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥጚ"))):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥጛ"): bstack1lll1l_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧጜ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥጝ"): env.get(bstack1lll1l_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦጞ")),
            bstack1lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦጟ"): None,
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤጠ"): env.get(bstack1lll1l_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤጡ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠧࡉࡉࠣጢ")) == bstack1lll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦጣ") and bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥጤ"))):
        return {
            bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨጥ"): bstack1lll1l_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧጦ"),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጧ"): env.get(bstack1lll1l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥጨ")),
            bstack1lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢጩ"): env.get(bstack1lll1l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦጪ")),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨጫ"): env.get(bstack1lll1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦጬ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠤࡆࡍࠧጭ")) == bstack1lll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣጮ") and bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢጯ"))):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥጰ"): bstack1lll1l_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨጱ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥጲ"): env.get(bstack1lll1l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧጳ")),
            bstack1lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦጴ"): env.get(bstack1lll1l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣጵ")),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጶ"): env.get(bstack1lll1l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣጷ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠨࡃࡊࠤጸ")) == bstack1lll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧጹ") and bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦጺ"))):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጻ"): bstack1lll1l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨጼ"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጽ"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦጾ")),
            bstack1lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጿ"): env.get(bstack1lll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤፀ")) or env.get(bstack1lll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦፁ")),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣፂ"): env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧፃ"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨፄ"))):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥፅ"): bstack1lll1l_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨፆ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥፇ"): bstack1lll1l_opy_ (u"ࠣࡽࢀࡿࢂࠨፈ").format(env.get(bstack1lll1l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬፉ")), env.get(bstack1lll1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪፊ"))),
            bstack1lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨፋ"): env.get(bstack1lll1l_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦፌ")),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧፍ"): env.get(bstack1lll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢፎ"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥፏ"))):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢፐ"): bstack1lll1l_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧፑ"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢፒ"): bstack1lll1l_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦፓ").format(env.get(bstack1lll1l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬፔ")), env.get(bstack1lll1l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨፕ")), env.get(bstack1lll1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩፖ")), env.get(bstack1lll1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ፗ"))),
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧፘ"): env.get(bstack1lll1l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣፙ")),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦፚ"): env.get(bstack1lll1l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ፛"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣ፜")) and env.get(bstack1lll1l_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ፝")):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ፞"): bstack1lll1l_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧ፟"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ፠"): bstack1lll1l_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣ፡").format(env.get(bstack1lll1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ።")), env.get(bstack1lll1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬ፣")), env.get(bstack1lll1l_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨ፤"))),
            bstack1lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ፥"): env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ፦")),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፧"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ፨"))
        }
    if any([env.get(bstack1lll1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ፩")), env.get(bstack1lll1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ፪")), env.get(bstack1lll1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ፫"))]):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ፬"): bstack1lll1l_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ፭"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ፮"): env.get(bstack1lll1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ፯")),
            bstack1lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ፰"): env.get(bstack1lll1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ፱")),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ፲"): env.get(bstack1lll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ፳"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ፴")):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ፵"): bstack1lll1l_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧ፶"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ፷"): env.get(bstack1lll1l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤ፸")),
            bstack1lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ፹"): env.get(bstack1lll1l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣ፺")),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ፻"): env.get(bstack1lll1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ፼"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨ፽")) or env.get(bstack1lll1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ፾")):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ፿"): bstack1lll1l_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᎀ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᎁ"): env.get(bstack1lll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᎂ")),
            bstack1lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᎃ"): bstack1lll1l_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᎄ") if env.get(bstack1lll1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᎅ")) else None,
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎆ"): env.get(bstack1lll1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᎇ"))
        }
    if any([env.get(bstack1lll1l_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᎈ")), env.get(bstack1lll1l_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᎉ")), env.get(bstack1lll1l_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᎊ"))]):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎋ"): bstack1lll1l_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᎌ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᎍ"): None,
            bstack1lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᎎ"): env.get(bstack1lll1l_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᎏ")),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᎐"): env.get(bstack1lll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᎑"))
        }
    if env.get(bstack1lll1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣ᎒")):
        return {
            bstack1lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᎓"): bstack1lll1l_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥ᎔"),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᎕"): env.get(bstack1lll1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᎖")),
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᎗"): bstack1lll1l_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧ᎘").format(env.get(bstack1lll1l_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨ᎙"))) if env.get(bstack1lll1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤ᎚")) else None,
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᎛"): env.get(bstack1lll1l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᎜"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ᎝"))):
        return {
            bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᎞"): bstack1lll1l_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ᎟"),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎠ"): env.get(bstack1lll1l_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥᎡ")),
            bstack1lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎢ"): env.get(bstack1lll1l_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦᎣ")),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᎤ"): env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᎥ"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᎦ"))):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎧ"): bstack1lll1l_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᎨ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᎩ"): bstack1lll1l_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᎪ").format(env.get(bstack1lll1l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭Ꭻ")), env.get(bstack1lll1l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᎬ")), env.get(bstack1lll1l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᎭ"))),
            bstack1lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎮ"): env.get(bstack1lll1l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᎯ")),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎰ"): env.get(bstack1lll1l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᎱ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠤࡆࡍࠧᎲ")) == bstack1lll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᎳ") and env.get(bstack1lll1l_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦᎴ")) == bstack1lll1l_opy_ (u"ࠧ࠷ࠢᎵ"):
        return {
            bstack1lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎶ"): bstack1lll1l_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢᎷ"),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎸ"): bstack1lll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧᎹ").format(env.get(bstack1lll1l_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧᎺ"))),
            bstack1lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᎻ"): None,
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᎼ"): None,
        }
    if env.get(bstack1lll1l_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤᎽ")):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᎾ"): bstack1lll1l_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥᎿ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᏀ"): None,
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏁ"): env.get(bstack1lll1l_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧᏂ")),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏃ"): env.get(bstack1lll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᏄ"))
        }
    if any([env.get(bstack1lll1l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥᏅ")), env.get(bstack1lll1l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣᏆ")), env.get(bstack1lll1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢᏇ")), env.get(bstack1lll1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦᏈ"))]):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᏉ"): bstack1lll1l_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣᏊ"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᏋ"): None,
            bstack1lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏌ"): env.get(bstack1lll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᏍ")) or None,
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏎ"): env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᏏ"), 0)
        }
    if env.get(bstack1lll1l_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᏐ")):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏑ"): bstack1lll1l_opy_ (u"ࠨࡇࡰࡅࡇࠦᏒ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏓ"): None,
            bstack1lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᏔ"): env.get(bstack1lll1l_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᏕ")),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᏖ"): env.get(bstack1lll1l_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥᏗ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᏘ")):
        return {
            bstack1lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏙ"): bstack1lll1l_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᏚ"),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᏛ"): env.get(bstack1lll1l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᏜ")),
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏝ"): env.get(bstack1lll1l_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᏞ")),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏟ"): env.get(bstack1lll1l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᏠ"))
        }
    return {bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᏡ"): None}
def get_host_info():
    return {
        bstack1lll1l_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥᏢ"): platform.node(),
        bstack1lll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᏣ"): platform.system(),
        bstack1lll1l_opy_ (u"ࠥࡸࡾࡶࡥࠣᏤ"): platform.machine(),
        bstack1lll1l_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᏥ"): platform.version(),
        bstack1lll1l_opy_ (u"ࠧࡧࡲࡤࡪࠥᏦ"): platform.architecture()[0]
    }
def bstack11lllll1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111l11l1l_opy_():
    if bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᏧ")):
        return bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ꮸ")
    return bstack1lll1l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧᏩ")
def bstack111l1111l1_opy_(driver):
    info = {
        bstack1lll1l_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᏪ"): driver.capabilities,
        bstack1lll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧᏫ"): driver.session_id,
        bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᏬ"): driver.capabilities.get(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᏭ"), None),
        bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᏮ"): driver.capabilities.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᏯ"), None),
        bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᏰ"): driver.capabilities.get(bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᏱ"), None),
    }
    if bstack1111l11l1l_opy_() == bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᏲ"):
        info[bstack1lll1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᏳ")] = bstack1lll1l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᏴ") if bstack11l111l11_opy_() else bstack1lll1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᏵ")
    return info
def bstack11l111l11_opy_():
    if bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᏶")):
        return True
    if bstack1l1lllll1l_opy_(os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᏷"), None)):
        return True
    return False
def bstack1l1l11l1_opy_(bstack111l1l11l1_opy_, url, data, config):
    headers = config.get(bstack1lll1l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᏸ"), None)
    proxies = bstack1l1l1111_opy_(config, url)
    auth = config.get(bstack1lll1l_opy_ (u"ࠪࡥࡺࡺࡨࠨᏹ"), None)
    response = requests.request(
            bstack111l1l11l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l111l1l1_opy_(bstack1ll111l1l_opy_, size):
    bstack11111lll_opy_ = []
    while len(bstack1ll111l1l_opy_) > size:
        bstack1l11111ll_opy_ = bstack1ll111l1l_opy_[:size]
        bstack11111lll_opy_.append(bstack1l11111ll_opy_)
        bstack1ll111l1l_opy_ = bstack1ll111l1l_opy_[size:]
    bstack11111lll_opy_.append(bstack1ll111l1l_opy_)
    return bstack11111lll_opy_
def bstack1111ll111l_opy_(message, bstack1111l111l1_opy_=False):
    os.write(1, bytes(message, bstack1lll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᏺ")))
    os.write(1, bytes(bstack1lll1l_opy_ (u"ࠬࡢ࡮ࠨᏻ"), bstack1lll1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᏼ")))
    if bstack1111l111l1_opy_:
        with open(bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭ᏽ") + os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᏾")] + bstack1lll1l_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ᏿"), bstack1lll1l_opy_ (u"ࠪࡥࠬ᐀")) as f:
            f.write(message + bstack1lll1l_opy_ (u"ࠫࡡࡴࠧᐁ"))
def bstack11111l1l1l_opy_():
    return os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᐂ")].lower() == bstack1lll1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᐃ")
def bstack1l11lll1_opy_(bstack111l1ll111_opy_):
    return bstack1lll1l_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᐄ").format(bstack111ll11l11_opy_, bstack111l1ll111_opy_)
def bstack11l111ll1_opy_():
    return bstack11ll1ll1ll_opy_().replace(tzinfo=None).isoformat() + bstack1lll1l_opy_ (u"ࠨ࡜ࠪᐅ")
def bstack1111l1l1l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1lll1l_opy_ (u"ࠩ࡝ࠫᐆ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1lll1l_opy_ (u"ࠪ࡞ࠬᐇ")))).total_seconds() * 1000
def bstack111l11ll11_opy_(timestamp):
    return bstack111l1111ll_opy_(timestamp).isoformat() + bstack1lll1l_opy_ (u"ࠫ࡟࠭ᐈ")
def bstack111111l111_opy_(bstack111111l1ll_opy_):
    date_format = bstack1lll1l_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᐉ")
    bstack111l111111_opy_ = datetime.datetime.strptime(bstack111111l1ll_opy_, date_format)
    return bstack111l111111_opy_.isoformat() + bstack1lll1l_opy_ (u"࡚࠭ࠨᐊ")
def bstack11111lllll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐋ")
    else:
        return bstack1lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᐌ")
def bstack1l1lllll1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1lll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᐍ")
def bstack1111l11lll_opy_(val):
    return val.__str__().lower() == bstack1lll1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᐎ")
def bstack11ll1l1lll_opy_(bstack1111ll11l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111ll11l1_opy_ as e:
                print(bstack1lll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᐏ").format(func.__name__, bstack1111ll11l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111111llll_opy_(bstack111l11llll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l11llll_opy_(cls, *args, **kwargs)
            except bstack1111ll11l1_opy_ as e:
                print(bstack1lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᐐ").format(bstack111l11llll_opy_.__name__, bstack1111ll11l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111111llll_opy_
    else:
        return decorator
def bstack1l11l1l111_opy_(bstack11l1l1l1l1_opy_):
    if bstack1lll1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᐑ") in bstack11l1l1l1l1_opy_ and bstack1111l11lll_opy_(bstack11l1l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᐒ")]):
        return False
    if bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᐓ") in bstack11l1l1l1l1_opy_ and bstack1111l11lll_opy_(bstack11l1l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᐔ")]):
        return False
    return True
def bstack11ll1111_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll11l1l1_opy_(hub_url):
    if bstack1111l1l1l_opy_() <= version.parse(bstack1lll1l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪᐕ")):
        if hub_url != bstack1lll1l_opy_ (u"ࠫࠬᐖ"):
            return bstack1lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᐗ") + hub_url + bstack1lll1l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥᐘ")
        return bstack111l111l1_opy_
    if hub_url != bstack1lll1l_opy_ (u"ࠧࠨᐙ"):
        return bstack1lll1l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᐚ") + hub_url + bstack1lll1l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᐛ")
    return bstack11l1l11l1_opy_
def bstack1111lll11l_opy_():
    return isinstance(os.getenv(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩᐜ")), str)
def bstack1ll1111l11_opy_(url):
    return urlparse(url).hostname
def bstack111ll1l11_opy_(hostname):
    for bstack11l1llll_opy_ in bstack1l1ll111_opy_:
        regex = re.compile(bstack11l1llll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111111ll11_opy_(bstack1111llll11_opy_, file_name, logger):
    bstack111l111l_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠫࢃ࠭ᐝ")), bstack1111llll11_opy_)
    try:
        if not os.path.exists(bstack111l111l_opy_):
            os.makedirs(bstack111l111l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠬࢄࠧᐞ")), bstack1111llll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1lll1l_opy_ (u"࠭ࡷࠨᐟ")):
                pass
            with open(file_path, bstack1lll1l_opy_ (u"ࠢࡸ࠭ࠥᐠ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1llll1l1_opy_.format(str(e)))
def bstack11111l1111_opy_(file_name, key, value, logger):
    file_path = bstack111111ll11_opy_(bstack1lll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᐡ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11111ll1_opy_ = json.load(open(file_path, bstack1lll1l_opy_ (u"ࠩࡵࡦࠬᐢ")))
        else:
            bstack1l11111ll1_opy_ = {}
        bstack1l11111ll1_opy_[key] = value
        with open(file_path, bstack1lll1l_opy_ (u"ࠥࡻ࠰ࠨᐣ")) as outfile:
            json.dump(bstack1l11111ll1_opy_, outfile)
def bstack1lll1ll1_opy_(file_name, logger):
    file_path = bstack111111ll11_opy_(bstack1lll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᐤ"), file_name, logger)
    bstack1l11111ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1lll1l_opy_ (u"ࠬࡸࠧᐥ")) as bstack1l111l111l_opy_:
            bstack1l11111ll1_opy_ = json.load(bstack1l111l111l_opy_)
    return bstack1l11111ll1_opy_
def bstack111ll111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪᐦ") + file_path + bstack1lll1l_opy_ (u"ࠧࠡࠩᐧ") + str(e))
def bstack1111l1l1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1lll1l_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥᐨ")
def bstack1lll1lll1_opy_(config):
    if bstack1lll1l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᐩ") in config:
        del (config[bstack1lll1l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᐪ")])
        return False
    if bstack1111l1l1l_opy_() < version.parse(bstack1lll1l_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪᐫ")):
        return False
    if bstack1111l1l1l_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫᐬ")):
        return True
    if bstack1lll1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᐭ") in config and config[bstack1lll1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᐮ")] is False:
        return False
    else:
        return True
def bstack1llll11ll_opy_(args_list, bstack111l1ll11l_opy_):
    index = -1
    for value in bstack111l1ll11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11llll1l1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11llll1l1l_opy_ = bstack11llll1l1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᐯ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᐰ"), exception=exception)
    def bstack11l11ll111_opy_(self):
        if self.result != bstack1lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᐱ"):
            return None
        if isinstance(self.exception_type, str) and bstack1lll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᐲ") in self.exception_type:
            return bstack1lll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᐳ")
        return bstack1lll1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᐴ")
    def bstack1111111lll_opy_(self):
        if self.result != bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐵ"):
            return None
        if self.bstack11llll1l1l_opy_:
            return self.bstack11llll1l1l_opy_
        return bstack1111l1ll11_opy_(self.exception)
def bstack1111l1ll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11111lll1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll111lll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1llll111l_opy_(config, logger):
    try:
        import playwright
        bstack1111l1llll_opy_ = playwright.__file__
        bstack11111lll11_opy_ = os.path.split(bstack1111l1llll_opy_)
        bstack11111llll1_opy_ = bstack11111lll11_opy_[0] + bstack1lll1l_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫᐶ")
        os.environ[bstack1lll1l_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬᐷ")] = bstack1l1l1lll1_opy_(config)
        with open(bstack11111llll1_opy_, bstack1lll1l_opy_ (u"ࠪࡶࠬᐸ")) as f:
            bstack1l1l1lllll_opy_ = f.read()
            bstack1111lll1l1_opy_ = bstack1lll1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪᐹ")
            bstack111l11lll1_opy_ = bstack1l1l1lllll_opy_.find(bstack1111lll1l1_opy_)
            if bstack111l11lll1_opy_ == -1:
              process = subprocess.Popen(bstack1lll1l_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤᐺ"), shell=True, cwd=bstack11111lll11_opy_[0])
              process.wait()
              bstack11111ll111_opy_ = bstack1lll1l_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ᐻ")
              bstack111l11l1l1_opy_ = bstack1lll1l_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦᐼ")
              bstack111l11l11l_opy_ = bstack1l1l1lllll_opy_.replace(bstack11111ll111_opy_, bstack111l11l1l1_opy_)
              with open(bstack11111llll1_opy_, bstack1lll1l_opy_ (u"ࠨࡹࠪᐽ")) as f:
                f.write(bstack111l11l11l_opy_)
    except Exception as e:
        logger.error(bstack111llll1_opy_.format(str(e)))
def bstack1llll11ll1_opy_():
  try:
    bstack1111lll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᐾ"))
    bstack11111ll1ll_opy_ = []
    if os.path.exists(bstack1111lll111_opy_):
      with open(bstack1111lll111_opy_) as f:
        bstack11111ll1ll_opy_ = json.load(f)
      os.remove(bstack1111lll111_opy_)
    return bstack11111ll1ll_opy_
  except:
    pass
  return []
def bstack1l1l1ll11_opy_(bstack1l11l11111_opy_):
  try:
    bstack11111ll1ll_opy_ = []
    bstack1111lll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᐿ"))
    if os.path.exists(bstack1111lll111_opy_):
      with open(bstack1111lll111_opy_) as f:
        bstack11111ll1ll_opy_ = json.load(f)
    bstack11111ll1ll_opy_.append(bstack1l11l11111_opy_)
    with open(bstack1111lll111_opy_, bstack1lll1l_opy_ (u"ࠫࡼ࠭ᑀ")) as f:
        json.dump(bstack11111ll1ll_opy_, f)
  except:
    pass
def bstack1lll1l1ll_opy_(logger, bstack1111ll1l11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1lll1l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᑁ"), bstack1lll1l_opy_ (u"࠭ࠧᑂ"))
    if test_name == bstack1lll1l_opy_ (u"ࠧࠨᑃ"):
        test_name = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧᑄ"), bstack1lll1l_opy_ (u"ࠩࠪᑅ"))
    bstack111l1l111l_opy_ = bstack1lll1l_opy_ (u"ࠪ࠰ࠥ࠭ᑆ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111ll1l11_opy_:
        bstack1llllll1l1_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᑇ"), bstack1lll1l_opy_ (u"ࠬ࠶ࠧᑈ"))
        bstack1ll11111ll_opy_ = {bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᑉ"): test_name, bstack1lll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᑊ"): bstack111l1l111l_opy_, bstack1lll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᑋ"): bstack1llllll1l1_opy_}
        bstack1111ll11ll_opy_ = []
        bstack1111lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᑌ"))
        if os.path.exists(bstack1111lllll1_opy_):
            with open(bstack1111lllll1_opy_) as f:
                bstack1111ll11ll_opy_ = json.load(f)
        bstack1111ll11ll_opy_.append(bstack1ll11111ll_opy_)
        with open(bstack1111lllll1_opy_, bstack1lll1l_opy_ (u"ࠪࡻࠬᑍ")) as f:
            json.dump(bstack1111ll11ll_opy_, f)
    else:
        bstack1ll11111ll_opy_ = {bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᑎ"): test_name, bstack1lll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᑏ"): bstack111l1l111l_opy_, bstack1lll1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᑐ"): str(multiprocessing.current_process().name)}
        if bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫᑑ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11111ll_opy_)
  except Exception as e:
      logger.warn(bstack1lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᑒ").format(e))
def bstack1l11ll1lll_opy_(error_message, test_name, index, logger):
  try:
    bstack111l11111l_opy_ = []
    bstack1ll11111ll_opy_ = {bstack1lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᑓ"): test_name, bstack1lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᑔ"): error_message, bstack1lll1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᑕ"): index}
    bstack11111l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᑖ"))
    if os.path.exists(bstack11111l1ll1_opy_):
        with open(bstack11111l1ll1_opy_) as f:
            bstack111l11111l_opy_ = json.load(f)
    bstack111l11111l_opy_.append(bstack1ll11111ll_opy_)
    with open(bstack11111l1ll1_opy_, bstack1lll1l_opy_ (u"࠭ࡷࠨᑗ")) as f:
        json.dump(bstack111l11111l_opy_, f)
  except Exception as e:
    logger.warn(bstack1lll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᑘ").format(e))
def bstack1l1l1ll1l1_opy_(bstack1l1llll1l_opy_, name, logger):
  try:
    bstack1ll11111ll_opy_ = {bstack1lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑙ"): name, bstack1lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᑚ"): bstack1l1llll1l_opy_, bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᑛ"): str(threading.current_thread()._name)}
    return bstack1ll11111ll_opy_
  except Exception as e:
    logger.warn(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᑜ").format(e))
  return
def bstack111111l1l1_opy_():
    return platform.system() == bstack1lll1l_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭ᑝ")
def bstack1lll1ll1l1_opy_(bstack111l11ll1l_opy_, config, logger):
    bstack1111l1l11l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l11ll1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁࠧᑞ").format(e))
    return bstack1111l1l11l_opy_
def bstack1111ll1ll1_opy_(bstack111l1l1l1l_opy_, bstack1111l111ll_opy_):
    bstack1111l1ll1l_opy_ = version.parse(bstack111l1l1l1l_opy_)
    bstack11111l1lll_opy_ = version.parse(bstack1111l111ll_opy_)
    if bstack1111l1ll1l_opy_ > bstack11111l1lll_opy_:
        return 1
    elif bstack1111l1ll1l_opy_ < bstack11111l1lll_opy_:
        return -1
    else:
        return 0
def bstack11ll1ll1ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1111ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111ll1111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1l1l11_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack1lll1l_opy_ (u"ࠧࡨࡧࡷࠫᑟ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack111111l1_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᑠ"))
    bstack111l11l1ll_opy_ = True
    if bstack1111l11lll_opy_(caps.get(bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨᑡ"))) or bstack1111l11lll_opy_(caps.get(bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪᑢ"))):
        bstack111l11l1ll_opy_ = False
    if bstack1lll1lll1_opy_({bstack1lll1l_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦᑣ"): bstack111l11l1ll_opy_}):
        bstack111111l1_opy_ = bstack111111l1_opy_ or {}
        bstack111111l1_opy_[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᑤ")] = bstack1111ll1111_opy_(framework)
        bstack111111l1_opy_[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᑥ")] = bstack11111l1l1l_opy_()
        if getattr(options, bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᑦ"), None):
            options.set_capability(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᑧ"), bstack111111l1_opy_)
        else:
            options[bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᑨ")] = bstack111111l1_opy_
    else:
        if getattr(options, bstack1lll1l_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫᑩ"), None):
            options.set_capability(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᑪ"), bstack1111ll1111_opy_(framework))
            options.set_capability(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᑫ"), bstack11111l1l1l_opy_())
        else:
            options[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᑬ")] = bstack1111ll1111_opy_(framework)
            options[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᑭ")] = bstack11111l1l1l_opy_()
    return options
def bstack11111l1l11_opy_(bstack111l1l1lll_opy_, framework):
    if bstack111l1l1lll_opy_ and len(bstack111l1l1lll_opy_.split(bstack1lll1l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᑮ"))) > 1:
        ws_url = bstack111l1l1lll_opy_.split(bstack1lll1l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᑯ"))[0]
        if bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᑰ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111ll11l_opy_ = json.loads(urllib.parse.unquote(bstack111l1l1lll_opy_.split(bstack1lll1l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᑱ"))[1]))
            bstack11111ll11l_opy_ = bstack11111ll11l_opy_ or {}
            bstack11111ll11l_opy_[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᑲ")] = str(framework) + str(__version__)
            bstack11111ll11l_opy_[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᑳ")] = bstack11111l1l1l_opy_()
            bstack111l1l1lll_opy_ = bstack111l1l1lll_opy_.split(bstack1lll1l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᑴ"))[0] + bstack1lll1l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᑵ") + urllib.parse.quote(json.dumps(bstack11111ll11l_opy_))
    return bstack111l1l1lll_opy_
def bstack1l1ll1l11l_opy_():
    global bstack11ll11l1l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11ll11l1l_opy_ = BrowserType.connect
    return bstack11ll11l1l_opy_
def bstack1l111l1ll1_opy_(framework_name):
    global bstack1ll1lllll_opy_
    bstack1ll1lllll_opy_ = framework_name
    return framework_name
def bstack1l1l111l11_opy_(self, *args, **kwargs):
    global bstack11ll11l1l_opy_
    try:
        global bstack1ll1lllll_opy_
        if bstack1lll1l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᑶ") in kwargs:
            kwargs[bstack1lll1l_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᑷ")] = bstack11111l1l11_opy_(
                kwargs.get(bstack1lll1l_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᑸ"), None),
                bstack1ll1lllll_opy_
            )
    except Exception as e:
        logger.error(bstack1lll1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧᑹ").format(str(e)))
    return bstack11ll11l1l_opy_(self, *args, **kwargs)
def bstack1111ll1l1l_opy_(bstack1111l11ll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1l1111_opy_(bstack1111l11ll1_opy_, bstack1lll1l_opy_ (u"ࠨࠢᑺ"))
        if proxies and proxies.get(bstack1lll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᑻ")):
            parsed_url = urlparse(proxies.get(bstack1lll1l_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᑼ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬᑽ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᑾ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1lll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᑿ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1lll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨᒀ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll1l1ll_opy_(bstack1111l11ll1_opy_):
    bstack1111l1l111_opy_ = {
        bstack111l1llll1_opy_[bstack111l1l11ll_opy_]: bstack1111l11ll1_opy_[bstack111l1l11ll_opy_]
        for bstack111l1l11ll_opy_ in bstack1111l11ll1_opy_
        if bstack111l1l11ll_opy_ in bstack111l1llll1_opy_
    }
    bstack1111l1l111_opy_[bstack1lll1l_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᒁ")] = bstack1111ll1l1l_opy_(bstack1111l11ll1_opy_, bstack1l1l111l_opy_.get_property(bstack1lll1l_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢᒂ")))
    bstack111l1ll1l1_opy_ = [element.lower() for element in bstack111ll11ll1_opy_]
    bstack111111lll1_opy_(bstack1111l1l111_opy_, bstack111l1ll1l1_opy_)
    return bstack1111l1l111_opy_
def bstack111111lll1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1lll1l_opy_ (u"ࠣࠬ࠭࠮࠯ࠨᒃ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111111lll1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111111lll1_opy_(item, keys)