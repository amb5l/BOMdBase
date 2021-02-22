import git

from django.shortcuts import render

from .shared import navbar1

def main(request):
    repo = git.Repo()
    tag = str(repo.tags[-1])
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=6)
    notes = 'Version: ' + tag + '('+ short_sha + ')'
    context = { \
        'navbar1': navbar1,
        'navbar2': [
            ('Backup/Export', '/backup'),
            ('Restore/Import', '/restore'),
            ('Admin', '/admin')
        ],
        'notes': notes
        }
    return render(request, 'base.html', context)