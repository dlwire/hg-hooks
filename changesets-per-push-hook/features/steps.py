# -*- coding: utf-8 -*-
from lettuce import *
from os import makedirs
from os import path
from shutil import rmtree
from subprocess import call
from subprocess import Popen
from subprocess import PIPE

@after.each_scenario
def stop_webserver(scenario):
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

    world.process = Popen(['hg', 'serve', '-a', 'localhost'], cwd='web-served-repo', stdout=PIPE)

@step(u'the changeset limiting hook')
def and_the_changset_limiting_hook(step):
    pass

@step(u'a local clone')
def and_a_local_clone(step):
    call(['hg', 'clone', 'http://localhost:8000', 'local-repo'], stdout=PIPE)

@step(u'I set the changesets per push limit to (\d)')
def when_i_set_changesets_per_push_limit(step, changeset_limit):
    pass
    
@step(u'I try to push (\d) changesets to the web-served repository')
def and_i_try_to_push_to_the_web_served_repository(step, changeset_count):
    call(['touch', 'temp'], cwd='local-repo', stdout=PIPE)
    call(['hg', 'add', 'temp'], cwd='local-repo', stdout=PIPE)
    call(['hg', 'commit', '-m"message"', '-u"user"'], cwd='local-repo', stdout=PIPE)
    call(['hg', 'push'], cwd='local-repo', stdout=PIPE)
   
@step(u'my changesets are not accepted')
def then_my_changesets_are_not_accepted(step):
    call(['hg', 'update'], cwd='web-served-repo', stdout=PIPE)
    assert not path.isfile('web-served-repo/temp'), "File web-served-repo/temp exists"
   
@step(u'my changesets are accepted')
def then_my_changesets_are_accepted(step):
    call(['hg', 'update'], cwd='web-served-repo', stdout=PIPE)
    assert path.isfile('web-served-repo/temp'), "File web-served-repo/temp doesn't exist"

