from setuptools import setup, Extension
from Cython.Build import cythonize

# 定义需要编译的扩展模块
extensions = [
    Extension("litequant.LSClient", ["litequant/LSClient.py"]),  # 编译 LSClient.py
    Extension("litequant.ParquetManager", ["litequant/ParquetManager.py"]),  # 编译 ParquetManager.py
]
setup(
    name='litequant',
    version='0.1.1',
    ext_modules=cythonize(extensions, exclude=["litequant/__init__.py"]),

    packages=['litequant'],
    # ext_modules=cythonize(extensions),  # 使用cythonize编译模块
    install_requires=[
        'requests',
        'pandas',
        'redis',
        'tqdm',
    ],
    author='Danene Tech Inc.',
    author_email='neneli@bignene123.com',
    description='Data API for Quantitative Analysts.',
    license='CC BY-NC',
    keywords='Data API for Quants',
)
