from lxml import etree


def parse():
    doc = etree.parse('test.xml')
    list_on_ancestor = []
    for ancestor in doc.findall('ancestor'):
        list_on_ancestor.append(tuple(map(lambda info: info.text, ancestor)))
    return list_on_ancestor


if __name__ == '__main__':
    for i in parse():
        print(i)
