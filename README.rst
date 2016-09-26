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

oaktree is not a replacement for all of the individual project REST APIs.
Those are all essential for cross-project communication and are well suited
for operators who can be expected to know things about how they have
deployed their clouds - and who in fact WANT to be able to make changes in
the cloud knowing deployment specifics. oaktree will never be for them.

oaktree is for end-users who do not and should not know what hypervisor, what
storage driver or what network stack the deployer has chosen. The two sets
of people are different audiences, so oaktree is a project to support the
end user.

Using
-----

To play with it, in one terminal run.

.. code-block:: bash

  python oaktree/__init__.py

The swagger docs will be at http://localhost:5000. The API currently takes
a fake auth key which is `deadbeefdeadbeefdeadbeefdeadbeef`. If you want to
do things with it, you can just curl.

.. code-block:: bash

  curl -X GET -H 'Oaktree-API-Key: deadbeefdeadbeefdeadbeefdeadbeef' --header 'Accept: application/json' 'http://localhost:5000/clouds'

If you want to try the gRPC version
-----------------------------------

In one window:

.. code-block:: bash

  python oaktree/rpc/server.py

In another window:

.. code-block:: bash

  python -i mt.py

You'll have a flavors object you can poke at.

Shape of the Project
--------------------

oaktree should be super simple to deploy, and completely safe for deployers
to upgrade from master constantly. Once it's released as a 1.0, it should
NEVER EVER EVER EVER EVER EVER EVER have a backwards incompatible change.
There is no reason, no justification, no obessession important enough to
inflict such pain on the user.

In addition to a REST api - oaktree will also have a websockets API that will
allow for active notification instead of polling. The shape of that has not
yet been designed.

The shade library will grow the ability to detect if a cloud has an oaktree
api available, and if it does, it will use it. Hopefully we'll quickly reach
a point where all deployers are deploying oaktree.

* Documentation: http://docs.openstack.org/developer/oaktree
* Source: http://git.openstack.org/cgit/openstack/oaktree
* Bugs: http://bugs.launchpad.net/oaktree
