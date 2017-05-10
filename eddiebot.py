#!/usr/bin/env python -u

__copyright__ = '(c) 2016 DataNexus Inc.  All Rights Reserved.'
__license__ = 'APLv2.0'
__author__ = 'ckeller@datanexus.org'

class Developer:
    """class that holds the developer commit information"""
    def __init__(self, name, login, email, additions, deletions, merge):
        self.name = name
        self.login = login
        self.email = email
        if merge:
            self.prs = 1
            self.commits = 0
            self.additions = 0
            self.deletions = 0
        else:
            self.prs = 0
            self.commits = 1
            self.additions = additions
            self.deletions = deletions
    
    def setName(self, name):
        self.name = name
    
    def setLogin(self, login):
        self.login = login
        
    def setEmail(self, email):
        self.email = email
    
    def incrementPR(self):
        self.pr = self.pr + 1
        
    def incrementChanges(self, additions, deletions, merge):
        if merge:
            # don't add the counts for merges so you don't get double credit for self-merging
            self.prs = self.prs + 1
        else:
            self.commits = self.commits + 1
            self.additions = self.additions + additions
            self.deletions = self.deletions + deletions    
            
    def display(self, manager, project):
        """display CSV or standard"""
        if manager:
            print "{},{},{},{},{},{},{}".format(project, self.login, self.name, self.commits, self.prs, self.additions, self.deletions)
        else:
            print "\t{} ({}): {} commits {} merges {} additions {} deletions".format(self.login, self.name, self.commits, self.prs, self.additions, self.deletions)
            
    def __hash__(self):
        return hash((self.login))
    
    def __eq__(self, other):
        return (self.login) == (other.login)
    
    def __ne__(self, other):
        return not(self == other)
    
    def __cmp__(self, other):
        """highest commits first ordering"""
        return cmp(other.commits, self.commits)


def processCommits(repo, args):
    from github import GithubException
    
    counter = 0
    people = {}

    try:
        for commit in repo.get_commits():
            merge = False
            # just in case all the user data isn't fully populated (should only happen in enterprise GitHub)
            if commit.author is None:
                name='nobody'
            else:
                name = commit.author.name
            
            if commit.committer is None:
                login = 's0'
            else:
                login = commit.committer.login
                
            if commit.committer is None:
                # commit is a PR merge
                merge = True
                # wierd case of bad data
                if commit.author is None:
                    login = 's0'
                else:
                    login = commit.author.login
        
            if commit.author is None or commit.author.email is None:
                email='noone@iag.com.au'
            else:
                email=commit.author.email
   
            # create new developer commit object            
            x = Developer(name, login, email, commit.stats.additions, commit.stats.deletions, merge)
        
            # either add it to the hash or update existing    
            if x in people:
                people[x].incrementChanges(commit.stats.additions, commit.stats.deletions, merge)
            else:
                people[x] = x
            counter += 1
    
        # standard display routine    
        if not args.manager:    
            print "{}: {} commits".format(repo.full_name, counter)
        for k in sorted(people):
            k.display(args.manager, repo.full_name)
    # repos with 0 commits generate an exception which we can safely ignore
    except GithubException as e:
        print "caught exception {}".format(e)
                    
def main():
    """main routine"""
    import argparse
    import sys
    from github import Github

    parser = argparse.ArgumentParser(description='GitHub Commit Reporting')
    parser.add_argument('--list-repos', action='store_true', help='list all repos viewable to token')
    parser.add_argument('--manager', action='store_true', help='change output to CSV for managers')
    parser.add_argument('--repo', dest='repo', help='limit to specific repo')
    parser.add_argument('endpoint', metavar='endpoint', help='GitHub API endpoint')
    parser.add_argument('token', metavar='token', help='GitHub API token')
    args = parser.parse_args()
        
    # First create a Github instance:
    g = Github(login_or_token=args.token, base_url=args.endpoint)

    # every data file needs a header
    if args.manager:
        print "# repo, login, name, commits, merges, additions, deletions"

    if args.list_repos:
        for repo in g.get_repos():
            print repo.full_name
        sys.exit(0)
    
    if args.repo:
        processCommits(g.get_repo(args.repo), args)
        sys.exit(0)
  
    # brute force walk every commit in every repo accessible
    for repo in g.get_repos():
        processCommits(repo, args)
if __name__ == '__main__':
    main()
