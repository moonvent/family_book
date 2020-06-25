from lxml import etree


class FamilyTree:
    """
        Класс по работе с данными из XML файла
    """
    def __init__(self):
        doc = etree.parse('test.xml')
        self.list_on_ancestors = []
        for ancestor in doc.findall('ancestor'):
            self.list_on_ancestors.append(tuple(map(lambda info: info.text, ancestor)))

    def find(self, name):
        list_of_finded_ancestors = []
        for ancestor in self.list_on_ancestors:
            if ancestor[0].find(name) > -1:
                list_of_finded_ancestors.append(ancestor)

        return tuple(list_of_finded_ancestors)


if __name__ == '__main__':
    for i in FamilyTree().list_on_ancestor:
        print(i)
