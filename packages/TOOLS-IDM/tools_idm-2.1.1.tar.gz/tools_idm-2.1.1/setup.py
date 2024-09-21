from setuptools import setup, find_packages

setup(
    name='TOOLS-IDM',
    version='2.1.1',
    packages=find_packages(),
    install_requires=[
        'aiohttp',  # Tambahkan dependencies Anda di sini
        # 'nama_paket_lain',  # Tambahkan paket lain jika diperlukan
    ],
    entry_points={
        'console_scripts': [
            'ess=ess.ess:main',
        ],
    },
    description='Script ESS:)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nama Anda',
    author_email='email@domain.com',
    url='https://github.com/username/repo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)