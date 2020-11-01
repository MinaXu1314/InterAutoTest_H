import os
import pytest
from config import Conf


if __name__ == '__main__':
    report_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    pytest.main(["-s", "--alluredir", report_path])