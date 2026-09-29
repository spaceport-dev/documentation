#!/usr/bin/env python3
"""Fetch an explicit documentation revision without creating a Git repository."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import tarfile
import tempfile
import urllib.request


def digest(data):
    return hashlib.sha256(data).hexdigest()


def install(revision, destination, archive=None):
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Use a full 40-character Git commit SHA for --revision')
    destination = Path(destination).absolute()
    if destination.is_symlink():
        raise ValueError('Refusing to replace a symlink destination')
    preserved = {}
    if destination.exists():
        record = destination / '.spaceport-docs.json'
        previous = json.loads(record.read_text())['files'] if record.exists() else {}
        for item in destination.iterdir():
            if item.is_symlink() or not item.is_file():
                raise ValueError('Refusing unmanaged path: ' + str(item))
            if item.name in ('README.md', '.gitignore'):
                preserved[item.name] = item.read_bytes()
            elif item.name == '.spaceport-docs.json':
                continue
            elif item.name not in previous:
                raise ValueError('Refusing unmanaged file: ' + str(item))
            elif digest(item.read_bytes()) != previous[item.name]:
                raise ValueError('Refusing locally modified documentation: ' + str(item))
    if archive:
        data = Path(archive).read_bytes()
    else:
        url = 'https://codeload.github.com/spaceport-dev/documentation/tar.gz/' + revision
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
        for item in tar:
            parts = item.name.split('/')
            if len(parts) == 3 and parts[1] == 'documentation' and item.isfile():
                name = parts[2]
                if not re.fullmatch(r'[a-z0-9_][a-z0-9_-]*\.md', name):
                    raise ValueError('Invalid documentation filename: ' + name)
                if name in files:
                    raise ValueError('Duplicate documentation filename: ' + name)
                content = tar.extractfile(item).read()
                content.decode('utf-8')
                files[name] = content
    if not {'_index.md', '_toc.md'} <= files.keys():
        raise ValueError('Archive is missing documentation index or table of contents')
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.spaceport-docs-', dir=destination.parent))
    backup = staging.with_name(staging.name + '-previous')
    try:
        for name, data in {**files, **preserved}.items():
            (staging / name).write_bytes(data)
        record = {'repository': 'spaceport-dev/documentation', 'revision': revision,
                  'files': {name: digest(data) for name, data in files.items()}}
        (staging / '.spaceport-docs.json').write_text(json.dumps(record, indent=2) + '\n')
        if destination.exists():
            destination.rename(backup)
        try:
            staging.rename(destination)
        except BaseException:
            if backup.exists(): backup.rename(destination)
            raise
        if backup.exists(): shutil.rmtree(backup)
    finally:
        if staging.exists(): shutil.rmtree(staging)
    print(f'Fetched {len(files)} documents at {revision} into {destination}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--destination', default='documentation')
    parser.add_argument('--archive', help='Use a trusted local GitHub-format archive (offline use)')
    args = parser.parse_args()
    try:
        install(args.revision, args.destination, args.archive)
    except Exception as error:
        parser.exit(1, f'Documentation fetch failed: {error}\n')
