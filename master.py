import os, re, csv
from pathlib import Path
from collections import Counter

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
        self.cache = None # cache information

    def divide(self) -> object:
        """divide name_str to other parameters"""

        # could be merged through better regular expression

        try:
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

        except AttributeError:
            print(f'Wrong name: {self.name_str}')

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

def merge_two_dicts(dict1: dict, dict2: dict) -> dict:
    """merge two dicts in the form of {str: int}"""

    new_dict = dict()

    for key, count in dict1.items():
        if key in dict2:
            new_dict[key] = count + dict2[key]
        else:
            new_dict[key] = count
    
    for key, count in dict2.items():
        if key not in new_dict:
            new_dict[key] = count

    return new_dict

if __name__ == '__main__':

    """Function 1. read all well behaved files and write content to csv files"""
    if False:
        path = 'C:\\Users\\06427\\Desktop\\文献资料\\化学分析\\LC\\WELL_BEHAVED'
        filenames = read_filenames(path)
        print(f'file count: {len(filenames)}')

        file_list = list()
        for filename in filenames:
            file = Filename(name_str=filename)
            file.divide()
            file_list.append(file)
        
        # output a csv file named 'output_filenames.csv' containing all filenames
        if True:
            with open('output_filenames.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['suffix', 'category', 'year', 'source', 'keywords'])
                for file in file_list:
                    writer.writerow([file.suffix, file.category, file.year, file.source, *(file.keywords)])
        
        # output a csv file named 'output_keywords_count.csv' containing keywords count
        if True:
            keywords_dict = dict()
            for file in file_list:
                keywords_dict = merge_two_dicts(keywords_dict, Counter(file.keywords))

            with open('output_keywords_count.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['keyword', 'count'])
                for key, value in keywords_dict.items():
                    writer.writerow([key, value])

    """Function 2. rename file name with new catalog and sorted keywords"""
    if False:
        path = Path('C:\\Users\\06427\\Desktop\\文献资料\\化学分析\\LC\\WELL_BEHAVED')
        filenames = read_filenames(path)
        for filename in filenames:
            file = Filename(name_str=filename)
            file.divide()
            if file.category.lower() in ['handbook', 'application', 'brochure']:
                file.category = 'Resource'
            file.keywords.sort()
            file.merge()
            try:
                Path(path / filename).rename(Path(path / file.name_str))
                print(f'old name: {filename}, new name: {file.name_str}')
            except FileExistsError:
                print(f'{filename} can not be renamed, because new name {file.name_str} is exsit!')

    """Test 1. Filename.divide() and Filename.merge()"""
    if False:
        name1 = '[Application] Agilent - RPLC 维生素 PDA 2002.pdf'
        name2 = '[Research] 2020 - J Chromatogr A - RPLC 混合模式 离子交换 评测.pdf'
        file1 = Filename(name_str=name1)
        file2 = Filename(name_str=name2)
        file1.divide()
        file2.divide()
        print(f"Filename.divide() category test: {file1.category == 'Application' and file2.category == 'Research'}")
        print(f"Filename.divide() source test: {file1.source == 'Agilent' and file2.source == 'J Chromatogr A'}")
        print(f"Filename.divide() year test: {file1.year == '' and file2.year == '2020'}")
        print(f"Filename.divide() keywords test: {file1.keywords == ['RPLC', '维生素', 'PDA', '2002'] and file2.keywords == ['RPLC', '混合模式', '离子交换', '评测']}")
        print(f"Filename.divide() suffix test: {file1.suffix == 'pdf' and file2.suffix == 'pdf'}")
        file1.merge()
        file2.merge()
        print(f'Filename.merge() test: {name1 == file1.name_str and name2 == file2.name_str}')

    """Test 2. def merge_two_dicts()"""
    if False:
        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'a':4, 'd': 10}
        res_dict = {'a': 5, 'b': 2, 'c': 3, 'd': 10}
        print(f'def merge_two_dicts() test: {res_dict == merge_two_dicts(dict1, dict2) and dict1 == merge_two_dicts(dict(), dict1)}')

    """"""