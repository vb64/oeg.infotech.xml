# coding: utf-8
"""
make test T=test_commands
"""
from . import TestInfotech


class TestCommands(TestInfotech):
    """
    commands for xml export file
    """
    def test_join(self):
        """
        join
        """
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('1736.xml'))
        dist1 = info.total_dist()
        welds1 = len(info.welds.items)
        defects1 = len(info.defects.items)
        lineobjects1 = len(info.lineobjects.items)

        self.assertEqual(dist1, 17727)
        self.assertEqual(welds1, 23)
        self.assertEqual(defects1, 10)
        self.assertEqual(lineobjects1, 6)

        info = Infotech.from_file(self.fixture('1737.xml'))

        dist2 = info.total_dist()
        welds2 = len(info.welds.items)
        defects2 = len(info.defects.items)
        lineobjects2 = len(info.lineobjects.items)

        self.assertEqual(dist2, 5589)
        self.assertEqual(welds2, 5)
        self.assertEqual(defects2, 2)
        self.assertEqual(lineobjects2, 4)

        text = info.join(['1100', self.fixture('1736.xml')])

        self.assertIn('IPL_INSPECT', text)
        self.assertEqual(info.total_dist(), dist1 + dist2 + 1100)
        self.assertEqual(len(info.welds.items), welds1 + welds2 + 1)
        self.assertEqual(len(info.defects.items), defects1 + defects2)
        self.assertEqual(len(info.lineobjects.items), lineobjects1 + lineobjects2)

        text = info.join([])
        self.assertIn('IPL_INSPECT', text)

        text = info.join(['not_exist_file'])
        self.assertIn('No such file or directory', text)

    def test_reverse(self):
        """
        reverse
        """
        from oeg_infotech import Infotech, lineobj, codes
        from oeg_infotech.base import DistItem

        info = Infotech.from_file(self.fixture('1736.xml'))
        self.assertEqual(info.total_dist(), 17727)
        root = info.xml.getroot()
        l_section = root.find(lineobj.Section.section_tag)
        self.assertEqual(int(l_section[0].get(DistItem.field_odometer)), 0)
        self.assertEqual(int(l_section[-1].get(DistItem.field_odometer)), 17710)

        self.assertEqual(l_section[1].get(DistItem.field_typeobj), codes.Feature.CASE_START)
        self.assertEqual(l_section[2].get(DistItem.field_typeobj), codes.Feature.CASE_END)

        text = info.reverse()

        self.assertIn('IPL_INSPECT', text)

        self.assertNotEqual(l_section[1].get(DistItem.field_typeobj), codes.Feature.CASE_START)
        self.assertNotEqual(l_section[2].get(DistItem.field_typeobj), codes.Feature.CASE_END)
        self.assertEqual(l_section[-2].get(DistItem.field_typeobj), codes.Feature.CASE_END)
        self.assertEqual(l_section[-3].get(DistItem.field_typeobj), codes.Feature.CASE_START)

        self.assertEqual(int(l_section[0].get(DistItem.field_odometer)), 17)
        self.assertEqual(int(l_section[-1].get(DistItem.field_odometer)), 17727)

    def test_fix(self):
        """
        repair
        """
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('umdp-1400.xml'))
        pig = info.xml.getroot().find('PIGPASS')[1]

        self.assertEqual(info.obj_dict['1'], u'УМДП-1400')
        self.assertEqual(pig.attrib.get('IDTYPEOBJ', None), '1')
        self.assertEqual(pig.attrib.get('MANUFACT_DATE', None), '')
        self.assertEqual(pig.attrib.get('PIGTYPE', None), '2')
        self.assertEqual(pig.attrib.get('OBSLTYPE', None), '5')

        info.fix()

        pig = info.xml.getroot().find('PIGPASS')[1]
        self.assertEqual(pig.attrib.get('IDTYPEOBJ', None), '1')
        self.assertEqual(pig.attrib.get('MANUFACT_DATE', None), '2017')
        self.assertEqual(pig.attrib.get('PIGTYPE', None), '990004033563')
        self.assertEqual(pig.attrib.get('OBSLTYPE', None), '2')
