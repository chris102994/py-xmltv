<!-- Links -->
[py-xmltv]: (https://github.com/chris102994/py-xmltv)
[Jing-Trang]: (https://github.com/relaxng/jing-trang)
[xsData]: (https://github.com/tefra/xsdata)

# [py-xmltv]

This is a simple project to turn the official XMLTV DTD/XSDs into proper serialized Python Data classes for easy writing/reading.

This is accomplished by using the [Jing-Trang] project to transform the supplied DTD into a valid XML. Once there's a valid XSD corresponding Python data classes are generated using the [xsData] project.

[![Build Status](https://travis-ci.com/chris102994/py-xmltv.svg?branch=master)](https://travis-ci.com/github/chris102994/py-xmltv)
[![PyPi Link](https://img.shields.io/pypi/status/py-xmltv?label=PyPi)](https://pypi.org/project/py-xmltv/)