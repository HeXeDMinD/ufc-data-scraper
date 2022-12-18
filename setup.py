import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ufc_data_scraper",
    version="0.9.5",
    author="Kyle Leben",
    author_email="leben.kyle.hex@gmail.com",
    description="A simple webscraping library, focused on the UFC website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/HeXeDMinD/ufc-data-scraper",
    project_urls={
        "Bug Tracker": "https://gitlab.com/HeXeDMinD/ufc-data-scraper/issues"
    },
    license="MIT",
    packages=[
        "ufc_data_scraper",
        "ufc_data_scraper.models",
        "ufc_data_scraper.scraper",
    ],
    install_requires=["requests", "bs4", "pytz", "unidecode"],
)
