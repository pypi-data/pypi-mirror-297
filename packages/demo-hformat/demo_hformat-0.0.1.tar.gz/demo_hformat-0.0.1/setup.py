from setuptools import setup, find_packages

setup(
    name="demo-hformat",
    version="0.0.1",
    description="Reformats files to stdout",
    install_requires = ["click", "colorama", "pandas"],
    entry_points="""
    [console_scripts]
    hformat=hformat.main:main
    """,
    author="Herve Habonimana",
    author_email="habonimanah@gmail.com",
    packages=find_packages(),
)
