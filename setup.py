import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ufc_data_scraper",
    version="0.9.87",
    author="Kyle Leben",
    author_email="leben.kyle.hex@gmail.com",
    description="A simple webscraping library, focused on the UFC website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HeXeDMinD/ufc-data-scraper",
    project_urls={
        "Bug Tracker": "https://github.com/HeXeDMinD/ufc-data-scraper/issues"
    },
    license="MIT",
    packages=[
        "ufc_data_scraper",
        "ufc_data_scraper.data_models",
        "ufc_data_scraper.data_models.event",
        "ufc_data_scraper.data_models.fighter",
        "ufc_data_scraper.scraper",
        "ufc_data_scraper.utils",
    ],
    install_requires=["requests", "bs4", "pytz", "unidecode"],
)
