# -*- coding: utf-8 -*-
from lettuce import *
from os import makedirs
from os import path
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
import os
from support import hooks

def add_commits(repository, changeset_count):
    for i in range(1, int(changeset_count)+1):
        add_a_commit(repository, 'change %d' % i)

def add_a_commit(repository, filename):
    call(['touch', filename], cwd=world.cloned_repo_name, stdout=PIPE)
    world.files_in_push.append(filename)
    call(['hg', 'add', filename], cwd=world.cloned_repo_name, stdout=PIPE)
    call(['hg', 'commit', '-m"%s"' % filename, '-u"user"'], cwd=world.cloned_repo_name, stdout=PIPE)

def update_to_tip(repository):
    call(['hg', 'update'], cwd=repository, stdout=PIPE)

def create_a_branch(repository):
    call(['hg', 'branch', 'named-branch'], cwd=repository, stdout=PIPE)

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
        f.write('pretxnchangegroup.limit-changesets-per-push = python:../limit-changesets-per-push.py:check_changeset_limit\n')

@step(u'a web-served repository')
def given_a_web_served_repository(step):
    initialize(world.web_served_repo_name)
    start_webserver(world.web_served_repo_name)

@step(u'the changeset limiting hook')
def and_the_changset_limiting_hook(step):
    add_hook(world.web_served_repo_name, 'pretxnchangegroup.limit-changesets-per-push = python:../limit-changesets-per-push.py:check_changeset_limit\n')

@step(u'a local clone')
def and_a_cloned_clone(step):
    clone('http://localhost:8000', world.cloned_repo_name)
    assert is_repository(world.cloned_repo_name), "Unable to clone webserver"

@step(u'I set the changesets per push limit to (\d)')
def when_i_set_changesets_per_push_limit(step, changeset_limit):
    with open('web-served-repo/.hg/.limit-changesets-per-push.config', 'w') as f:
        f.write(changeset_limit)
    
@step(u'I try to push (\d) changesets to the web-served repository')
def and_i_try_to_push_to_the_web_served_repository(step, changeset_count):
    add_commits(world.cloned_repo_name, changeset_count)
    push(world.cloned_repo_name)

@step(u'And I try to push 2 changesets to a named branch')
def and_i_try_to_push_2_changesets_to_a_named_branch(step):
    create_a_branch(world.cloned_repo_name)
    add_commits(world.cloned_repo_name, 2)
    push(world.cloned_repo_name)
   
@step(u'my changesets are not accepted')
def then_my_changesets_are_not_accepted(step):
    update_to_tip(world.web_served_repo_name)
    assert not any(path.isfile(world.web_served_repo_name + '/' + filename) for filename in world.files_in_push), "Some files were present"
   
@step(u'my changesets are accepted')
def then_my_changesets_are_accepted(step):
    update_to_tip(world.web_served_repo_name)
    assert all(path.isfile(world.web_served_repo_name + '/' + filename) for filename in world.files_in_push), "Some files were missing"

