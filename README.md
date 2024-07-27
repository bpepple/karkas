# Karkas

A small project to update a comic's Comic.xml Format element to the new values used by Metron

## Installation

```bash
pipx install karkas-1.1.0-py3-none-any.whl
```

## Purpose

Metron has recently consolidated the `Cancelled Series` and `Ongoing` formats to `Single Issue` and changes
`Annual Series` to `Annual`.

This program simply update's a comic's ComicInfo.xml file for these changes.

## Usage

Simply run the following:
```bash
karkas /path/to/comics
```
