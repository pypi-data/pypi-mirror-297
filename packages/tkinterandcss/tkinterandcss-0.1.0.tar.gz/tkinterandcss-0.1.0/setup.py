from setuptools import setup, find_packages

setup(
    name='tkinterandcss',
    version='0.1.0',
    author='Bobby',
    author_email='akirasumeragi699@gmail.com',
    description='Thư viện để áp dụng CSS cho widget Tkinter.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hqmdokkai/tkinterandcss',  # Thay đổi thành URL của bạn
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "tkinter" ,
    ],
)
