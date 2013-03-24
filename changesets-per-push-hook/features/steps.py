# -*- coding: utf-8 -*-
from lettuce import *
from os import path
from support import hg, hooks

@step(u'a web-served repository')
def given_a_web_served_repository(step):
    hg.initialize(world.web_served_repo_name)
    hg.start_webserver(world.web_served_repo_name)

@step(u'the changeset limiting hook')
def and_the_changset_limiting_hook(step):
    hg.add_hook(world.web_served_repo_name, 'pretxnchangegroup.limit-changesets-per-push = python:../limit-changesets-per-push.py:check_changeset_limit\n')

@step(u'a local clone')
def and_a_cloned_clone(step):
    hg.clone('http://localhost:8000', world.cloned_repo_name)
    assert hg.is_repository(world.cloned_repo_name), "Unable to clone webserver"

@step(u'I set the changesets per push limit to (\d)')
def when_i_set_changesets_per_push_limit(step, changeset_limit):
    with open('web-served-repo/.hg/.limit-changesets-per-push.config', 'w') as f:
        f.write(changeset_limit)
    
@step(u'I try to push (\d) changesets to the web-served repository')
def and_i_try_to_push_to_the_web_served_repository(step, changeset_count):
    hg.add_commits(world.cloned_repo_name, changeset_count)
    hg.push(world.cloned_repo_name)

@step(u'And I try to push 2 changesets to a named branch')
def and_i_try_to_push_2_changesets_to_a_named_branch(step):
    hg.create_a_branch(world.cloned_repo_name)
    hg.add_commits(world.cloned_repo_name, 2)
    hg.push(world.cloned_repo_name)
   
@step(u'my changesets are not accepted')
def then_my_changesets_are_not_accepted(step):
    hg.update_to_tip(world.web_served_repo_name)
    assert not any(path.isfile(world.web_served_repo_name + '/' + filename) for filename in world.files_in_push), "Some files were present"
   
@step(u'my changesets are accepted')
def then_my_changesets_are_accepted(step):
    hg.update_to_tip(world.web_served_repo_name)
    assert all(path.isfile(world.web_served_repo_name + '/' + filename) for filename in world.files_in_push), "Some files were missing"

