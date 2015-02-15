===============================
rackcli
===============================

.. image:: https://badge.fury.io/py/rackcli.png
    :target: http://badge.fury.io/py/rackcli

.. image:: https://travis-ci.org/jnoller/rackcli.png?branch=master
        :target: https://travis-ci.org/jnoller/rackcli

.. image:: https://pypip.in/d/rackcli/badge.png
        :target: https://pypi.python.org/pypi/rackcli


Description
-----------

"rackcli" is a minimalistic cli for the Rackspace cloud based on
`python-openstacksdk`_ & the `rackspace-sdk-plugin`_. It is not meant to replace
any other power tools (such as `supernova`_, or `python-openstackclient`_) but
rather to be an opinionated end-user-only tool to provide a quick and seamless
user experience to accessing the Rackspace Cloud.

For example - it uses the "end user" names for services - such as "servers" vs
"nova" and "files" vs "swift".

It is also very alpha. Only good for hacking on right now.

* Free software: Apache 2.0
* Documentation: https://rackcli.readthedocs.org.

Features
--------

* It's a platypus; it doesn't do much right now



.. image:: http://weknowgifs.com/wp-content/uploads/2013/11/i-have-no-idea-what-im-doing-dog-gif.gif



.. _python-openstacksdk: https://github.com/stackforge/python-openstacksdk
.. _rackspace-sdk-plugin: https://github.com/rackerlabs/rackspace-sdk-plugin
.. _python-openstackclient: https://github.com/openstack/python-openstackclient
.. _supernova: https://github.com/major/supernova/
