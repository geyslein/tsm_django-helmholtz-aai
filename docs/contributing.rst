.. _contributing:

Contribution and development hints
==================================
The django-helmholtz-aai project is developed by the
`Helmholtz Coastal Data Center (HCDC)`_ of the `Helmholtz-Zentrum Hereon`_. It
is open-source as we believe that this package can be helpful for multiple
other django applications, and we are looking forward for your feedback,
questions and especially for your contributions.

- If you want to ask a question, are missing a feature or have comments on the
  docs, please `open an issue at the source code repository`_
- If you have suggestions for improvement, please let us know in an issue, or
  fork the repository and create a merge request. See also :ref:`development`.

.. _Helmholtz Coastal Data Center (HCDC): https://hcdc.hereon.de
.. _Helmholtz-Zentrum Hereon: https://www.hereon.de
.. _open an issue at the source code repository: https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai/issues/new/

.. _development:

Contributing in the development
-------------------------------
Thanks for your wish to contribute to this app!! The source code of the
django-helmholtz-aai package is hosted at
https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai. It's an open gitlab
where you can register via GitHub, or via the Helmholtz AAI. Once you created
an account, you can fork_ this repository to your own user account and
implement the changes. Afterwards, please make a merge request into the main
repository. If you have any questions, please do not hesitate to create an
issue on gitlab and contact the developers.

Once you created you fork, you can clone it via

.. code-block:: bash

    git clone https://gitlab.hzdr.de/<your-user>/django-helmholtz-aai.git

and install it in development mode with the `[dev]` option via::

    pip install -e ./django-helmholtz-aai/[dev]

Once you installed the package, run the migrations::

    cd django-helmholtz-aai/
    python manage.py migrate

which will create an sqlite-database for you.

Fixing the docs
^^^^^^^^^^^^^^^
The documentation for this package is written in restructured Text and built
with sphinx_ and deployed on readthedocs_.

If you found something in the docs that you want to fix, head over to the
``docs`` folder and build the docs with `make html` (or `make.bat` on windows).
The docs are then available in ``docs/_build/html/index.html`` that you can
open with your local browser.

Implement your fixes in the corresponding ``.rst``-file and push them to your
fork on gitlab.

Contributing to the code
^^^^^^^^^^^^^^^^^^^^^^^^
We use automated formatters (see their config in ``pyproject.toml`` and
``setup.cfg``), namely

-  `Black <https://black.readthedocs.io/en/stable/>`__ for standardized
   code formatting
-  `blackdoc <https://blackdoc.readthedocs.io/en/stable/>`__ for
   standardized code formatting in documentation
-  `Flake8 <http://flake8.pycqa.org/en/latest/>`__ for general code
   quality
-  `isort <https://github.com/PyCQA/isort>`__ for standardized order in
   imports.
-  `mypy <http://mypy-lang.org/>`__ for static type checking on
   `type hints <https://docs.python.org/3/library/typing.html>`__

We highly recommend that you setup
`pre-commit hooks <https://pre-commit.com/>`__ to automatically run all the
above tools every time you make a git commit. This can be done by running::

   pre-commit install

from the root of the repository. You can skip the pre-commit checks with
``git commit --no-verify`` but note that the CI will fail if it
encounters any formatting errors.

You can also run the pre-commit step manually by invoking::

   pre-commit run --all-files


.. _fork: https://gitlab.hzdr.de/hcdc/django/django-helmholtz-aai/-/forks/new

.. _sphinx: https://www.sphinx-doc.org
.. _readthedocs: https://readthedocs.org
