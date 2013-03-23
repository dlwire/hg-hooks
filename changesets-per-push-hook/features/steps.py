# -*- coding: utf-8 -*-
from lettuce import *
from os import makedirs
from os import path
from shutil import rmtree
from subprocess import call
from subprocess import Popen
from subprocess import PIPE

@before.each_scenario
def setup(scenario):
    world.files_in_push = []

@after.each_scenario
def teardown(scenario):
    if world.process is not None:
        world.process.kill()
        world.process = None

    rmtree('web-served-repo')
    rmtree('local-repo')
        
@step(u'a web-served repository')
def given_a_web_served_repository(step):
    makedirs('web-served-repo')
    call(['hg', 'init'], cwd='web-served-repo')

    with open('web-served-repo/.hg/hgrc', 'w') as f:
        f.write('[web]\n')
        f.write('allow_push=*\n')
        f.write('push_ssl=false\n')

    world.process = Popen(['hg', 'serve', '-a', 'localhost'], cwd='web-served-repo', stdout=PIPE, stderr=PIPE)

    assert world.process is not None, "Unable to start webserver"

@step(u'the changeset limiting hook')
def and_the_changset_limiting_hook(step):
    with open('web-served-repo/.hg/hgrc', 'a') as f:
        f.write('\n')
        f.write('[hooks]\n')
        f.write('pretxnchangegroup.limit-changesets-per-push = python:../limit-changesets-per-push.py:check_changeset_limit\n')

@step(u'a local clone')
def and_a_local_clone(step):
    call(['hg', 'clone', 'http://localhost:8000', 'local-repo'], stdout=PIPE)

    assert path.isdir('local-repo/.hg'), "Unable to clone webserver"

@step(u'I set the changesets per push limit to (\d)')
def when_i_set_changesets_per_push_limit(step, changeset_limit):
    pass
    
@step(u'I try to push (\d) changesets to the web-served repository')
def and_i_try_to_push_to_the_web_served_repository(step, changeset_count):
    for i in range(1, int(changeset_count)+2):
        call(['touch', 'temp %d' % i], cwd='local-repo', stdout=PIPE)
        world.files_in_push.append('temp %d' % i)
        call(['hg', 'add', 'temp %d' % i], cwd='local-repo', stdout=PIPE)
        call(['hg', 'commit', '-m"message %d"' % i, '-u"user"'], cwd='local-repo', stdout=PIPE)

    call(['hg', 'push'], cwd='local-repo', stdout=PIPE)
   
@step(u'my changesets are not accepted')
def then_my_changesets_are_not_accepted(step):
    call(['hg', 'update'], cwd='web-served-repo', stdout=PIPE)
    assert not any(path.isfile('web-served-repo/' + filename) for filename in world.files_in_push), "Some files were present"
   
@step(u'my changesets are accepted')
def then_my_changesets_are_accepted(step):
    call(['hg', 'update'], cwd='web-served-repo', stdout=PIPE)
    assert all(path.isfile('web-served-repo/' + filename) for filename in world.files_in_push), "Some files were missing"

