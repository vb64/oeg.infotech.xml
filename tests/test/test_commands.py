# coding: utf-8
"""
make test T=test_commands
"""
from . import TestInfotech


class TestCommands(TestInfotech):
    """Commands for xml export file."""

    def test_join(self):
        """Join command."""
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('1736.xml'))
        dist1 = info.total_dist()
        welds1 = len(info.welds.items)
        defects1 = len(info.defects.items)
        lineobjects1 = len(info.lineobjects.items)

        assert dist1 == 17727
        assert welds1 == 23
        assert defects1 == 10
        assert lineobjects1 == 6

        info = Infotech.from_file(self.fixture('1737.xml'))

        dist2 = info.total_dist()
        welds2 = len(info.welds.items)
        defects2 = len(info.defects.items)
        lineobjects2 = len(info.lineobjects.items)

        assert dist2 == 5589
        assert welds2 == 5
        assert defects2 == 2
        assert lineobjects2 == 4

        text = info.join(['1100', self.fixture('1736.xml')])

        assert 'IPL_INSPECT' in text
        assert info.total_dist() == dist1 + dist2 + 1100
        assert len(info.welds.items) == welds1 + welds2 + 1
        assert len(info.defects.items) == defects1 + defects2
        assert len(info.lineobjects.items) == lineobjects1 + lineobjects2

        text = info.join([])
        assert 'IPL_INSPECT' in text

        text = info.join(['not_exist_file'])
        assert 'No such file or directory' in text

    def test_reverse(self):
        """Reverse command."""
        from oeg_infotech import Infotech, lineobj, codes
        from oeg_infotech.base import DistItem

        info = Infotech.from_file(self.fixture('1736.xml'))
        assert info.total_dist() == 17727
        root = info.xml.getroot()
        l_section = root.find(lineobj.Section.tag)
        assert int(l_section[0].get(DistItem.field_odometer)) == 0
        assert int(l_section[-1].get(DistItem.field_odometer)) == 17710

        assert l_section[1].get(DistItem.field_typeobj) == codes.Feature.CASE_START
        assert l_section[2].get(DistItem.field_typeobj) == codes.Feature.CASE_END

        text = info.reverse()

        assert 'IPL_INSPECT' in text

        assert l_section[1].get(DistItem.field_typeobj) != codes.Feature.CASE_START
        assert l_section[2].get(DistItem.field_typeobj) != codes.Feature.CASE_END
        assert l_section[-2].get(DistItem.field_typeobj) == codes.Feature.CASE_END
        assert l_section[-3].get(DistItem.field_typeobj) == codes.Feature.CASE_START

        assert int(l_section[0].get(DistItem.field_odometer)) == 17
        assert int(l_section[-1].get(DistItem.field_odometer)) == 17727

    def test_fix(self):
        """Repair command."""
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('umdp-1400.xml'))
        pig = info.xml.getroot().find('PIGPASS')[1]

        assert info.obj_dict['1'] == u'УМДП-1400'
        assert pig.attrib.get('IDTYPEOBJ', None) == '1'
        assert pig.attrib.get('MANUFACT_DATE', None) == ''
        assert pig.attrib.get('PIGTYPE', None) == '2'
        assert pig.attrib.get('OBSLTYPE', None) == '5'

        info.fix()

        pig = info.xml.getroot().find('PIGPASS')[1]
        assert pig.attrib.get('IDTYPEOBJ', None) == '1'
        assert pig.attrib.get('MANUFACT_DATE', None) == '2017'
        assert pig.attrib.get('PIGTYPE', None) == '990004033563'
        assert pig.attrib.get('OBSLTYPE', None) == '2'

        info = Infotech.from_file(self.fixture('empty.xml'))
        info.fix()
