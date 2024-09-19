from setuptools import setup, find_packages

setup(
    name='blum_rendy',  # Nama paket Anda
    version='0.1',
    description='Deskripsi singkat paket',
    author='Rendy',
    author_email='email@domain.com',
    packages=find_packages(),  # Akan mencari semua modul di dalam folder proyek
    install_requires=[
        # Daftar dependensi yang diperlukan paket Anda
        # 'some_package>=1.0.0',
    ],
)
