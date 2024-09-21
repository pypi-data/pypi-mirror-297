from .genetor import generate_case
from .running.runner import main
from .running.conf import App
from .utils.config import kconfig
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .core.api.case import TestCase as ApiTestCase
from .core.adr.case import TestCase as AdrTestCase
from .core.ios.case import TestCase as IosTestCase
from .core.web.case import TestCase as WebTestCase

__version__ = "0.1.36"
__description__ = "API/安卓/IOS/WEB平台自动化测试框架"
