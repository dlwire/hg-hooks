from lettuce import *
from shutil import rmtree

@before.all
def setup():
    world.cloned_repo_name = 'local-repo'
    world.web_served_repo_name = 'web-served-repo'

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
