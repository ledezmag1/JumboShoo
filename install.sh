#!/usr/bin/env bash

jumboshoo_git_dir="$HOME/dev/jumboshoo/JumboShoo"

# Create directory structure
if [ ! -d "$jumboshoo_git_dir" ];
then
    mkdir -p "$jumboshoo_git_dir"
fi

cd "$jumboshoo_git_dir"

pip install -r requirements.txt

echo "Creating symbolic link from $supportdir/estts.service to /etc/systemd/system/"
ln -s "$jumboshoo_git_dir/service/jumboshoo.service" /etc/systemd/system/ || {
    echo "Failed to create symbolic link from $jumboshoo_git_dir/service/jumboshoo.service to /etc/systemd/system/"
    exit 1
}

