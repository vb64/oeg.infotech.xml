"""
PIGPASS section
"""
from .ordered_attrib import ET
from .codes import PassType
from .base import Section as InfotechSection, AbstractItem
from . import XmlFormat


class Item(AbstractItem):
    """
    object item from <PIGPASS> xml section
    <PASS
      IDTYPEOBJ="0" DATE1="25.05.2018 10:58:00" DATE2="25.05.2018 11:10:00"
      SPEED_AVERAGE="0.26" REM="" MANUFACTURER="xxxx" MANUFACT_DATE="2010"
      PIGTYPE="990005096296" OBSLTYPE="2"
    />
    """
    xml_node_name = 'PASS'

    field_typeobj = 'IDTYPEOBJ'
    field_date1 = 'DATE1'
    field_date2 = 'DATE2'
    field_speed = 'SPEED_AVERAGE'
    field_rem = 'REM'
    field_manufacturer = 'MANUFACTURER'
    field_manufac_date = 'MANUFACT_DATE'
    field_pigtype = 'PIGTYPE'
    field_insptype = 'OBSLTYPE'

    # IUST fields
    field_iust_type = 'IUST_TYPE'

    def __init__(self, xml_format=XmlFormat.Infotech):
        self.xml_format = xml_format
        self.pig = None
        self.objtype = None
        self.date1 = None
        self.date2 = None
        self.speed = None
        self.rem = None
        self.manufacturer = None
        self.manufac_date = None
        self.pigtype = None
        self.insptype = None

        self.iust_type = None

    @classmethod
    def from_xml(cls, xml_item, xml_format=XmlFormat.Infotech):
        """
        create item from xml item
        """
        obj = cls(xml_format=xml_format)

        obj.objtype = xml_item.attrib[Item.field_typeobj]
        obj.date1 = xml_item.attrib[Item.field_date1]
        obj.date2 = xml_item.attrib[Item.field_date2]
        obj.speed = xml_item.attrib[Item.field_speed]
        obj.rem = xml_item.attrib[Item.field_rem]
        obj.manufacturer = xml_item.attrib[Item.field_manufacturer]
        obj.manufac_date = xml_item.attrib[Item.field_manufac_date]
        obj.pigtype = xml_item.attrib[Item.field_pigtype]
        obj.insptype = xml_item.attrib[Item.field_insptype]

        if obj.xml_format == XmlFormat.Iust:
            obj.iust_type = xml_item.attrib[Item.field_iust_type]

        return obj

    def add_xml_child(self, parent_node):
        """
        create and add pigpass xml node of object to parent xml node
        """
        node = ET.SubElement(parent_node, Item.xml_node_name)

        node.set(Item.field_typeobj, self.objtype)
        node.set(Item.field_date1, self.date1)
        node.set(Item.field_date2, self.date2)
        node.set(Item.field_speed, self.speed)
        node.set(Item.field_rem, self.rem)
        node.set(Item.field_manufacturer, self.manufacturer)
        node.set(Item.field_manufac_date, self.manufac_date)
        node.set(Item.field_pigtype, self.pigtype)

        if self.xml_format == XmlFormat.Iust:
            node.set(Item.field_iust_type, self.iust_type)

        node.set(Item.field_insptype, self.insptype)

        return node


class Section(InfotechSection):
    """
    <PIGPASS> xml section
    """
    section_tag = 'PIGPASS'
    item_attributes = [
      Item.field_typeobj,
      Item.field_date1,
      Item.field_date2,
      Item.field_speed,
      Item.field_rem,
      Item.field_manufacturer,
      Item.field_manufac_date,
      Item.field_pigtype,
      Item.field_insptype,
    ]

    def __init__(self, infotech):
        super(Section, self).__init__(infotech, Item, Section.section_tag)

    def is_navigate(self):
        """
        is navigate data present
        """
        if not self._items:
            return False

        for pigpass in self._items:
            if pigpass.insptype in [PassType.NAVIGATE, PassType.COMPLEX_NAV]:
                return True

        return False
