from setuptools import setup, find_packages

setup(
    name='pyqt-editable-treewidget-example',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt example of QTreeWidget which is editable (intuitive enough to use)',
    url='https://github.com/yjg30737/pyqt-editable-treewidget-example.git',
    install_requires=[
        'PyQt5>=5.8'
    ]
)