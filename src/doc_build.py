from jinja2 import Environment, FileSystemLoader
import os
import json
import yaml
from collections import OrderedDict
from datetime import datetime



def createTopicalList(commands):


    topics = []

    for cmd in commands:
        topics.append(cmd['topic'])

    distinct_topics = sorted(set(topics))

    result = {}

    for topic in distinct_topics:
        result[topic] = list(filter(lambda command: command['topic'] == topic, commands))
        # for c in result[topic]:
        #     if 'qHelp' in c: 
        #         c.pop('qHelp')
        #     else:
        #         print(c)
        #         c.pop('flags')

    return result



def generateMarkdown(qHelp):

    parent = True if len(qHelp['commands']) > 0 else False
    commands = createTopicalList(qHelp['commands']) if parent  else []

    templateLoader = FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__),"../templates"))
    templateEnv = Environment(loader=templateLoader)
    TEMPLATE_FILE = "command-template.md.jinja"
    template = templateEnv.get_template(TEMPLATE_FILE)
    mark_down = template.render(qHelp=qHelp, is_parent=parent, commands=commands)

    return mark_down


def exportMarkdown(qHelp):

    md = generateMarkdown(qHelp)

    md_file = os.path.join(os.path.dirname(__file__),'../docs',qHelp['tree']['self'])
    os.makedirs(os.path.dirname(md_file), exist_ok=True)
    md_export = open(md_file, "w")
    md_export.write(md)
    md_export.close()


def buildIndex():

    templateLoader = FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__),"../templates"))
    templateEnv = Environment(loader=templateLoader)
    TEMPLATE_FILE = "index.md.jinja"
    template = templateEnv.get_template(TEMPLATE_FILE)
    mark_down = template.render(date=datetime.today().strftime('%Y-%m-%d'))
    md_file = os.path.join(os.path.dirname(__file__),'../docs/index.md')
    os.makedirs(os.path.dirname(md_file), exist_ok=True)
    md_export = open(md_file, "w")
    md_export.write(mark_down)
    md_export.close()


def docBuild(qHelp):

    exportMarkdown(qHelp)
    buildIndex()

    if len(qHelp['commands']) > 0:

        for command in qHelp['commands']:

            docBuild(command['qHelp'])


