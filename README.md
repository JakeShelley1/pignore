# Pignore
Gitignore generator written in Python.

![](http://i.imgur.com/QmNzbhs.gif)

## Features
- Easy to [install](https://github.com/jakeshelley1/pignore#installation)
- Supports tons of [gitignore files](https://github.com/github/gitignore) by default
- [Save gitignores](https://github.com/jakeshelley1/pignore#usage) for later use
- Works anywhere you can use pip or easy_install

## Installation
`pip install pignore`
Run `pignore update` after installation to get default gitignores
## Usage
### Commands
```bash
   g | generate   generate a gitignore file
   u | update     update gitignore stored files
   s | save       save current directory gitignore file
   l | list       list all available gitignores
```

## Examples
### Update
```bash
$ pignore update
```
Updates gitignores from [Github's gitignore repo](https://github.com/github/gitignore)
### Basic Generate
```bash
$ pignore generate java
```
Generates a Java `.gitignore` file in current directory
### Append Multiple Gitignores
```bash
$ pignore generate java python swift
```
Generates appends Java, Python, and Swift `.gitignore` files to create a single `.gitignore` file in current directory

If there is already a `.gitignore` file in the current directory you will have the option to overwrite it or append to it
### Save
```bash
$ pignore save my_gitignore
```
Save `.gitignore` in current directory to provided file name. You can generate the `.gitignore` later using:
```bash
$ pignore generate my_gitignore
```
### List
```bash
pignore list
```
Lists gitignores provided from update and all saved gitignores

## Feature Requests
Feel free to request features and enhancements in the [issue tracker](https://github.com/JakeShelley1/pignore/issues)

## License
Pignore uses the [MIT License](https://github.com/JakeShelley1/pignore/blob/master/LICENSE.txt)
