from subprocess import call, PIPE, Popen, STDOUT
from lettuce import world
from os import makedirs, path
from urllib2 import urlopen, URLError

def add_a_commit(repository, file='filename', user='User', branch='default', comment='comment'):
    create_a_branch(repository, branch)
    call(['touch', file], cwd=repository, stdout=PIPE)
    world.files_in_push.append(file)
    call(['hg', 'add', file], cwd=repository, stdout=PIPE)
    call(['hg', 'commit', '-m"%s"' % comment, '-u"%s"' % user], cwd=repository, stdout=PIPE)

def update_to_tip(repository):
    call(['hg', 'update'], cwd=repository, stdout=PIPE)

def create_a_branch(repository, branch):
    call(['hg', 'branch', branch], cwd=repository, stdout=PIPE)

def push(repository):
    call(['hg', 'push'], cwd=repository, stdout=PIPE)

def initialize(repository):
    makedirs(repository)
    call(['hg', 'init'], cwd=repository)

def start_webserver(repository):
    with open(repository + '/.hg/hgrc', 'w') as f:
        f.write('[web]\n')
        f.write('allow_push=*\n')
        f.write('push_ssl=false\n')
    world.process = Popen(['hg', 'serve', '-a', 'localhost'], cwd=repository, stdout=PIPE, stderr=PIPE)

    assert world.process is not None, "Unable to start webserver"

def clone(source_url, destination):
    while 0 is not call(['hg', 'clone', source_url, destination], stdout=PIPE):
        pass

def is_repository(dir):
    return path.isdir(dir + '/.hg')
                                                                                                        
def add_hook(repository, hook):
    with open(repository + '/.hg/hgrc', 'a') as f:
        f.write('\n')
        f.write('[hooks]\n')
        f.write(hook)

if __name__ is "__main__":
    pass
