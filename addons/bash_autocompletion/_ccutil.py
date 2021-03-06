_ccutilpy_completion() 
{
    local prev opts
    COMPREPLY=('c' 'conflict' 'r' 'revert' 'up' 'update' '--always-open-browser' '--browser' '--reverts' '--commit' '--dry-run' '-h' '-b' '-c' '-v' '-q' '-a' '-r', '-i')
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [[ ${prev} == "-b" ]] ; then
        COMPREPLY=($(git branch | grep -v \* | sed -e 's/ //g'))
        return 0
    fi

    if [[ ${prev} == "-c" ]] ; then
        COMPREPLY=($(git branch | grep -v \* | sed -e 's/ //g'))
        return 0
    fi

    if [[ ${prev} == "up" ]] ; then
        COMPREPLY=('auto' 'manual' 'id' 'setid' 'reset' 'browse')
        return 0
    fi
}
complete -F _ccutilpy_completion ccutil.py
