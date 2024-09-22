from setuptools import setup, find_packages

setup(
    name="projekku",  # Nama package, harus unik di PyPI
    version="0.1.0",  # Versi package
    packages=find_packages(),  # Mencari semua modul di package
    author="Anugrah Fitri",
    author_email="irafitrinovanda@gmaill.com",
    description="hanya mengetes ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Jika README.md menggunakan format Markdown
    url="https://github.com/anugrahfitri-code/my_package",  # URL ke repository, jika ada
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Sesuaikan lisensi
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versi Python yang didukung
)
