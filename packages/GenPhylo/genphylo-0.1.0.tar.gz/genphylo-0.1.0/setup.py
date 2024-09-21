from setuptools import setup, find_packages

setup(
    name='genphylo',  # Package name in lowercase
    version='0.1.0',  # Initial version
    author='Marta Casanellas, Martí Cortada, Adrià Dieguez',
    author_email='marta.casanellas@upc.edu',
    description='GenPhylo generates synthetic alignments on a phylogenetic tree with given branch lengths.',
    long_description=open('README.md').read(),  # Ensure README.md exists
    long_description_content_type='text/markdown',  # Ensure this matches the README format
    url='https://github.com/GenPhyloProject/GenPhylo',  # Link to your GitHub repo
    packages=find_packages(),  # Automatically find and include your package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify Python version support
    install_requires=[
        # List your package dependencies here, e.g., 'numpy>=1.18.0'
    ],
)

