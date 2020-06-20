import json
import os


import requests
import tqdm


def flatten_specs(specializations):
    specs_flatten = []
    for spec in specializations:
        specs_flatten.append({key:spec[key] for key in ['id', 'name']})
        for subspec in spec['specializations']:
            specs_flatten.append(subspec)
    return specs_flatten


def get_vacancies(dst_folder):
    if not os.path.isdir(dst_folder):
        os.makedirs(dst_folder)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'
    }
    params = {'per_page': 100}
    specs = requests.get('https://api.hh.ru/specializations', headers=headers).json()
    specs = flatten_specs(specs)
    
    for idx, spec in enumerate(tqdm(specs)):
        vacancies = []
        for i in range(20):
            response = requests.get('https://api.hh.ru/vacancies',
                                    headers=headers,
                                    timeout=5,
                                    params={'specialization': spec['id'],
                                            'per_page': 100,
                                            'page': i})
            if response.status_code != 200:
                break
            vacancies += response.json()['items']

        with open(f"{spec['name'].replace(',', '').replace(' ', '_').replace('/', '_')}.json", 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False)


def extract_info(json_data):
    res_data = {}
    res_data['id'] = json_data['id']
    res_data['name'] = json_data['name']
    res_data['employer'] = json_data['employer']['name']
    
    if json_data['salary'] is None:
        res_data['salary'] = None
    elif json_data['salary']['from'] is not None and json_data['salary']['to'] is not None:
        res_data['salary'] = (json_data['salary']['to'] \
                             + json_data['salary']['from']) // 2
    elif json_data['salary']['from'] is not None:
        res_data['salary'] = json_data['salary']['from']
    elif json_data['salary']['to'] is not None:
        res_data['salary'] = json_data['salary']['to']
    else:
        res_data['salary'] = None
    if res_data['salary'] is not None:
        if json_data['salary']['currency'] == 'EUR':
            res_data['salary'] *= 80
        elif json_data['salary']['currency'] == 'USD':
            res_data['salary'] *= 70
    
    requirement = json_data['snippet']['requirement']
    if requirement is not None:
        if requirement.endswith('...'):
            res_data['requirement'] = requirement.split('.')[:-4]
        else:
            res_data['requirement'] = requirement.split('.')
    else:
        res_data['requirement'] = None
    
    responsibility = json_data['snippet']['responsibility']
    if responsibility is not None:
        if responsibility.endswith('...'):
            res_data['responsibility'] = responsibility.split('.')[:-4]
        else:
            res_data['responsibility'] = responsibility.split('. ')
    else:
        res_data['responsibility'] = None
    
    return res_data


def shorten_vacancies_info(src_folder, dst_folder):
    if not os.path.isdir(dst_folder):
        os.makedirs(dst_folder)
    for fpath in tqdm(fpaths):
        with open(fpath) as f:
            vacancy = os.path.splitext(os.path.basename(fpath))[0]
            data = json.load(f)
        data = [extract_info(d) for d in data]
        with open(os.path.join(dst_folder, f'{vacancy}.json'), 'w') as f:
            json.dump(data, f, ensure_ascii=False)


def aggregate_specs_info(shorten_vacancies_dir, dst_fpath):
    all_specializations = {}
    for fname in tqdm(os.listdir(shorten_vacancies_dir)):
        spec = os.path.splitext(fname)[0]
        fpath = os.path.join(shorten_vacancies_dir, fname)
        with open(fpath) as f:
            data = json.load(f)
        responsibilities = []
        requirements = []
        salaries = []
        for d in data:
            if d['requirement'] is not None:
                requirements += d['requirement']
            if d['responsibility'] is not None:
                responsibilities += d['responsibility']
            if d['salary'] is not None:
                salaries.append(d['salary'])
        all_specializations[spec] = {'requirements': requirements, 'responsibilities': responsibilities, 'salaries': salaries}
    with open(dst_fpath, 'w') as f:
        json.dump(all_specializations, f, ensure_ascii=False)