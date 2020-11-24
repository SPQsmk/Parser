import sys


def parse_file(path):
    doc = {}
    key = ''

    with open(path, 'r') as f:
        for line in f:
            # Пропуск комментариев
            if line.startswith('#'):
                continue

            # Убираю пробелы, \t\n... в левой части строки
            data = line.lstrip()

            # Если форматированная строка пустая
            if len(data) == 0:
                # Если словарь не пустой
                if len(doc) != 0:
                    yield doc
                    doc = {}
                    key = ''
                # Пропуск пустой строки
                continue

            # Если после удаления пробельных символов с левой части строки,
            # длина получившейся строки равна длине исходной, то строка начинается с ключа
            if len(data) == len(line):
                # Индекс первого двоеточия
                colon_id = data.find(':')
                # Разбиваю строку на ключ и значения
                key = data[:colon_id]
                # Удаляю пробельные символы с обеих сторон значения
                val = data[colon_id + 1:].strip()
                # Еслю ключа еще нет в словаре, то создаю его
                if not key in doc:
                    doc[key] = val
                # Если ключ есть, то добавляю к его значению новое
                else:
                    doc[key] += f'\n{val}'
            # Если в строке нет ключа, то добавляю значение к значению предыдущего ключа
            else:
                doc[key] += f'\n{data.strip()}'
        # Если словарь не пустой, добавляю в список документов
        if len(doc) != 0:
            yield doc


def load_data(path):
    parsed_data = parse_file(path)

    with open('res.txt', 'w') as f:
        for document in parsed_data:
            res = '{'
            for key in document:
                # Если значение многострочное
                if '\n' in document[key]:
                    strs = document[key].split('\n')
                    res += f"'{key}': '{strs[0]}\\n'"
                    for i in range(1, len(strs) - 1):
                        res += f"\n{' '*(len(key) + 4)}'{strs[i]}\\n'"
                    res += f"\n{' '*(len(key) + 4)}'{strs[-1]}'"
                else:
                    res += f"'{key}': '{document[key]}'"
                res += ',\n'
            res = res[:-2] + '}\n'
            f.write(res)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        filename = 'example.txt'
    else:
        filename = args[0]
    try:
        load_data(filename)
    except:
        print('Incorrect filename')
