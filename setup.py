from setuptools import setup, find_packages

setup(
    name='rubberband',
    version='0.1',
    packages=find_packages(),
    py_modules=["run_tool"],
    install_requires=[
        'click',
        'pyyaml',
        'snakemake'
    ],
    entry_points={
        'console_scripts': [
            'rubberband=run_tool:main'
        ]
    }
)