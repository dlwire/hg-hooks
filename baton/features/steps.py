# -*- coding: utf-8 -*-
from lettuce import *
from os import path
from support import hg, hooks

@step(u'a web-served repository')
def given_a_web_served_repository(step):
    hg.initialize(world.web_served_repo_name)
    hg.start_webserver(world.web_served_repo_name)

@step(u'the baton hook')
def add_baton_hook(step):
    hg.add_hook(world.web_served_repo_name, 'pretxnchangegroup.baton = python:../baton.py:execute_hook\n')

@step(u'a local clone$')
def and_a_cloned_clone(step):
    hg.clone('http://localhost:8000', world.cloned_repo_name)
    assert hg.is_repository(world.cloned_repo_name), "Unable to clone webserver"

@step(u'I push without the comment \'BATON\'$')
def i_push(step):
    hg.add_a_commit(world.cloned_repo_name)
    hg.push(world.cloned_repo_name)

@step(u'I push with the comment \'([^\']*)\'$')
def i_push_with_the_comment(step, group1):
    hg.add_a_commit(world.cloned_repo_name, comment=group1)
    hg.push(world.cloned_repo_name)

@step(u'I push without the comment \'BATON\' to a named branch$')
def i_push_to_a_named_branch(step):
    hg.add_a_commit(world.cloned_repo_name, branch='named_branch')
    hg.push(world.cloned_repo_name)
 
@step(u'my changesets are not accepted$')
def then_my_changesets_are_not_accepted(step):
    hg.update_to_tip(world.web_served_repo_name)
    assert not any(path.isfile(world.web_served_repo_name + '/' + filename) for filename in world.files_in_push), "Some files were present"
   
@step(u'my changesets are accepted$')
def then_my_changesets_are_accepted(step):
    hg.update_to_tip(world.web_served_repo_name)
    assert all(path.isfile(world.web_served_repo_name + '/' + filename) for filename in world.files_in_push), "Some files were missing"

