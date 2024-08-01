# Karkas

A small project to update a comic's Comic.xml Format element to the new values used by Metron

## Installation

```bash
pipx install karkas-1.2.0-py3-none-any.whl
```

## Purpose

Metron has recently made some changes to it's `Series Types` and this program simply update's a comic's ComicInfo.xml 
file for these changes. These changes are as follows:
- Change `Cancelled Series` and `Ongoing` to `Single Issue`
- Change `Annual Series` to `Annual`
- Change `Hard Cover` to `Hardcover`
- Change `Digital Chapters` to `Digital Chapter`

## Usage

Simply run the following:
```bash
karkas /path/to/comics
```
