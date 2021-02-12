"""
make test T=test_readme.py
"""
from . import TestInfotech


class TestReadme(TestInfotech):
    """Check readme.md code."""

    def test_readme(self):
        """Readme.md example code."""

        from oeg_infotech import Infotech, XmlFormat

        iust = self.fixture('iust.xml')
        itech = self.fixture('1736.xml')

        info = Infotech.from_file(iust, xml_format=XmlFormat.Iust)
        assert 'IUST_TYPE' in str(info)

        info1 = Infotech.from_file(itech)
        assert 'IPL_INSPECT' in str(info1)

        xml_string = info1.reverse()
        assert 'IPL_INSPECT' in xml_string

        xml_string = info1.join(['1100', itech])
        assert 'IPL_INSPECT' in xml_string
