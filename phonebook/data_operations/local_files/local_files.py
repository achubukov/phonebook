import os

from phonebook.data_operations.api.api import API


class LocalFiles:

    def __init__(self, base_path=os.getcwd()):
        self.base_path = os.path.join(base_path, '_справочник_')
        print(self.base_path)
        try:
            os.makedirs(self.base_path)
        except OSError:
            print('Дирректория уже существует')

    def _is_phone_in_book(self, phone):
        tree = os.walk(self.base_path)
        for i in tree:
            if len(i[2]) != 0:
                for j in i[2]:
                    with open(os.path.join(i[0], j), 'r') as f:
                        # if phone.find(f.read()) != -1:
                        if f.read() == str(phone):
                            return True
        return False

    def _find_name_in_book(self, name):
        tree = os.walk(self.base_path)
        for i in tree:
            if len(i[2]) != 0:
                for j in i[2]:
                    full_path = os.path.join(i[0], j)
                    if name == os.path.splitext(os.path.basename(full_path))[0]:
                        return full_path
        return 'None'

    def save_phone(self, phone, name):
        if not LocalFiles._is_phone_in_book(self, phone):
            response_dict = API().send_request(phone)
            if 'valid' in response_dict and response_dict.get('valid') is True:
                country_name = response_dict.get('country_name')
                dir = os.path.join(self.base_path, country_name)
                try:
                    os.mkdir(dir)
                except OSError:
                    pass
                f_path = os.path.join(dir, name)
                if not os.path.isfile(f_path):
                    with open(f_path, 'w') as f:
                        f.write(response_dict.get('number'))
                else:
                    print('Человек уже записан!')

            elif 'valid' in response_dict and response_dict.get('valid') is False:
                print('Номер неопределен')
            else:
                print(response_dict['type'], response_dict['info'], sep='\n')
        else:
            print('Номер уже в справочнике')

    #
    # def list_phones(self, country, limit):
    #
    def search_by_name(self, name):
        path = self._find_name_in_book(name)
        if path != 'None':
            with open(path, 'r') as f:
                print(name, ' - ', f.read())
            return True
        else:
            print('Запись не найдена')
            return False

    def delete_phone_by_name(self, name):
        path = self._find_name_in_book(name)
        if path != 'None':
            os.remove(path)
            print('номер удален')
        else:
            print('нет такой записи')
        return


