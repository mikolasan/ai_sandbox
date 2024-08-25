project('malstrom', 'cpp',
    version: '0.1.0',
    default_options: [
        'warning_level=3',
        'cpp_std=c++17',
        'buildtype=debug',
        'optimization=g'
    ])

# liblua_dep = dependency('lua5.3')
# libpython_dep = dependency('python2.7')
# libdl_dep = dependency('dl')

cpp_args = [
]

#subdir('deps')

malstrom_src = [
    'src/main.cpp',
]
malstrom_inc = include_directories(
    'thirdparty',
)
#malstrom_dep = [
#]

executable('malstrom', malstrom_src,
    include_directories: malstrom_inc,
    cpp_args: cpp_args,
    #link_args: malstrom_link_args,
    #dependencies: malstrom_dep,
    #install : true,
    #install_dir : '.',
)
