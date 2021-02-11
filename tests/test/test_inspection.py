"""
make test T=test_inspection.py
"""
from . import TestInfotech


class TestInspection(TestInfotech):
    """Check inspection xml."""

    def test_ordered_attributes(self):
        """Test attributes order in generated xml."""
        from oeg_infotech import Infotech

        fname = self.fixture('1736.xml')
        title_line = open(fname).readlines()[1]
        assert 'IPL_INSPECT' in title_line

        info = Infotech.from_file(fname)
        root = info.xml.getroot()

        try:
            root.ordered_attributes = [
              'NLCH', 'PLACE', 'L1', 'KZ_TYPE', 'L2', 'KP_TYPE', 'ISP',
              'INSPECTION_START_DATE', 'INSPECTION_END_DATE',
            ]
        except AttributeError:
            pass  # Python3

        assert title_line in info.reverse(), "Wrong attribute order in IPL_INSPECT"

    def test_from_file(self):
        """Inspection from xml."""
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
        try:
            text = info.__unicode__()
        except TypeError:
            text = True  # Python 3
        assert text

    def test_navigate(self):
        """Inspection with navigate data."""
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
        assert info.welds.as_csv(with_navigation=True)

        assert not info.is_navigate
        info.is_navigate = True
        info.rebuild_typeobjs()
        assert info.is_navigate
