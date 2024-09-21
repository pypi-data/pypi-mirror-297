from .running.runner import main
from .running.conf import App
from .utils.config import kconfig
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .page import Page
from .core.adr import AdrElem, AdrTC
from .core.ios import IosElem, IosTC
from .core.web import WebElem, WebTC
from .core.api.request import HttpReq
from .core.api.case import TestCase as TC
from .core.api.genetor import generate_case

__version__ = "0.1.37"
__description__ = "API/安卓/IOS/WEB平台自动化测试框架"
