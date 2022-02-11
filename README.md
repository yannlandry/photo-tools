# Photo Tools

Various scripts that I use to manage my photo library: synchronize backups, remove unedited photos, prepare images for web viewing.

**Disclaimer:** Not responsible for the loss and/or corruption of files; use at your own risk.

## `backup.py`

A safe wrapper around `rsync` that copies new and updated files from a source to a destination.

## `clean.py`

A tool that removes any RAW file (those that have a specific, configurable, extension) that doesn't have any other editing artifacts (XMP sidecar, DNG, PSD, TIF, etc.) in the same repository. Very useful when XMP sidecars are enabled in Lightroom.
