~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Belfius plugin for ofxstatement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project provides  an `ofxstatement`_ plugin for converting the Belgian Belfius bank's CSV format statements to OFX.

`ofxstatement`_ is a tool to convert proprietary bank statement to OFX format,
suitable for importing to GnuCash. Plugin for ofxstatement parses a
particular proprietary bank statement format and produces common data
structure, that is then formatted into an OFX file.

.. _ofxstatement: https://github.com/kedder/ofxstatement


Users of ofxstatement have developed several plugins for their banks. They are
listed on main `ofxstatement`_ site. If your bank is missing, you can develop
your own plugin.

To convert proprietary ``belfius.csv`` to OFX ``belfius.ofx``, run::

    $ ofxstatement convert -t belfius belfius.csv belfius.ofx

