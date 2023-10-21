import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import os.path

def correct_df(df: pd.DataFrame, index: int):
    for i in range(5):
        df.at[index + i, 'optimized trains'] = df.iloc[index + 2 + i]['optimized trains']
    df = df.drop(index=[len(df) - 1, len(df) - 2])
    return df

def count_trains_in_station(data: pd.DataFrame, station: int, param: str):
    arriving = data[data.end == station]
    serving = data[data.start == station]
    return arriving[param].sum(), serving[param].sum()

def get_pairs(ids, data, param):
    dict_of_pairs = {}
    for id in ids:
        dict_of_pairs[id] = int(data[data.id == id][param])
    return dict_of_pairs

def sep_trains(routes: dict, target: int, updated_routes: list[int], data: pd.DataFrame):
    result = {}
    routes_to_pop = []
    already_done = {}
    for route in routes.keys():
        if route in updated_routes:
            already_done[route] = data[data.id == route]['optimized trains']

    for key, value in already_done.items():
        if not isinstance(value, (int, float)):
            already_done[key] = 0
            data.at[key, 'optimized trains'] = 0

    for item in routes_to_pop:
        del routes[item]


    if sum(already_done.values()) > target:
        while sum(already_done.values()) > target:
            for key in already_done.values():
                already_done[key] -= 10
        target -= sum(already_done.values())
    else:
        target -= sum(already_done.values())

        
    for route, trains in routes.items():
        if target == 0:
            result[route] = 0
        elif target >= trains:    
            result[route] = trains
            target -= trains
        elif target < trains:
            result[route] = target
            target -= target
        
    return result

updated_routes = []
def calc_one_station(my_data: pd.DataFrame, station: int, param: str):
    incoming_routes = get_pairs(list(my_data[my_data.end == station]['id']), my_data, param=param)
    outcoming_routes = get_pairs(list(my_data[my_data.start == station]['id']), my_data, param=param)
    global updated_routes

    target = min(count_trains_in_station(my_data, station, param=param))
    sep_incoming = sep_trains(incoming_routes, target, updated_routes, data=my_data)
    sep_outcoming = sep_trains(outcoming_routes, target, updated_routes, data=my_data)

    for route, amount in sep_incoming.items():
        my_data.at[route, 'optimized trains'] = amount
        # print(amount)
        updated_routes.append(route)

    for route, amount in sep_outcoming.items():
        my_data.at[route, 'optimized trains'] =  amount
        # print(amount)
        updated_routes.append(route)

    return my_data

def start_calculating(data: pd.DataFrame, param):
    my_data = data
    # my_data['optimized trains_2'] = ""
    global updated_routes
    updated_routes = []

    # Считаем значения для вершин с 1 связью
    for index in range(len(my_data)-2):
        route = my_data.iloc[index]
        # print(route)
        station = int(route['start'])
        incoming_routes = list(data[data.end == station]['id'])
        outcoming_routes = list(data[data.start == station]['id'])

        if len(incoming_routes) == 1 and len(outcoming_routes) == 1:
            my_data = calc_one_station(my_data=my_data, station=station, param=param)

    # Считаем остальные элементы
    for index in range(len(my_data)-2):
        route = my_data.iloc[index]
        station = int(route['start'])
        
        my_data = calc_one_station(my_data=my_data, station=station, param=param)

    return correct_df(my_data, 171)

def start_second_task(data: pd.DataFrame):
    data['amount_of_trains_2'] = ""

    for index in range(len(data)):
        value = round(float(data.iloc[index]['tonnage_limit']) / float(data.iloc[index]['max_train_tonnage']), 0)
        data.at[index, 'amount_of_trains_2'] = value

    return calculate_tonnage(update_amount_of_trains(data))

def update_amount_of_trains(data: pd.DataFrame):
    data = data.rename(columns={'optimized trains' : 'planed trains'})
    updated_data = start_calculating(data, param='amount_of_trains_2')
    del updated_data['amount_of_trains_2']

    return updated_data

def calculate_tonnage(data: pd.DataFrame):
    data = data.rename(columns={'optimized trains':'optimized trains (task2)'})
    data['tonnage_for_train'] = ''

    for index in range(len(data)):
        value = float(data.iloc[index]['tonnage_limit']) / int(data.iloc[index]['optimized trains (task2)'])
        value = value if value <= int(data.iloc[index]['max_train_tonnage']) else int(data.iloc[index]['max_train_tonnage'])
        data.at[index, 'tonnage_for_train'] = value
    del data['planed trains']

    return data

def work_with_file(path_to_csv: str, final_filname: str = 'updated_data'):
    if not os.path.exists(path_to_csv):
        raise Exception("Указан неверный путь к файлу или файла не существует")
    
    if not path_to_csv.endswith('.csv'):
        raise Exception('Файл с данными должен иметь расширение .csv')
    
    
    data = pd.read_csv(path_to_csv)
    my_data = data.copy()

    my_data = start_calculating(data, param='quantity_limit')
    my_data = start_second_task(my_data)
    my_data = start_calculating(my_data, param='quantity_limit')
    del my_data['Unnamed: 0']
    
    my_data.to_csv(f'{final_filname}.csv')

    return f'{final_filname}.csv'



def main():
    path_to_csv = input('Введите путь к файлу с данными: ')
    name_for_new_file = input('Введите название файла с результатом оптимизации (без постфикса .csv): ')

    work_with_file(path_to_csv=path_to_csv, final_filname=name_for_new_file)

if __name__ == "__main__":
    main() 