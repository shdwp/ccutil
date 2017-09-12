import git

from utils import verbose

COMMIT_SEARCH_LIMIT = 50
r = None

def open_repo(path):
    global r
    r = git.Repo(path)
    return r

def feature_base(at_ref):
    for commit in r.iter_commits(r.branches["develop"], max_count=COMMIT_SEARCH_LIMIT):
        if commit in r.iter_commits(at_ref, max_count=COMMIT_SEARCH_LIMIT):
            verbose("{} based at {} in develop", at_ref, commit)
            return commit

def feature_files_changed(ref):
    result = []
    base = feature_base(ref)

    if not base:
        print("Can't find base commit for {}!", ref)
        return None

    for c in r.iter_commits(ref, max_count=COMMIT_SEARCH_LIMIT):
        if c == base:
            break
        else:
            verbose("Adding changes from {}", c)
            result += c.stats.files.keys()

    return result

def features_conflicts(ref1, ref2):
    verbose("Finding conflicts between {}", ref1)
    ref1_changes = feature_files_changed(ref1)
    verbose("")
    verbose("And {}", ref2)

    if ref2 == r.branches["develop"]:
        ref1_base = feature_base(ref1)
        ref2_changes = []
        for c in r.iter_commits(r.branches["develop"], max_count=COMMIT_SEARCH_LIMIT):
            if c == ref1_base:
                break
            else:
                verbose("Adding changes from {}", c)
                ref2_changes += c.stats.files.keys()
    else:
        ref2_changes = feature_files_changed(ref2)

    verbose("")
    for path in ref1_changes:
        verbose("{} changed {}", ref1, path)
    for path in ref2_changes:
        verbose("{} changed {}", ref2, path)

    return set(ref1_changes).intersection(set(ref2_changes))

def reverts_list():
    based_on = feature_base(r.head)

    head_files = list(map(lambda x: x.b_path, based_on.diff(r.head.commit)))
    working_files = list(map(lambda x: x.b_path, based_on.diff(None)))
    verbose("{} total edits from HEAD, {} from working tree", len(head_files), len(working_files))

    result = []
    for file in head_files:
        if file not in working_files:
            result.append(file)

    return result

def conflicts_list(branch):
    if branch and branch != "develop":
        ref2 = r.branches[branch]
    else:
        ref2 = r.branches["develop"]
        current_base = feature_base(r.head)
        ahead_count = 0
        for c in r.iter_commits(r.branches["develop"], max_count=COMMIT_SEARCH_LIMIT):
            if c == current_base:
                break
            else:
                ahead_count += 1
        print("Develop is {} commits ahead of current branch".format(ahead_count))

    return features_conflicts(r.head, ref2)
