"""
make test T=test_inspection.py
"""
from . import TestInfotech


class TestInspection(TestInfotech):
    """
    inspection
    """
    def test_from_file(self):
        """
        inspection from xml
        """
        from oeg_infotech import Infotech
        from oeg_infotech.codes import PigType

        info = Infotech.from_file(self.fixture('1736.xml'))
        assert len(info.pigpass.items) == 2

        types = [pigpass.pigtype for pigpass in info.pigpass.items]
        assert PigType.MFL in types
        assert PigType.TFI in types
        assert PigType.CALIPER_MECH not in types
        assert len(info.welds.items) == 23

        assert not info.pigpass.is_navigate()

    def test_navigate(self):
        """
        inspection with navigate data
        """
        from oeg_infotech import Infotech
        from oeg_infotech.codes import PassType

        info = Infotech.from_file(self.fixture('1827.xml'))
        self.compare_xml(
          info.xml,
          Infotech.from_file(self.fixture('1827.xml')).xml,
          is_navigate=info.is_navigate
        )

        assert not info.pigpass.is_navigate()
        info.pigpass.items[0].insptype = PassType.NAVIGATE
        assert info.pigpass.is_navigate()
