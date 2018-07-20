====
Tabs
====

Abstract
========
Tabs is a tool for quickly and easily opening and organising a new terminal
session with tabs already open at your desired modules.

Set up
======
Before you are able to use the functionality of Tabs, you will first have to
edit your *~/.mycshrc* file to have the following lines in:
    alias tabs /path/to/your/tabs/repo/tabs
    alias clone 'source /path/to/your/tabs/repo/clone'

Usage
=====
When you begin using Tabs you will not have any mapping to the modules on your
system. You can begin by running Tabs in *write* mode:
    tabs write --name/-n module_name --path/-p /path/to/modules/root
This will populate the mapping.
You can then run Tabs in *open* mode, like so:
    tabs open --module/-m module_1 module_2.....
or list whats available:
    tabs open --list/-l
or open everything:
    tabs open --all/-a

To automatically update the mapping everytime you check out a new repo, there
is the *clone* function, which is run in the same way as git clone:
    clone ssh://some/git/repo.git repo_name
If you don't supply it with the *repo_name* it will automatically use the git
repo file name. Oh, and it also sets the Terminal title and cd's into the repo
directory for you. That's nice isn't it.

