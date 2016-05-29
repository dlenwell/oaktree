=======
oaktree
=======

An oaktree is a RESTful place to get shade.

oaktree is a REST interface for interacting with OpenStack clouds that is
inherently interoperable and multi-cloud aware. It is based on the python
shade library, which grew all of the logic needed to interact with OpenStack
clouds and to work around differences in vendor deployment choices. Rather
than keep all of that love in Python Library form, oaktree allows othre
languages to reap the benefits as well.

To play with it, in one terminal run.

.. code-block:: bash

  python oaktree/__init__.py

The swagger docs will be at http://localhost:5000. The API currently takes
a fake auth key which is `deadbeefdeadbeefdeadbeefdeadbeef`. If you want to
do things with it, you can just curl.

.. code-block:: bash

  curl -X GET -H 'Oaktree-API-Key: deadbeefdeadbeefdeadbeefdeadbeef' --header 'Accept: application/json' 'http://localhost:5000/clouds'

* Documentation: http://docs.openstack.org/developer/oaktree
* Source: http://git.openstack.org/cgit/openstack/oaktree
* Bugs: http://bugs.launchpad.net/oaktree
