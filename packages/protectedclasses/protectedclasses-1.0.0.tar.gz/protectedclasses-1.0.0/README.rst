================
protectedclasses
================

Overview
--------

Use the class ``Protected`` as a parent.

Installation
------------

To install ``protectedclasses``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install protectedclasses

Implementation
--------------

.. code-block:: python

    class Protected:
        def __setattr__(self, name, value):
            cls = type(self)
            if name.startswith("_"):
                super().__setattr__(name, value)
                return
            if isinstance(getattr(cls, name, None), property):
                super().__setattr__(name, value)
                return
            e = "%r object has no property %r"
            e %= (cls.__name__, name)
            raise AttributeError(e)

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/protectedclasses>`_
* `Download <https://pypi.org/project/protectedclasses/#files>`_
* `Source <https://github.com/johannes-programming/protectedclasses>`_

Credits
-------

* Author: Johannes
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``protectedclasses``!