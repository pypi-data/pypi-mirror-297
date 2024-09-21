from setuptools import Extension, setup

setup(
    name='zcurvepy',
    version='1.2.0',
    install_requires=['matplotlib', 'scipy', 'scikit-learn', 'biopython'],
    python_requires='>=3',
    ext_modules=[Extension("zcurvepy", ["zcurvepy.cpp"])]
)
