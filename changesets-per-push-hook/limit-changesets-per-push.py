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

class ChangesetLimitCheck(object):
    def __init__(self, repository):
        self.changesets = len(repository.get_changesets_on_branch('default'))
        self.limit = self.read_changeset_limit(repository.get_root_directory())

    def execute(self):
        if self.is_set_to_no_limit():
            return

        if self.limit < self.changesets:
            raise util.Abort('You tried to push %d changesets\n' \
                             '  The limit for this repository is %d!\n' \
                             'Please compress your changes and push again' % (self.changesets, self.limit))

    def read_changeset_limit(self, root):
        with open(root + '/.hg/.limit-changesets-per-push.config') as f:
            return int(f.read())
        return 0

    def is_set_to_no_limit(self):
        return self.limit is 0


def is_set_to_no_limit(changeset_limit):
    return changeset_limit is 0

def check_changeset_limit(ui, repo, node=None, **kwargs):
    print('Running changeset limit hook')

    hg = Repository(repo, node)
    hook = ChangesetLimitCheck(hg)

    hook.execute()
   
