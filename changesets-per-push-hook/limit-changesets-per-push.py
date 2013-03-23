import sys
sys.path.append("/Library/Python/2.7/site-packages/")

from mercurial import util

def get_incoming_changesets(repo, node):
    """ Method to get the changesets in the repo coming in this push, stolen from the webs"""
    return [repo[rev] for rev in xrange(repo[node].rev(), len(repo))]

def get_changeset_limit(repo_root_dir):
    with open(repo_root_dir + '/.hg/.limit-changesets-per-push.config') as f:
        return int(f.read())
    return 0

def is_set_to_no_limit(changeset_limit):
    return changeset_limit is 0

def check_changeset_limit(ui, repo, node=None, **kwargs):
    print('Running changeset limit hook')
    
    changeset_limit = get_changeset_limit(repo.root)
    if is_set_to_no_limit(changeset_limit):
        return;

    incoming_changesets = len(get_incoming_changesets(repo, node))
    if changeset_limit < incoming_changesets:
        raise util.Abort('You tried to push %d changesets, the limit for this repository is %d! Please compress your changes and push again' % (incoming_changesets, changeset_limit))

