putio.py
========

Simple wrapper for `Put.io API v2 <https://api.put.io/v2/docs>`_.


Installing
----------

putio.py is available on PyPI.

.. code-block:: bash

    $ pip install putio.py


Usage
-----

.. code-block:: python

    import putio

    helper = putio.AuthHelper(CLIENT_ID, CLIENT_SECRET, \
                              CALLBACK_URL, type='token')

    # this will open a browser to authetication url
    # after authenticating you will find the oauth_token in the address bar
    helper.open_authentication_url()

    client = putio.Client(OAUTH_TOKEN)

    # list files
    files = client.File.list()

    # add a new transfer
    client.Transfer.add_url('http://example.com/good.torrent')

    # read the code for other methods.
