# Karkas

A small project to update a comic's Comic.xml Format element to the new values used by Metron

## Installation

```bash
pipx install karkas-1.0.0-py3-none-any.whl
```

## Purpose

Metron has recently consolidated the `Cancelled Series` and `Ongoing` formats to `Single Issue`.
This program simple update's the comic's ComicInfo.xml file for the change.

## Usage

Simply run the following:
```bash
karkas /path/to/comics
```
