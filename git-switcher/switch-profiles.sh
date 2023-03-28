#!/bin/bash

profiles_dir="$HOME/GitProfiles"
profiles=("work" "personal")

echo "Select a Git profile:"
select profile in "${profiles[@]}"; do
    if [[ -n $profile ]]; then
        profile_file="$profiles_dir/$profile"
        git config --global include.path "$profile_file"
        echo "Switched to $profile"
        break
    else
        echo "Invalid selection"
    fi
done
