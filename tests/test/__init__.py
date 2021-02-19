"""Root class for Infotech tests."""
import os
from unittest import TestCase


class TestInfotech(TestCase):
    """Base class for tests."""

    fixtures_path = os.path.join(
      os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
      'fixtures'
    )

    def fixture(self, file_name):
        """Full file name for fixture."""
        return os.path.join(self.fixtures_path, file_name)

    @staticmethod
    def assert_list(data, sample):
        """Assert, that content of two lists is same."""
        assert len(data) == len(sample)
        for item in data:
            assert item in sample

    @staticmethod
    def compare_xml_attrib(section_name, index, data, sample, name):
        """Compare xml attrib value for generated (data) and fixture (sample) item."""
        d_val = data.get(name)
        s_val = sample.get(name)
        assert d_val == s_val, "'{}' item {} {} '{}' must be '{}'".format(section_name, index, name, d_val, s_val)

    @staticmethod
    def compare_xml_attrib_float(section_name, index, data, sample, name, prec):
        """Compare xml attrib value for generated (data) and fixture (sample) item."""
        d_val = data.get(name)
        s_val = sample.get(name)
        assert abs(float(d_val) - float(s_val)) <= (prec * 1.1), "'{}' item {} {} '{}' must be '{}'".format(
          section_name, index, name, d_val, s_val
        )

    def compare_xml_section(
      self, section_name, data_root, sample_root, is_deep=True, is_navigate=False, is_kbd=False
    ):  # pylint: disable=too-many-arguments,too-many-locals
        """Compare generated xml section (data) and fixtures xml section (sample)."""
        d_sect = data_root.find(section_name)
        s_sect = sample_root.find(section_name)
        d_list = list(d_sect)
        s_list = list(s_sect)
        d_len = len(d_list)
        s_len = len(s_list)
        assert d_len == s_len, "'{}' items {} must be {}".format(section_name, d_len, s_len)

        if not is_deep:
            return

        index = 0
        for item in d_list:
            s_item = s_list[index]
            self.compare_xml_attrib(section_name, index, item, s_item, 'ODOMETER')
            self.compare_xml_attrib(section_name, index, item, s_item, 'IDTYPEOBJ')

            if is_navigate:
                self.compare_xml_attrib(section_name, index, item, s_item, 'SRID')
                self.compare_xml_attrib_float(section_name, index, item, s_item, 'L', 0.000001)
                self.compare_xml_attrib_float(section_name, index, item, s_item, 'B', 0.000001)
                self.compare_xml_attrib_float(section_name, index, item, s_item, 'H', 0.00001)

            if is_kbd:
                self.compare_xml_attrib(section_name, index, item, s_item, 'METHOD')
                self.compare_xml_attrib(section_name, index, item, s_item, 'PBEZ')
                self.compare_xml_attrib(section_name, index, item, s_item, 'PBEZ_PERCENT')
                # self.compare_xml_attrib(section_name, index, item, s_item, 'KBD')
                # self.compare_xml_attrib(section_name, index, item, s_item, 'TIME_LIMIT')

            index += 1

    def compare_xml(self, data, sample, is_navigate=False):
        """Compare generated xml (data) and fixtures xml (sample)."""
        fld_root_start = 'INSPECTION_START_DATE'
        fld_root_end = 'INSPECTION_END_DATE'
        fld_root_isp = 'ISP'
        d_root = data.getroot()
        s_root = sample.getroot()
        assert d_root.get(fld_root_start) == d_root.get(fld_root_start)
        assert d_root.get(fld_root_end) == d_root.get(fld_root_end)
        assert d_root.get(fld_root_isp) == d_root.get(fld_root_isp)

        self.compare_xml_section('PIGPASS', d_root, s_root, is_deep=False)
        self.compare_xml_section('WELDS', d_root, s_root, is_navigate=is_navigate)
        self.compare_xml_section('LINEOBJS', d_root, s_root, is_navigate=is_navigate)
        self.compare_xml_section('DEFECTS', d_root, s_root, is_navigate=is_navigate, is_kbd=True)

    @staticmethod
    def dump_xml(xmltree):
        """Debug dump dump_xml(Infotech.xml)."""
        root = xmltree.getroot()
        print("#", root.tag)
        print("#", root.attrib)

        for child in root:
            print(child.tag, child.attrib)
            for item in child:
                print("#", item.tag, item.attrib)
