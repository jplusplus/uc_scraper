
This is a non-official scraper for statistical data from the (https://www.uc.se/konkursstatistik)[uc.se]  built on top of the `Statscraper package <https://github.com/jplusplus/statscraper>`.

The scraper is limited to the data availble through https://www.uc.se/konkursstatistik

Install
-------

.. code:: bash

  $ pip install uc_scraper


Example usage
-------------

.. code:: python

  from uc import UCScraper

  # Init scraper
  scraper = UCScraper()

  # List all available datasets
  print(scraper.items)
  # [<UCDataset: Riks- och länsstatistik (b'Riks- och l\xc3\xa4nsstatistik')>, <UCDataset: Kommunstatistik (b'Kommunstatistik')>, <UCDataset: Branschstatistik (b'Branschstatistik')>]

  # Select a dataset
  dataset = scraper.items["Branschstatistik"]

  # List all available dimensions
  print(dataset.dimensions)
  #

  # Make a query
  res = dataset.fetch()  # Get latest available data by default

  # Analyze the results with Pandas
  df = res.pandas

  # You are able to query month ranges
  res = dataset.fetch({"from": "2019-06"})

  res = dataset.fetch({"from": "2019-06", "to": "2019-07"})


Develop
-------

Set up:

.. code:: bash

  $ pip install -r requirements.txt

Run tests:

.. code:: bash

  $ make tests

Deploy to pypi (assuming you have Twine installed, if not `pip install twine`)

.. code:: bash

  $ make tests
