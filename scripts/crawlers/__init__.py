"""
YouthFit Multi-Strategy Policy Crawler Package
"""

from .base_crawler import BaseCrawler
from .bs4_crawler import (
    Bs4Crawler,
    BusanYouthCrawler,
    DaeguYouthCrawler,
    GwangjuYouthCrawler,
    IncheonYouthCrawler,
    ShHousingCrawler,
)
from .hidden_api_crawler import (
    GyeonggiJobabaCrawler,
    HiddenApiCrawler,
    SeoulYouthCrawler,
)
from .nationwide_crawler import (
    ChungnamYouthCrawler,
    DaejeonYouthCrawler,
    GangwonYouthCrawler,
    GyeongnamYouthCrawler,
    JejuYouthCrawler,
    JeonbukYouthCrawler,
    NationwideRegionalCrawler,
    SejongYouthCrawler,
    UlsanYouthCrawler,
)
from .playwright_crawler import PlaywrightCrawler

__all__ = [
    "BaseCrawler",
    "Bs4Crawler",
    "BusanYouthCrawler",
    "ChungnamYouthCrawler",
    "DaeguYouthCrawler",
    "DaejeonYouthCrawler",
    "GangwonYouthCrawler",
    "GwangjuYouthCrawler",
    "GyeonggiJobabaCrawler",
    "GyeongnamYouthCrawler",
    "HiddenApiCrawler",
    "IncheonYouthCrawler",
    "JejuYouthCrawler",
    "JeonbukYouthCrawler",
    "NationwideRegionalCrawler",
    "PlaywrightCrawler",
    "SejongYouthCrawler",
    "SeoulYouthCrawler",
    "ShHousingCrawler",
    "UlsanYouthCrawler",
]
