import sys
sys.path.append("/Library/Python/2.7/site-packages/")

from mercurial import util as hg

def check_changeset_limit(ui, repo, node=None, **kwargs):
    print('Running changeset limit hook. Limit is set to 2')
