import pkg_resources
import os

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["\t%s==%s" % (i.key, i.version) for i in installed_packages])

print('Installed packages:')

for pkg in installed_packages_list:
    print(pkg)

print('\n')
print('Files:')


def list_files(start_path):
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(sub_indent, f))


list_files(os.getcwd())
