import re

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
        print(tuple_of_data[0])
        tuple_of_data, image = tuple_of_data
        result_dict = {}
        # if tuple_of_data.get('fullname'):

        if tuple_of_data.get('comment'):
            result_dict.update({'comment': tuple_of_data.get('comment')})
        else:
            result_dict.update({'comment': None})

        result_dict.update({'fullname': re.sub(r'\([^)]*\)', '', tuple_of_data.get('fullname')).replace('  ', ' ')})

        if tuple_of_data.get('nearest'):
            result_dict.update({'nearest': tuple_of_data.get('nearest')})
        else:
            result_dict.update({'nearest': None})

        if tuple_of_data.get('bdate'):
            result_dict.update({'bdate': tuple_of_data.get('bdate')})

        result_dict['parents'] = tuple(parent for parent in tuple_of_data.get('nearest') if parent.get('rel') in ('Отец', 'Мать'))

        second_half = tuple(near for near in tuple_of_data.get('nearest') if near.get('rel') in ('Жена', 'Муж', 'Супруг', 'Супруга'))
        for one_person in second_half:
            one_person['rel'] = 'Супруга' if one_person.get('rel') in ('Жена', 'Супруга') else 'Супруг'
            one_person['fullname'] = re.sub(r'\([^)]*\)', '', one_person.get('fullname')).replace('  ', ' ')

        result_dict['second_half'] = second_half

        result_dict['bro_and_sis'] = tuple(bro_and_sis for bro_and_sis in tuple_of_data.get('nearest') if bro_and_sis.get('rel') in ('Брат', 'Сестра'))

        result_dict['childrens'] = tuple(children for children in tuple_of_data.get('nearest') if children.get('rel') in ('Сын', 'Дочь'))

        # for item in tuple_of_data.items():
        #     print(item)

        return result_dict, image

    def find_full(self, id_):
        for ancestor in self.data.get('persons'):
            if ancestor.get('id') == id_:
                return self.sort_need_data((ancestor, tuple(i.get('path') for i in self.data.get('docs') if i.get('id') == id_)))


if __name__ == '__main__':
    for i in FamilyTree().find('1'):
        print(i)
