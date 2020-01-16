"""
make test T=test_init.py
"""
from . import TestInfotech


class TestInit(TestInfotech):
    """
    Infotech core function
    """
    @staticmethod
    def test_reverse_orient():
        """
        reverse_orient
        """
        from oeg_infotech import reverse_orient

        assert reverse_orient('') == ''
        assert reverse_orient('0') == '0,0'
        assert reverse_orient('6.0') == '6,0'
        assert reverse_orient('3.0') == '9,0'
        assert reverse_orient('3.5') == '8,5'
        assert reverse_orient('9.0') == '3,0'
        assert reverse_orient('9.5') == '2,5'

    def test_infotech(self):
        """
        package
        """
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('1736.xml'))
        assert info.total_dist() == 17727

        assert len(info.obj_dict) == 15
        assert len(info.defects.items) == 10
        assert len(info.lineobjects.items) == 6
        assert len(info.welds.items) == 23
        # cached access
        assert len(info.defects.items) == 10
        assert len(info.lineobjects.items) == 6

        assert 'IPL_INSPECT' in "{}".format(info)
        assert info.defects.as_csv()

    def test_navigation(self):
        """
        navigation
        """
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('navigation.xml'))
        assert 'IPL_INSPECT' in info.reverse()

    def test_iust(self):
        """
        iust format
        """
        from oeg_infotech import Infotech, XmlFormat

        info = Infotech.from_file(self.fixture('1736.xml'), xml_format=XmlFormat.Iust)
        xml = info.reverse()

        assert 'IUST_TYPE' in xml
        assert 'IUST_GEO' in xml
        assert 'IUST_FROM_WELD' in xml
