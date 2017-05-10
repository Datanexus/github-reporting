#!/usr/bin/env python -u

__copyright__ = '(c) 2016 DataNexus Inc.  All Rights Reserved.'
__license__ = 'APLv2.0'
__author__ = 'ckeller@datanexus.org'

class Developer:
    """class that holds the developer commit information"""
    def __init__(self, name, login, email, additions, deletions):
        self.name = name
        self.login = login
        self.email = email
        self.commits = 1
        self.additions = additions
        self.deletions = deletions
    
    def setName(self, name):
        self.name = name
    
    def setLogin(self, login):
        self.login = login
        
    def setEmail(self, email):
        self.email = email
    
    def incrementChanges(self, additions, deletions):
        self.commits = self.commits + 1
        self.additions = self.additions + additions
        self.deletions = self.deletions + deletions    
            
    def display(self, manager, project):
        """display CSV or standard"""
        if manager:
            print "{},{},{},{},{},{}".format(project, self.login, self.name, self.commits, self.additions, self.deletions)
        else:
            print "\t{} ({}): {} commits {} additions {} deletions".format(self.login, self.name, self.commits, self.additions, self.deletions)
            
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
    counter = 0
    people = {}
    for commit in repo.get_commits():
        # just in case all the user data isn't fully populated (should only happen in enterprise GitHub)
        if commit.author is None:
            author='unassigned'
            login='s0'
            email='noone@iag.com.au'
        else:
            author = commit.author.name
        
            if commit.committer is None:
                login = commit.author.login
            else:
                login = commit.committer.login
            
            if commit.author.email is None:
                email='noone@iag.com.au'
            else:
                email=commit.author.email
   
        # create new developer commit object
        x = Developer(author, login, email, commit.stats.additions, commit.stats.deletions)
        
        # either add it to the hash or update existing    
        if x in people:
            people[x].incrementChanges(commit.stats.additions, commit.stats.deletions)
        else:
            people[x] = x
        counter += 1
    
    # standard display routine    
    if not args.manager:    
        print "{}: {} commits".format(repo.full_name, counter)
    for k in sorted(people):
        k.display(args.manager, repo.full_name)
                    
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
        print "# repo, login, name, commits, additions, deletions"

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