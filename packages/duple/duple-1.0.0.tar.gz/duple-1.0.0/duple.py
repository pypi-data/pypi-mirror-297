import click
from pathlib import Path
import os
import hashlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map             #concurrency
from itertools import repeat
from humanize import naturalsize
import json
from collections import Counter
from send2trash import send2trash
from time import perf_counter
from datetime import datetime as dt

def get_hash(path: str, hash: str) -> str:
    with open(path, 'rb') as f:
        digest = hashlib.file_digest(f, hash)
    return digest.hexdigest(), path

def dict_from_stat(stats: os.stat_result) -> dict:
    temp = repr(stats).replace('os.stat_result(', '').replace(')','').replace(' ', '').split(',')
    result = dict()
    for item in temp:
        temp_item = item.split('=')
        result[temp_item[0]] = int(temp_item[1])
    return result

def dump_dict_to_json(input: dict, filename: str, indent: int = 4):
    with open(filename, 'w') as f:
        json.dump(input, f, indent=indent)

def traverse_files(path: str) -> dict | list:
    #cycle through all files collecting information
    result = dict()
    #  key = path, value = dictionary
    #     value dictionary:
    #         os.stat_result
    #         depth
    #         type
    
    for root, dirs, files in tqdm(os.walk(path, followlinks = False), desc = 'Preprocessing File Tree'):
        for file in files:
            temp = f'{root}/{file}'
            tempPath = Path(temp)
            if tempPath.exists():
                result[temp] = dict_from_stat(tempPath.stat())
                result[temp]['type'] = 'ignored'
                result[temp]['depth'] = len(tempPath.parents)

    sizes = dict()
    for key, value in result.items():
        if value['st_size'] not in sizes.keys():
            sizes[value['st_size']] = list()
        sizes[value['st_size']].append(key)
    
    potential_duplicates = list()
    for key, value in sizes.items():
        if len(value) > 1:
            for file in value:
                result[file]['type'] = 'potential_duplicate'
                potential_duplicates.append(file)
    
    return result, potential_duplicates

def annotate_duplicates(hashes: list, all_files: dict, 
                                                        depth_lowest: bool, 
                                                        depth_highest: bool,
                                                        shortest_name: bool,
                                                        longest_name: bool,
                                                        created_oldest: bool,
                                                        created_newest: bool,
                                                        modified_oldest: bool,
                                                        modified_newest: bool) -> dict | dict:
    
    # define test functions
    def path_depth(path: str) -> int:
        return all_files[path]['depth'], path
        return len(Path(path).parents)
    
    def name_length(path: str) -> int:
        return len(Path(path).name), path
    
    def created_date(path: str) -> int:
        return all_files[path]['st_birthtime'], path
        return Path(path).stat().st_birthtime
    
    def modified_date(path: str) -> int: 
        return all_files[path]['st_mtime'], path
        return Path(path).stat().st_mtime

    # select the test function based on flag
    options = [(depth_lowest , path_depth, 1),
               (depth_highest , path_depth, -1),
               (shortest_name , name_length, 1),
               (longest_name , name_length, -1),
               (created_oldest ,  created_date, 1),
               (created_newest , created_date, -1),
               (modified_oldest , modified_date, 1),
               (modified_newest , modified_date, -1)]
    
    for flag, function, option in options:
        if flag:
            test_fun = function
            negate = option
    
    #group hashes
    grouped_hashes = dict()
    for key, value in hashes:
        if key not in grouped_hashes.keys():
            grouped_hashes[key] = list()
        grouped_hashes[key].append(value)

    dupes = dict()
    for hash, file_paths in grouped_hashes.items():
        for file_path in file_paths:
            all_files[file_path]['hash'] = hash
            if hash not in dupes.keys():
                dupes[hash] = list()
            dupes[hash].append(file_path)
    
    dupes = {key: value for key, value in dupes.items() if len(value) > 1}

    for value in dupes.values():
        seed, result = test_fun(value[0])
        for file_path in value:
            if file_path in all_files.keys():
                all_files[file_path]['type'] = 'duplicate'
                all_files[file_path]['twins'] = len(value) - 1

            if negate * seed > negate * test_fun(file_path)[0]:
                seed, result = test_fun(file_path)
        
        all_files[result]['type'] = 'original'

    for key, value in all_files.items():
        if value['type'] == 'potential_duplicate':
            value['type'] = 'original'  

    return all_files, dupes
    
def calculate_statistics(all_files: dict) -> dict:
    result = dict()
    result['total files'] = 0
    result['ignored files'] = 0
    result['duplicates'] = 0
    result['duplicate groups'] = 0
    result['total size - duplicates'] = 0
    result['total size - all files'] = 0

    for key, value in all_files.items():
        
        if value['type'] == 'ignored':
            result['ignored files'] += 1

        if value['type'] == 'duplicate':
            result['total size - duplicates'] += value['st_size']
            result['duplicates'] += 1
        
        if value['type'] == 'original':
            result['duplicate groups'] += 1

        result['total size - all files'] += value['st_size']
        result['total files'] += 1
    
    result['total size - duplicates'] = naturalsize(result['total size - duplicates'])
    result['total size - all files'] = naturalsize(result['total size - all files'])
    return result

def remove_empty_directories() -> None:
    for root, folders, files in os.walk(os.getcwd()):
        if f'.DS_Store' in files:
            send2trash(f'{root}/.DS_Store')

    dirs = list()
    for root, folders, files in os.walk(os.getcwd()):
        if not files and not folders:
            dirs.append(root)

    dirs = sorted(dirs, key = lambda x: -1 * len(Path(x).parents))
    for dir in dirs:
        send2trash(dir)

def get_delete_paths() -> dict:
    if not duple_outputs_exist():
        return
    
    with open('duple.delete', 'r') as f:
        items = f.read().splitlines()
    
    results = dict()
    flag = False
    for item in items:
        if item == 'Duplicate Results:':
            flag = True
        
        if flag and '----' in item:
            break

        if flag and item.split('|')[0].strip() in ['duplicate', 'original']:
            item_split = item.split('|')
            action = item_split[0]
            size = item_split[1]
            path = item_split[2][1:]
            results[path] = {'type': action, 'size': size, 'path': path}

    return results

def duple_outputs_exist() -> bool:
    if not Path('duple.delete').exists() or not Path('duple.json').exists():
        raise FileExistsError('duple.delete and/or duple.json do no exists - run duple scan to create these files')
        return False
    return True

def create_output(all_files: dict, dupes: dict, summary_statistics: dict) -> None:
    
    max_len_key = max([len(k) for k in summary_statistics.keys()])
    max_len_val = max([len(str(v)) for v in summary_statistics.values()])
    max_len_type = max([len(v['type']) for k, v in all_files.items()]) + 2
    max_len_size = max([len(naturalsize(v['st_size'])) for k, v in all_files.items()]) + 2
    section_divider = f"\n{''.rjust(100,'-')}\n\n"

    for key, value in summary_statistics.items():
        click.secho(f'{key.ljust(max_len_key, ".")}{click.style(str(value).rjust(max_len_val,"."), fg = "green")}')

    dump_dict_to_json(all_files, 'duple.json')

    with open('duple.delete', 'w') as f:
        f.write(f'Duple Report Generated on {dt.now().isoformat()}, commanded by user: {os.getlogin()}\n\n')
        f.write(section_divider)
        f.write('Summary Statistics:\n')
        for key, value in summary_statistics.items():
            f.write(f'{key.ljust(max_len_key)}{str(value).rjust(max_len_val)}\n')

        f.write(section_divider)
        f.write('Outputs:\n')
        f.write(f'{os.getcwd()}/duple.delete\n')
        f.write(f'{os.getcwd()}/duple.json\n')

        f.write(section_divider)
        f.write('Instructions to User:\n')
        f.write('The sections below describe what action duple will take when \'duple rm\' is commanded.'
                ' The first column is the flag that tells duple what to do:\n'
                '\torig   : means duple will take no action for this file, listed only as a reference to the user\n'
                '\tdelete : means duple will send this file to the trash can or recycling bin, if able\n')
        
        f.write(section_divider)
        f.write('Duplicate Results:\n')
        if len(dupes.keys()) == 0:
            f.write('No duplicates found.\n')

        for value in dupes.values():
            for file in value:
                if all_files[file]['type'] in ['duplicate','original']:
                    flag = str(all_files[file]["type"]).ljust(max_len_type)
                    size = naturalsize(all_files[file]["st_size"]).rjust(max_len_size)
                    f.write(f'{flag}|{size} | {file}\n')
            f.write('\n')
        
        f.write(section_divider)
        f.write('All Files in Scan:\n')
        for file, stats in all_files.items():
            flag = str(stats["type"]).ljust(max_len_type)
            size = naturalsize(stats["st_size"]).rjust(max_len_size)
            f.write(f'{flag}|{size} | {file}\n')

def get_version() -> str:
    path = Path(__file__).parent
    with open(f'{path}/pyproject.toml', 'r') as f:
        lines = f.read().splitlines()
    
    for line in lines:
        if line[:7] == 'version':
            ver = line[-6:-1]
            return ver

@click.group()
def cli() -> None:
    pass

@cli.command()
def version() -> str:
    '''
    A simple program to find and remove duplciate files.
    '''
    click.secho(f'duple version: {get_version()}')

@cli.command()
@click.argument('path', type = click.STRING)
@click.argument('hash', type = click.STRING)
@click.option('--depth_lowest', '-d', is_flag = True, help = 'keep the file with the lowest pathway depth')
@click.option('--depth_highest', '-D', is_flag = True, help = 'keep the file with the highest pathway depth')
@click.option('--shortest_name', '-s', is_flag = True, help = 'keep the file with the shortest name')
@click.option('--longest_name', '-S', is_flag = True, help = 'keep the file with the longest name')
@click.option('--created_oldest', '-c', is_flag = True, help = 'keep the file with the oldest creation date')
@click.option('--created_newest', '-C', is_flag = True, help = 'keep the file with the newest creation date')
@click.option('--modified_oldest', '-m', is_flag = True, help = 'keep the file with the oldest modification date')
@click.option('--modified_newest', '-M', is_flag = True, help = 'keep the file with the newest modification date')
@click.option('--number_of_cpus', '-ncpu', type = click.INT, help = 'Maximum number of workers (cpu cores) to use for the scan', default = 0)
@click.option('--chunksize', '-ch', type = click.INT, help = 'chunksize to give to workers, minimum of 2', default = 2)
def scan(path: str, hash: str, depth_lowest: bool, 
                               depth_highest: bool,
                               shortest_name: bool,
                               longest_name: bool,
                               created_oldest: bool,
                               created_newest: bool,
                               modified_oldest: bool,
                               modified_newest: bool,
                               number_of_cpus: int = 0,
                               chunksize: int = 2,) -> None:
    '''
    Scan recursively computes a hash of each file and puts the hash into
    a dictionary.  The keys are the hashes of the files, and the values
    are the file paths and metadata.  If an entry has more than 1 file
    associated, they are duplicates.  The original is determined by the
    flags or options (ex: -d).  The duplicates are added to a file called
    duple.delete.
    '''
    
    perf_start_overall = perf_counter()

    # input validation
    if hash not in hashlib.algorithms_available:
        click.secho(f'Hash must be one of the following: {hashlib.algorithms_available}')
        return

    if number_of_cpus > os.cpu_count():
        click.secho(f'Too many cpus (number_of_cpus too high), only using {os.cpu_count()} cpus')
        number_of_cpus = os.cpu_count()
    
    if number_of_cpus == 0:
        number_of_cpus = int(int(os.cpu_count() * 2/3) + 1)
    
    if chunksize < 2:
        click.secho(f'chunksize too low, setting to default of 2')
        chunksize = 2

    flags = [depth_lowest,
            depth_highest,
            shortest_name,
            longest_name,
            created_oldest,
            created_newest,
            modified_oldest,
            modified_newest]

    c = Counter(flags)
    if c[True] > 1:
        click.secho('Only one flag can be chosen at a time.')
        return
    if c[True] == 0:
        click.secho('Must select at least one flag to determine handling of duplicates, ex: -d')
        return

    '''
    # start analysis

    #eliminate files with unique sizes from analysis - if a file has a unique size it isn't a duplicate of another file
    # rawfilesdict = dict()
    # filedict = dict()
    # # click.secho('Preprocessing Directories....')
    # for root, dirs, files in tqdm(os.walk(path, followlinks=False), desc = 'Preprocessing Directories'):
    #     for file in files:
    #         temp = f'{root}/{file}'
    #         tempPath = Path(temp)
    #         if tempPath.exists():
    #             tempStat = dict_from_stat(tempPath.stat())
    #             rawfilesdict[temp] = tempStat
    #             if tempStat['st_size'] not in filedict.keys():
    #                 filedict[tempStat['st_size']] = list()
    #             filedict[tempStat['st_size']].append(temp)
    '''

    perf_start_file_traversal = perf_counter()
    all_files, potential_duplicates = traverse_files(path)
    perf_finish_file_traversal = perf_counter()

    '''
    # filelist = list()
    # for k, v in filedict.items():
    #     if len(v) > 1:
    #         filelist.extend(v)
    #/eliminate files with unique sizes from analysis

    # hash_start = perf_counter()
    # hashes = process_map(get_hash, filelist, repeat(hash), max_workers = number_of_cpus, chunksize = 2, desc = 'Hashing Files...')
    # hash_finish = perf_counter()
    '''

    perf_start_hash = perf_counter()
    hashes = process_map(get_hash, potential_duplicates, repeat(hash), max_workers = number_of_cpus, chunksize = 2, desc = 'Hashing Files...')
    perf_finish_hash = perf_counter()

    perf_start_report_duplicates = perf_counter()
    all_files, dupes = annotate_duplicates(hashes, all_files, *flags)
    perf_finish_report_duplicates = perf_counter()

    perf_start_statistics = perf_counter()
    summary_statistics = calculate_statistics(all_files)
    perf_finish_statistics = perf_counter()

    perf_finish_overall = perf_counter()
    
    summary_statistics['hash_type'] = hash
    summary_statistics['file system traveral time (seconds)'] = round(perf_finish_file_traversal - perf_start_file_traversal, 4)
    summary_statistics['hashing time (seconds)'] = round(perf_finish_hash - perf_start_hash, 4)
    summary_statistics['annotating duplicates (seconds)'] = round(perf_finish_report_duplicates - perf_start_report_duplicates, 4)
    summary_statistics['calculating statistics time (seconds)'] = round(perf_finish_statistics - perf_start_statistics, 4)
    summary_statistics['total time (seconds)'] = round(perf_finish_overall - perf_start_overall, 4)
    summary_statistics['wrote summary results'] = f'{os.getcwd()}/duple.delete'
    summary_statistics['wrote raw results'] = f'{os.getcwd()}/duple.json'
    summary_statistics['version'] = get_version()
    
    create_output(all_files, dupes, summary_statistics)

@cli.command()
@click.option('--verbose', '-v', is_flag = True, help = 'Use this flag to enter verbose mode')
@click.option('--dry_run', '-dr', is_flag = True, help = 'Perform dry run, do everything except for deleting the files')
def rm(verbose: bool, dry_run: bool) -> None:
    '''
    rm sends all 'duplicate' files specified in duple.delete to the trash folder
    '''

    if not duple_outputs_exist():
        return
    
    files = get_delete_paths()
    if not verbose:
        for file, data in tqdm(files.items()):
            if data['type'].strip() == 'duplicate':
                if not dry_run:
                    send2trash(file)
    
    else:    
        cnt = 0
        total = len(files.keys())
        for file, data in files.items():

            if data['type'].strip() == 'duplicate' and not dry_run:
                type_style = click.style('deleted'.ljust(14), fg = 'yellow')
                send2trash(file)
            
            if data['type'].strip() == 'duplicate' and dry_run:
                type_style = click.style('will delete'.ljust(14), fg = 'yellow')

            if data['type'].strip() == 'original' and dry_run:
                type_style = click.style('will keep'.ljust(14), fg = 'green')

            if data['type'].strip() == 'original' and not dry_run:
                type_style = click.style('kept'.ljust(14), fg = 'green')
            
            cnt += 1
            completion_style = click.style(f'[{cnt/total*100 : 6.1f}%]', fg = 'cyan')
            click.secho(f'{completion_style} {type_style}{data["size"]} -->  {file}')

    remove_empty_directories()