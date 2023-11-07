import os, re
from pathlib import Path

# define filename class
class Filename():

    def __init__(self, name_str ='', category='', source='',year='', keywords=list()) -> None:
        """name_str can be divided into other parameters"""
        self.name_str = name_str
        self.category = category
        self.source = source
        self.year = year
        self.keywords = keywords

    def divide(self) -> object:
        """divide name_str to other parameters"""
        
        # find the categropy in name_str
        categorpy_re = re.compile(r'^\[\w+\]')
        self.category = (categorpy_re.search(self.name_str).group())[1:-1]

        # find the source and year in name_str
        year_re = re.compile(r'\] \d - ')
        source_re = re.compile(r'[\]\-] \d*\D+ - ')
        self.source = source_re.search(self.name_str).group()

        return self

    def merge(self) -> object:
        """merge parameters into name_str"""
        pass

def read_filenames(path: Path) -> list:
    """
    read files named in '[XX] XX' format in a folder
    """

    filenames = os.listdir(path)

    # only read well behaved name
    name_re = re.compile(r'^\[\w+\]')
    for name in filenames[:]:
        if not name_re.search(name):
            filenames.remove(name)

    return filenames

if __name__ == '__main__':

    """1. read all well behaved files"""
    if False:
        path = 'C:\\Users\\06427\\Desktop\\文献资料\\化学分析\\LC\\WELL_BEHAVED'
        data = read_filenames(path)
        print(f'file count: {len(data)}')
        for name in data:
            print(name)

    """2. test def in class Filename"""
    if True:
        name1 = '[Application] Agilent - RPLC 维生素 PDA.pdf'
        name2 = '[Research] 2020 - J Chromatogr A - RPLC 混合模式 离子交换 评测.pdf'
        file1 = Filename(name_str=name1)
        file2 = Filename(name_str=name2)
        file1.divide()
        file2.divide()
        print(f'The category of "{name1}" is "{file1.category}"')
        print(f'The category of "{name2}" is "{file2.category}"')
        print(f'The source of "{name1}" is "{file1.source}"')
        print(f'The source of "{name2}" is "{file2.source}"')
        print(f'The year of "{name1}" is "{file1.year}"')
        print(f'The year of "{name2}" is "{file2.year}"')
        print(f'The keywords of "{name1}" is:')
        for keyword in file1.keywords:
            print(keyword)
        print(f'The keywords of "{name2}" is:')
        for keyword in file2.keywords:
            print(keyword)
        