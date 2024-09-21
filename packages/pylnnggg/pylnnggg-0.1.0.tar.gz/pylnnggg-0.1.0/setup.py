from setuptools import setup, find_packages

setup(
    name='pylnnggg',  # Nama paket harus ditulis dengan huruf kecil
    version='0.1.0',  # Versi paket
    author='LaangYB',  # Nama Anda
    author_email='sedekgaming123@gmail.com',  # Email Anda
    description='Bot ini dibuat untuk to the point aja',  # Deskripsi singkat
    long_description=open('README.md').read(),  # Membaca deskripsi panjang dari file README.md
    long_description_content_type='text/markdown',  # Tipe konten untuk deskripsi panjang
    url='https://github.com/LaangYB/LaangUbot',  # URL repositori Anda
    packages=find_packages(),  # Menemukan semua paket
    install_requires=[
        # Daftar dependensi Anda
        'numpy',  # Contoh dependensi
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Ganti dengan lisensi yang sesuai
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versi Python minimum yang dibutuhkan
)
