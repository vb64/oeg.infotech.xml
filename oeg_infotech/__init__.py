# coding: utf-8
"""
Infotech staff
"""
from StringIO import StringIO, StringIO as BytesIO  # pylint: disable=reimported
from .ordered_attrib import ET


class XmlFormat(object):  # pylint: disable=too-few-public-methods
    """
    xml type
    """
    Infotech = 0
    Iust = 1


def reverse_orient(orient):
    """
    reverse orientation
    """
    if not orient:
        return orient

    hours = 12.0 - float(orient.replace(',', '.'))
    if hours == 12.0:
        hours = 0.0

    return "{0:0.1f}".format(hours).replace('.', ',')


def numerate(items, from_index):
    """
    enumerate items from given from_index
    """
    for item in items:
        item.number = "{}".format(from_index)
        from_index += 1


def indent(elem, level=0, ident_item="    "):
    """
    http://effbot.org/zone/element-lib.htm#prettyprint
    in-place prettyprint formatter
    """
    i = "\n" + level*ident_item
    if len(elem):  # pylint: disable=len-as-condition
        if not elem.text or not elem.text.strip():
            elem.text = i + ident_item
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:  # pylint: disable=redefined-argument-from-local
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class Infotech(object):
    """
    Infotech xml export
    """
    typobj_section = 'TYPEOBJS'
    typobj_item = 'TYPEOBJ'
    typobj_id = 'IDTYPEOBJ'
    typobj_title = 'TITLE'

    gps_sys_code = '0'
    gps_sys_name = 'WGS-84'

    template = """<?xml version="1.0" encoding="windows-1251"?>
<IPL_INSPECT>
<TYPEOBJS></TYPEOBJS>
<DEFECTS></DEFECTS>
<LINEOBJS></LINEOBJS>
<WELDS></WELDS>
<PIGPASS></PIGPASS>
</IPL_INSPECT>
"""

    def __init__(self, codepage="windows-1251", xml_format=XmlFormat.Infotech):
        self.xml = ET.parse(StringIO(self.template))
        self.obj_dict = {}
        self.codepage = codepage
        self.xml_format = xml_format
        self.is_navigate = None

        from . import defect, weld, lineobj, pigpass
        self.welds = weld.Section(self)
        self.defects = defect.Section(self)
        self.lineobjects = lineobj.Section(self)
        self.pigpass = pigpass.Section(self)

    def __unicode__(self):
        output = BytesIO()
        self.xml.write(output, encoding=self.codepage)

        return output.getvalue()

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def from_file(cls, file_name, xml_format=XmlFormat.Infotech):
        """
        load data from xml file
        """
        obj = cls(xml_format=xml_format)
        obj.xml = ET.parse(file_name)
        sect = obj.xml.getroot().find(obj.typobj_section)
        obj.obj_dict = {typ.attrib[obj.typobj_id]: typ.find(obj.typobj_title).text for typ in sect}

        return obj

    def rebuild_typeobjs(self):
        """
        generate new content for TYPEOBJS section of xml, based on obj_dict data
        """
        section = self.xml.getroot().find(self.typobj_section)
        section.clear()

        if self.is_navigate:
            node = ET.SubElement(section, self.typobj_item)
            node.set(self.typobj_id, self.gps_sys_code)
            title = ET.SubElement(node, self.typobj_title)
            title.text = self.gps_sys_name

        for key, val in self.obj_dict.items():
            node = ET.SubElement(section, self.typobj_item)
            node.set(self.typobj_id, key)
            title = ET.SubElement(node, self.typobj_title)
            title.text = val

    def total_dist(self):
        """
        return length of inspection
        """
        return self.welds.items[-1].end()

    def start_dist(self):
        """
        return start distance of inspection
        """
        return self.welds.items[0].dist

    def reverse(self):
        """
        reverse vector of objects and return string dump of updated xml
        """
        total_length = self.total_dist()
        self.lineobjects.reverse(total_length)
        self.welds.reverse(total_length)
        self.defects.reverse(total_length)

        return "{}".format(self)

    def fix(self):
        """
        repair umdp-1400 data in PIGPASS section
        """
        umdp = u'УМДП-1400'  # encode(self.codepage)
        umdp_key = None

        for key, val in self.obj_dict.items():
            if val == umdp:
                umdp_key = key
                break

        if not umdp_key:
            return "{}".format(self)

        for pig in self.xml.getroot().find('PIGPASS'):
            if pig.attrib.get('IDTYPEOBJ', None) == umdp_key:
                pig.set('MANUFACT_DATE', '2017')
                pig.set('PIGTYPE', '990004033563')
                pig.set('OBSLTYPE', '2')

        return "{}".format(self)

    def join(self, file_list):
        """
        join several xml files and connect tubes
        """
        from .codes import Tube, NAME
        is_updated = False

        for item in file_list:
            current_length = self.total_dist()
            try:
                self.welds.add_tube(Tube.UNKNOWN, current_length, int(item))
                if Tube.UNKNOWN not in self.obj_dict:
                    self.obj_dict[Tube.UNKNOWN] = NAME[Tube.UNKNOWN]

                is_updated = True

            except ValueError:

                try:
                    info = Infotech.from_file(item)
                except IOError as exc:
                    return str(exc)

                for key in info.obj_dict:
                    if len(key) > 2:
                        if key not in self.obj_dict:
                            self.obj_dict[key] = info.obj_dict[key]

                start = info.start_dist()

                self.welds.add_from_xml(info.welds, current_length, start)
                self.defects.add_from_xml(info.defects, current_length, start)
                self.lineobjects.add_from_xml(info.lineobjects, current_length, start)

                is_updated = True

        if is_updated:
            numerate(self.welds.items, 1)
            numerate(self.defects.items, 1)

            self.rebuild_typeobjs()
            self.welds.rebuild_xml()
            self.defects.rebuild_xml()
            self.lineobjects.rebuild_xml()

        indent(self.xml.getroot(), level=0)

        return "{}".format(self)
