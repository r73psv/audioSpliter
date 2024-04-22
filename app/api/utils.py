# парсер config файла
def config_parser(config_path):
    with open(config_path, 'r') as config_file:
        # создаем словарь и построчно читаем в него содержимое файла
        config = dict()
        lines = config_file.readlines()
        for line in lines:
            k, v = line.split(' = ')
            config[k] = v.split('\n')[0]
            return config