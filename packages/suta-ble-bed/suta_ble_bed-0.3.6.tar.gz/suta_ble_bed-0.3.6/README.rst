============
SUTA BLE Bed
============


.. image:: https://img.shields.io/pypi/v/suta_ble_bed.svg
        :target: https://pypi.python.org/pypi/suta_ble_bed

.. image:: https://img.shields.io/travis/sredman/suta_ble_bed.svg
        :target: https://travis-ci.com/sredman/suta_ble_bed

.. image:: https://readthedocs.org/projects/suta-ble-bed/badge/?version=latest
        :target: https://suta-ble-bed.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/sredman/suta_ble_bed/shield.svg
     :target: https://pyup.io/repos/github/sredman/suta_ble_bed/
     :alt: Updates

BLE handling code for bed frames which use the SUTA app,
such as the such as the i500 or i800 (and others)

Supports control of the bed but not access to the current state.
Expected to be used as a module to build your own integration with some
control system, but ships with a rough CLI to play with directly.

Does device discovery by name because (as far as I could tell) the bed
does not support discovery by the typical manufacturer UUID.

Notionally, this should be fine unless your neighbor is actively trying
to intercept your bed control.


* Free software: MIT license
* Documentation: https://suta-ble-bed.readthedocs.io.


Features
--------

* TODO

Usage
--------

.. code-block:: python

    async with SutaBleBedController() as controller:
      async for bed in controller.devices():
        await bed.raise_feet()
        break

Note that the `async for` will return a result each time the advertising data changes,
which includes any time the signal strength changes.

or

.. code-block:: sh

   python -m suta_ble_bed --MAC=AA:BB:CC:DD:EE:FF head-down

Release Process
---------------

To tag and release the latest code:

.. code-block:: sh

   # Write release notes
   vim HISTORY.rst
   git add HISTORY.rst
   git commit -m "Release notes for vx.y.z"
   # Bump
   bump2version [patch,minor,major]
   # Assuming no errors ...
   git push --tags

Go to this repository in Github, make a new release using the UI.

The Github Action should then take care of publishing the release on Pypi.

Credits
-------

This module would not have been possible without the research done by stevendodd on Github:
https://github.com/stevendodd/sleepmotion-ble/blob/main/pi-zero/sleepmotion-ble.py

Inspired by:
https://github.com/sopelj/python-ember-mug/blob/main/ember_mug/mug.py

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
