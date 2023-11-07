import os, re
from pathlib import Path

# define filename class
class Filename():

    def __init__(self, name_str='', category='', source='',year='', keywords=list(), suffix='') -> None:
        """name_str can be divided into other parameters"""

        self.name_str = name_str
        self.category = category
        self.source = source
        self.year = year
        self.keywords = keywords
        self.suffix = suffix
        self.str_cache = '' # cache string information

    def divide(self) -> object:
        """divide name_str to other parameters"""

        # could be merged through better regular expression

        # find the categropy in name_str
        categorpy_re = re.compile(r'^\[(\w+)\]')
        self.category = (categorpy_re.search(self.name_str).group(1))

        # find the year in name_str
        year_re = re.compile(r'\] (\d{4}) \- ')
        try:
            self.year = year_re.search(self.name_str).group(1)
        except AttributeError:
            pass

        # find the source in name_str
        if self.year:
            source_re = re.compile(r'\] \d{4} \- (.+) \- ')
            self.source = source_re.search(self.name_str).group(1)
        else:
            source_re = re.compile(r'\] (.+) \- ')
            self.source = source_re.search(self.name_str).group(1)

        # find the keywords in name_str
        keywords_re = re.compile(r'\].*\- (.*)\.')
        keywords_str = keywords_re.search(self.name_str).group(1)
        self.keywords = keywords_str.split(' ')

        # find the suffix in name_str
        suffix_re = re.compile(r'\.(\w+)$')
        self.suffix = suffix_re.search(self.name_str).group(1)

        return self

    def merge(self) -> object:
        """merge parameters into name_str"""
        
        if self.year:
            self.name_str = f'[{self.category}] {self.year} - {self.source} - {" ".join(self.keywords)}.{self.suffix}'
        else:
            self.name_str = f'[{self.category}] {self.source} - {" ".join(self.keywords)}.{self.suffix}'

        return self

def read_filenames(path: str) -> list:
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
        filenames = read_filenames(path)
        print(f'file count: {len(filenames)}')
        for filename in filenames:
            print(filename)

    """2. test def in class Filename"""
    if False:
        name1 = '[Application] Agilent - RPLC 维生素 PDA 2002.pdf'
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
        print(f'The suffix of "{name1}" is "{file1.suffix}"')
        print(f'The suffix of "{name2}" is "{file2.suffix}"')
        file1.merge()
        file2.merge()
        print(f'Filename.merge test: {name1 == file1.name_str and name2 == file2.name_str}')

    """3. rename file name"""
    if True:
        path = 'C:\\Users\\06427\\Desktop\\文献资料\\化学分析\\LC\\WELL_BEHAVED'
        filenames = read_filenames(path)
        for filename in filenames:
            file = Filename(name_str=filename)
            file.str_cache = file.name_str
            file.divide()
            if file.source.lower() == 'Application'.lower():
                file.source = 'Resource'
            file.merge()
            if file.name_str not in filenames:
                Path(path / file.str_cache).rename(Path(path / file.name_str))
