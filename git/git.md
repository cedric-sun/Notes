Git Note
================================

## Initialize
`git init`

## Configure Identifier
**Only for the current repository**  
`git config user.email 'email address'`

**Globally**  
`git config global user.email 'email address'`

## Diff
**Workspace and Stage(Index)**  
`git diff`

**Stage(Index) and Repository**  
`git diff --staged` or `git diff --cached`

**Workspace and Repository**  
`git diff HEAD`

## Commit operation
### Show History Commits
`git log [--pretty=oneline] [--graph]`

### Backtrack to certain commit (with clean working directory)
`git reset --hard {HEAD^ | HEAD^^... | HEAD~back_cnt | Commit_ID}`

### Backtrack to certain commit (with all changes staged)
`git reset --soft {HEAD^ | HEAD^^... | HEAD~back_cnt | Commit_ID}`

### Backtrack to certain commit (with all changes unstaged)
`git reset {HEAD^ | HEAD^^... | HEAD~back_cnt | Commit_ID}`

## Show History Instructives
`git reflog`

## Revert Workspace Changes
`git checkout -- filename`

## Revert Staged Changes
`git reset HEAD filename`

## Create a New Branch
`git branch my_new_branch`

## Switch HEAD to Other Branch
`git checkout my_new_branch`

## Create a New Branch Meanwhile Switch to it
`git checkout -b my_new_branch`

## Show All Branches and the Current One
`git branch`

## Automerge
`git merge branch_to_merge`

## Delete Branch
`git branch -d branch_to_delete`

## Cancel commit
### `
