from mercurial import util

class Repository(object):
    def __init__(self, repo, node):
        self.repo = repo
        self.node = node

    def get_changesets_on_branch(self, branch):
        return [changeset for changeset in self.get_changesets() if changeset.branch() is branch]

    def get_changesets(self):
        return [self.repo[rev] for rev in xrange(self.repo[self.node].rev(), len(self.repo))]

    def get_root_directory(self):
        return self.repo.root
#
def get_changeset_limit(repo_root_dir):
    with open(repo_root_dir + '/.hg/.limit-changesets-per-push.config') as f:
        return int(f.read())
    return 0

def is_set_to_no_limit(changeset_limit):
    return changeset_limit is 0

def check_changeset_limit(ui, repo, node=None, **kwargs):
    print('Running changeset limit hook')

    hg = Repository(repo, node)
    
    changeset_limit = get_changeset_limit(hg.get_root_directory())
    if is_set_to_no_limit(changeset_limit):
        return;

    incoming_changesets = len(hg.get_changesets_on_branch('default'))
    if changeset_limit < incoming_changesets:
        raise util.Abort('You tried to push %d changesets, the limit for this repository is %d! Please compress your changes and push again' % (incoming_changesets, changeset_limit))


