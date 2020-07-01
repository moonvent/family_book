from lxml import etree


class FamilyTree:
    """
        Класс по работе с данными из XML файла
    """
    def __init__(self):
        doc = etree.parse(r'static\семья.xml')

        self.data = {}
        for something in doc.getroot()[:-3]:
            if something.tag == 'events':
                continue
            self.data[something.tag] = []
            for children in something:
                person_in_program = dict(children.attrib)

                for tag in children:
                    if tag.tag == 'nearest' and tag.text:
                        nearest = {'nearest': []}
                        for child_nearest in tag:
                            nearest.get('nearest').append(dict(child_nearest.attrib))
                        person_in_program.update(nearest)
                    else:
                        person_in_program.update({tag.tag: tag.text})

                self.data[something.tag].append(person_in_program)

    def find(self, name):
        list_of_finded_ancestors = []
        for ancestor in self.data.get('persons'):
            if ancestor.get('fullname').lower().find(name.lower()) > -1:
                list_of_finded_ancestors.append({'id': ancestor.get('id'),
                                                'fullname': ancestor.get('fullname'),})
        return tuple(list_of_finded_ancestors)

    def sort_need_data(self, tuple_of_data):
        tuple_of_data, image = tuple_of_data
        result_dict = {}
        # if tuple_of_data.get('fullname'):

        if tuple_of_data.get('comment'):
            result_dict.update({'comment': 'Комментарий: ' + tuple_of_data.get('comment')})
        else:
            result_dict.update({'comment': None})
        result_dict.update({'fullname': 'Имя: ' + tuple_of_data.get('fullname')})

        if tuple_of_data.get('nearest'):
            result_dict.update({'nearest': tuple_of_data.get('nearest')})
        else:
            result_dict.update({'nearest': None})

        if tuple_of_data.get('bdate'):
            result_dict.update({'bdate': 'Годы жизни: ' + tuple_of_data.get('bdate')})
        return result_dict, image, len(result_dict) / 2 * .1

    def find_full(self, id_):
        for ancestor in self.data.get('persons'):
            if ancestor.get('id') == id_:
                return self.sort_need_data((ancestor, tuple(i.get('path') for i in self.data.get('docs') if i.get('id') == id_)))


if __name__ == '__main__':
    for i in FamilyTree().find('1'):
        print(i)
