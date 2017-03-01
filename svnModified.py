"""
Version: Python 3.5.4
Author: Paarth Bhasin
Purpose: Build a list of projects which have been recently modified on an existing local SVN server, to later
checkout those projects and deploy to runtime/production again.
Date: 7th February, 2017
Development Location: Cognizant Digital Works, Melbourne (Odecee/Cognizant Office)
Description: Python Program to read the file 'modified.txt', which contains the list of all the files that have been
modified, in our SVN repository. Following this, build.properties file will be updated dynamically to contain
the name of the projects that have been recently modified. This would trigger CI/CD and builds on all those projects
using Jenkins.
"""
import re
import os

svn_url = "https://m11825/svn/CICD/trunk/"
modified_file = "C:/Users/Client/Desktop/SummerInternship/modified.txt"
path = "C:/Program Files (x86)/Jenkins/workspace/PollSVN/"


def getmodifiedFiles():
    f1 = open(modified_file, mode='r')
    lines = f1.readlines()
    f1.close()
    modified = []  # Contains list of modified projects in SVN
    p = re.compile(
        "%s(.*?)((\/[\w\&\*\^\$\#\%%\@\~\`\;\:\,\<\?\"'\|\+\=\-\\[\\]\>\{\}]+\/?)+|\/?)$" % svn_url)  # Only look for projects

    for line in lines:
        string = line.split()
        m = p.search(string[1])
        if m is not None and m.group(1) not in modified:
            modified.append(m.group(1))
    print(modified)
    antProperties(modified)  # Function to update AntScript properties dynamically


def antProperties(modified):
    isApplication = False
    global path

    for word in modified:
        os.system("svn list %s/%s > abc.txt" % (svn_url, word))
        f3 = open("abc.txt", 'r')
        directory = f3.readlines()
        f3.close()
        # print(directory)
        for x in directory:
            if re.search("\.application", x) is not None:  # filter only those projects which are applications
                isApplication = True
                break

        if not isApplication:
            modified.remove(word)

        isApplication = False

    for i in range(len(modified)):
        string = "modified="  # Changes the modified_projects property in the properties file
        file_path = path
        prop_file = "build" + str(i) + ".properties"
        string += modified[i]
        print(prop_file)
        file_path += prop_file
        print(file_path)
        f2 = open(file_path, mode='w')
        f2.write(str(string))  # Write all lines back including the updated modified_projects property
        f2.close()
    print("Build file updated with latest modified projects")  # We are here means we were able to write updates.
    # os.system("cd C:/Users/Client/Desktop/SummerInternship/svnModified/ & del *.properties")


def main():
     getmodifiedFiles()

if __name__ == '__main__':
    main()
