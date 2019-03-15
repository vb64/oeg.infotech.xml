"""
make test T=test_inspection
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
        self.assertEqual(len(info.pigpass.items), 2)

        types = [pigpass.pigtype for pigpass in info.pigpass.items]
        self.assertIn(PigType.MFL, types)
        self.assertIn(PigType.TFI, types)
        self.assertNotIn(PigType.CALIPER_MECH, types)
        self.assertEqual(len(info.welds.items), 23)

    def test_navigate(self):
        """
        inspection with navigate data
        """
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('1736.xml'))
        self.compare_xml(info.xml, Infotech.from_file(self.fixture('1736.xml')).xml, is_navigate=info.is_navigate)
