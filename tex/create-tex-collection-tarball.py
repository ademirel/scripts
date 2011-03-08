#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Download collection, parse TLPOBJ files and creates tarball for pisi files
Collections are disjoint, that means no collections conflicts with another
"""

import os
import sys
import commands
import shutil

# List of mirrors are: http://www.ctan.org/tex-archive/CTAN.sites

# TeXLive collections in the texlive-core package:
# (corresponds to the "medium scheme" of TeX Live)
core_collections = [ "basic",
                     "context",
                     "genericrecommended",
                     "fontsrecommended",
                     "langczechslovak",
                     "langdutch",
                     "langfrench",
                     "langgerman",
                     "langitalian",
                     "langpolish",
                     "langportuguese",
                     "langspanish",
                     "langenglish",
                     "latex",
                     "latex3",
                     "latexrecommended",
                     "luatex",
                     "mathextra",
                     "metapost",
                     "texinfo",
                     "xetex"]

core_collections.extend(["langhungarian", "langlithuanian"])

other_collections = [ "bibtexextra",
                      "fontsextra",
                      "formatsextra",
                      "games",
                      "genericextra",
                      "htmlxml",
                      "humanities",
                      "langcjk",
                      "langcyrillic",
                      "langgreek",
                      "latexextra",
                      "music",
                      "pictures",
                      "plainextra",
                      "pstricks",
                      "publishers",
                      "science"]

def download_module(module_names, collection=False):
    # Download modules
    mirror = "http://mirror.informatik.uni-mannheim.de/pub/mirrors/tex-archive/systems/texlive/tlnet/archive/"

    for module in module_names:
        if collection:
            module = "collection-" + module
        os.system("wget %s%s.tar.xz" % (mirror, module))

def extract_lxma(module=False):
    # Extract all compressed packages, for future use
    if not module:
        for collection in os.listdir("."):
            if collection.endswith("tar.xz"):
                os.system("tar Jxf %s" % collection)
    else:
        os.system("tar Jxf %s.tar.xz" % module)




def extract_module(collection_name):
    # Extract module information from the collection tarballs

    # Remove .tar.xz extension, we could also use os.path.splitext()
    collection_name = collection_name[:-7]

    module_names = []
    for line in open("tlpkg/tlpobj/%s.tlpobj" % collection_name, "r").readlines():
        if "depend" in line:
            line = line.strip().split(" ")
            if not line[1].startswith("collection") and not line[1].startswith("hyphen"):
                module_names.append(line[1])
        elif "revision" in line:
            line = line.strip().split(" ")
            revision = line[1]

    return (module_names, revision)

def collection_with_runfiles_pattern(collection_name):
    runfiles = []
    runfiles_found = False
    for line in open("tlpkg/tlpobj/%s.tlpobj" % collection_name, "r").readlines():
        if "runfiles" in line:
            runfiles_found = True
            continue

        if runfiles_found:
            if line.startswith(" "):
                runfiles.append(line.strip())

    module_names = []
    for line in runfiles:
        if "texmf-dist" in line:
            module_names.append(collection_name)

    return list(set(module_names))


def main():
    download_module(core_collections , True)
    download_module(["binextra", "fontutils"] , True)

    # Extract collection-* files to obtain tlpobj files
    extract_lxma()

    core_modules = []
    extra_modules = []
    for collection in os.listdir("."):
        if collection.endswith("tar.xz"):

            # save the modules to look for runfile patterns later
            if "binextra" in collection or "fontutils" in collection:
                module, revsion = extract_module(collection)
                extra_modules.extend(module)
            else:
                module, revsion = extract_module(collection)
                core_modules.extend(module)

            # collection files are not needed anymore. These contains just plain tlpobj files
            os.remove(collection)

    # Download modules
    download_module(core_modules, False)
    download_module(extra_modules, False)

    module_with_runfiles = []
    for module in extra_modules:
        extract_lxma(module)

        module = collection_with_runfiles_pattern(module)
        module_with_runfiles.extend(module)

    # Remove modules that does not match to the runfiles pattern
    modules_without_runfiles = set(extra_modules) - set(module_with_runfiles)
    for module in modules_without_runfiles:
        os.remove(module + ".tar.xz")


    # Additional core modules
    core_additional = ["bidi", "iftex", "pgf", "ruhyphen", "ukrhyph"]
    core_modules.extend(core_additional)
    

#    return module_names


# Create dir for packaging
#package_name = "texlive_" + name + "_2011_" + revision

## Extract and remove archive packages
#if not os.path.exists(package_name):
#    os.mkdir(package_name)

#for module in module_names:
#    os.system("tar Jxf %s.tar.xz -C %s" % (module,package_name))

## Compress files to tar.bz2 package
#print "Compressing files ..."
#os.system("tar cjf %s.tar.bz2 %s" % (package_name,package_name))

#def cleanup():
#    # Remove unused files
#    print "Removing unused files ..."
#    shutil.rtree(package_name)
#    shutil.rmtree("tlpkg")

#        os.remove(module + ".tar.xz")
#    # Remove collection tarball, it should not interrupt with module tarballs later
#    print "Removing base collection file ..."
#    os.remove(collection_package)


if __name__ == "__main__":
    sys.exit(main())



