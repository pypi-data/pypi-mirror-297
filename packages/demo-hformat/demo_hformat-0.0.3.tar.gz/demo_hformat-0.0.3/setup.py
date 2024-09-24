from setuptools import setup, find_packages

setup(
    name="demo-hformat",
    version="0.0.3",
    description="Reformats files to stdout",
    install_requires = ["click", "pandas"],
    entry_points="""
    [console_scripts]
    hformat=hformat.main:main
    """,
    author="Herve Habonimana",
    author_email="habonimanah@gmail.com",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
