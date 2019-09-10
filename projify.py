#!/user/bin/env python3

"""
Creates Qt Creator basic projects from NRF52 SDK's Makefiles
    python3 projify.py /home/nRF5_SDK_15.3.0_59ac345/examples/peripheral/blinky/pca10040/blank/armgcc/Makefile
"""

import sys
import os
import re


def load_makefile():
    # Get makefile path
    try:
        mk_path = sys.argv[1]
        if mk_path[-1] in ['\\', '/']:
            mk_path = mk_path[:-1]
        mk_dir, mk_name = os.path.split(mk_path)
    except IndexError:
        sys.exit('Nothing to do! Pass path to Makefile as an argument!')
    # Read makefile
    try:
        with open(mk_path, 'r') as file:
            return (file.readlines(), mk_dir)
    except FileNotFoundError:
        sys.exit('%s was not found!' % mk_path)


def get_var(mk_file, var_name):
    var_name_re = re.compile('(^\s*%s\s*:=\s*)(\S*)' % var_name)
    for line in mk_file:
        re_res = var_name_re.match(line)
        if re_res:
            var_value = re_res.group(2)
            break
    else:
        sys.exit('%s variable was not found!' % var_name)
    print('%s = %s' % (var_name, var_value))
    return var_value


def get_src_files(mk_file, sdk_root, proj_dir):
    start_src_re = re.compile('^\s*SRC_FILES\s*\+=.*')
    src_file_re = re.compile('^\s*(\S+)\s*.*')
    start_found = False
    src_files = []

    for line in mk_file:
        if not start_found and start_src_re.match(line):
            start_found = True
        elif start_found:
            re_res = src_file_re.match(line)
            if re_res:
                src_files += [re_res.group(1).replace('$(', '{').replace(')', '}')]
            else:
                break
    else:
        sys.exit('SRC_FILES variable was not found!')

    print('SRC_FILES = ')
    for i in range(len(src_files)):
        src_files[i] = src_files[i].format(SDK_ROOT=sdk_root, PROJ_DIR=proj_dir)
        print('  %s' % src_files[i])

    return src_files


def get_inc_dirs(mk_file, sdk_root, proj_dir):
    start_inc_re = re.compile('^\s*INC_FOLDERS\s*\+=.*')
    inc_dir_re = re.compile('^\s*(\S+)\s*.*')
    start_found = False
    inc_dirs = []

    for line in mk_file:
        if not start_found and start_inc_re.match(line):
            start_found = True
        elif start_found:
            re_res = inc_dir_re.match(line)
            if re_res:
                inc_dirs += [re_res.group(1).replace('$(', '{').replace(')', '}')]
            else:
                break
    else:
        sys.exit('INC_FOLDERS variable was not found!')

    print('INC_FOLDERS = ')
    for i in range(len(inc_dirs)):
        inc_dirs[i] = inc_dirs[i].format(SDK_ROOT=sdk_root, PROJ_DIR=proj_dir)
        print('  %s' % inc_dirs[i])

    return inc_dirs


def get_defines(mk_file):
    define_re = re.compile('(^.*CFLAGS\s*\+=\s*-D)(\S*)')
    defines = []

    for line in mk_file:
        re_res = define_re.match(line)
        if re_res:
            defines += [re_res.group(2).replace('=', ' ')]

    print('DEFINES = ')
    for d in defines:
        print('  %s' % d)

    return defines


def save_project(mk_dir, proj_name, src_files, inc_dirs, defines):
    # proj.creator file
    proj_creator_path = os.path.join(mk_dir, proj_name + '.creator')
    with open(proj_creator_path, 'w') as file:
        file.write('[General]\n\n')
    print('%s file created' % proj_creator_path)

    # proj.files file
    proj_files = os.path.join(mk_dir, proj_name + '.files')
    with open(proj_files, 'w') as file:
        for line in src_files:
            file.write('%s\n' % line)
    print('%s file created' % proj_files)

    # proj.includes file
    proj_includes = os.path.join(mk_dir, proj_name + '.includes')
    with open(proj_includes, 'w') as file:
        for line in inc_dirs:
            file.write('%s\n' % line)
    print('%s file created' % proj_includes)

    # proj.config file
    proj_config = os.path.join(mk_dir, proj_name + '.config')
    with open(proj_config, 'w') as file:
        for line in defines:
            file.write('#define %s\n' % line)
    print('%s file created' % proj_config)


if __name__ == '__main__':
    mk_file, mk_dir = load_makefile()
    proj_name = get_var(mk_file, 'PROJECT_NAME')
    sdk_root = get_var(mk_file, 'SDK_ROOT')
    proj_dir = get_var(mk_file, 'PROJ_DIR')
    src_files = get_src_files(mk_file, sdk_root, proj_dir)
    inc_dirs = get_inc_dirs(mk_file, sdk_root, proj_dir)
    defines = get_defines(mk_file)
    save_project(mk_dir=mk_dir,
                 proj_name=proj_name,
                 src_files=src_files,
                 inc_dirs=inc_dirs,
                 defines=defines)
