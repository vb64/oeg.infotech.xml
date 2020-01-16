# oeg.infotech.xml

[![Python 2.7](https://img.shields.io/travis/vb64/oeg.infotech.xml.svg?label=Python%202.7&style=plastic)](https://travis-ci.org/vb64/oeg.infotech.xml)
[![Code Climate](https://img.shields.io/codeclimate/maintainability-percentage/vb64/oeg.infotech.xml.svg?label=Code%20Climate&style=plastic)](https://codeclimate.com/github/vb64/oeg.infotech.xml)
[![Coverage Status](https://coveralls.io/repos/github/vb64/oeg.infotech.xml/badge.svg?branch=master)](https://coveralls.io/github/vb64/oeg.infotech.xml?branch=master)

Библиотека Python для обработки xml файлов "Инфотех" с поддержкой дополнительных полей, требуемых для загрузки в "ИУС Т".

## Установка

```
$ pip install oeg-infotech
```

## Использование

```python

from oeg_infotech import Infotech, XmlFormat

# загрузить файл в формате "ИУС Т"
info = Infotech.from_file('iust.xml', xml_format=XmlFormat.Iust)
'IUST_TYPE' in str(info)
True

# загрузить файл в формате "Инфотех"
info1 = Infotech.from_file('infotech1.xml')
'IPL_INSPECT' in str(info1)
True

# перевернуть данные, пересчитав дистанции и ориентаци. обьектов
xml_string = info1.reverse()
'IPL_INSPECT' in xml_string
True

# обьединить перевернутые данные из infotech1.xml и данные из infotech2.xml, вставив между ними трубу длиной 11 метров
xml_string = info1.join(['1100', 'infotech2.xml'])
'IPL_INSPECT' in xml_string
True

```

## Разработка

```
$ git clone git@github.com:vb64/oeg.infotech.xml.git
$ cd oeg.infotech.xml
$ make setup PYTHON_BIN=/path/to/python27/executable
$ make tests
```
