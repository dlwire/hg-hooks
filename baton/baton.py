import os
from mercurial import util

def filter_baton_comment(changeset):
    return 'BATON' in changeset.description()
    
def filter_on_default(changeset):
    return changeset.branch() == 'default'

def get_incoming_changesets(repo, node):
    return [repo[revNum] for revNum in xrange(repo[node], len(repo))]

def execute_hook(ui, repo, node=None, **kwargs):
    print('Executing baton hook')

    incoming_changesets = get_incoming_changesets(repo, node)
    on_default = filter(filter_on_default, incoming_changesets)

    if len(on_default) == 0:
        print('  No changesets on default branch, accepting changes')
        return False

    with_baton_comment = filter(filter_baton_comment, on_default)
    if len(with_baton_comment) == 0:
        raise util.Abort('  Changesets on default and no "BATON" comment\n  Rejected Push!!\n\nMake sure you have the baton before you push')

    print('  Passed baton hook, accepting changes')
        
    return False
