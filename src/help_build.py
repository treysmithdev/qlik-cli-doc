import subprocess
import json
import os

def qHelpBuild(params):

    qHelp = {
        "name": '',
        "path": '',
        "tree": {},
        "description": '',
        "usage": [],
        "commands": [],
        "flags": {
            "local": [],
            "global": []
        }
    }

    cli_params = [row[:] for row in params]
    qHelp['name'] = cli_params[-1]
    qHelp['path'] = ' '.join(cli_params)
    cli_params.append("-h")

    path = qHelp['path'].split(' ')



# parent_path: location of parent file
# self_path: location of export file
# child_path: variablized location of child command file 

# Scenarios:

# path: qlik

#     parent_path: NULL
#     self_path: /qlik/qlik.md
#     child_path: /qlik/[cmd]/[cmd].md
#         - /qlik/app/app.md

# path: qlik app

#     parent_path: /qlik/qlik.md
#     self_path: /qlik/app/app.md
#     child_path: /qlik/app/app [cmd].md
#         - /qlik/app/app content.md

# path: qlik app content

#     parent_path: /qlik/app/app.md
#     self_path: /qlik/app/app content.md
#     child_path: /qlik/app/app content [cmd].md
#         - /qlik/app/app content get.md

# path: qlik qrs

#     parent_path: /qlik/qlik.md
#     self_path: /qlik/qrs/qrs.md
#     child_path: /qlik/qrs/[cmd]/[cmd].md
#         - /qlik/qrs/qrs/app/app.md

# path: qlik qrs app

#     parent_path: /qlik/qrs/qrs.md
#     self_path: /qlik/qrs/app/app.md
#     child_path: /qlik/qrs/app/app [cmd].md
#         - /qlik/qrs/app/app copy.md

    if len(path) == 1:
        parent_path = 'index.md'
        self_path = '{0}/{0}.md'.format(path[0])
        child_path = '{0}/{1}/{1}.md'.format(path[0],'[cmd]')

    elif 'qrs' not in path:

        # qlik app
        if len(path) == 2:

            parent_path = '{0}/{0}.md'.format(path[0]) # /qlik/qlik.md
            self_path = '{0}/{1}/{1}.md'.format(path[0],path[1]) # /qlik/app/app.md
            child_path = '{0}/{1}/{1} {2}.md'.format(path[0], path[1], '[cmd]') # /qlik/app/app copy.md
        
        else:
            parent_path = '{0}/{1}/{2}.md'.format(path[0], path[1], ' '.join(path[1:-1])) # /qlik/app/app.md
            self_path = '{0}/{1}/{2}.md'.format(path[0],path[1],' '.join(path[1:])) # /qlik/app/app dimension.md
            child_path = '{0}/{1}/{2} {3}.md'.format(path[0], path[1], ' '.join(path[1:]), '[cmd]') # /qlik/app/app dimension ls.md

    elif 'qrs' in path:

        if len(path) == 2:

            parent_path = '{0}/{0}.md'.format(path[0]) # /qlik/qlik.md
            self_path = '{0}/{1}/{1}.md'.format(path[0],path[1]) # /qlik/qrs/qrs.md
            child_path = '{0}/{1}/{2}/{2}.md'.format(path[0], path[1], '[cmd]') # /qlik/qrs/app/app.md

        elif len(path) == 3:
            parent_path =  '{0}/{1}/{1}.md'.format(path[0],path[1]) # /qlik/qrs/qrs.md
            self_path = '{0}/{1}/{2}/{2}.md'.format(path[0], path[1], path[2]) # /qlik/qrs/app/app.md
            child_path = '{0}/{1}/{2}/{2} {3}.md'.format(path[0], path[1], path[2], '[cmd]') # /qlik/qrs/app/app dimension.md

        else:
            parent_path =  '{0}/{1}/{2}/{3}.md'.format(path[0], path[1], path[2], ' '.join(path[2:-1])) # /qlik/qrs/app/app.md
            self_path = '{0}/{1}/{2}/{3}.md'.format(path[0], path[1], path[2], ' '.join(path[2:])) # /qlik/qrs/app/app dimension.md
            child_path = '{0}/{1}/{2}/{3} {4}.md'.format(path[0], path[1], path[2], ' '.join(path[2:]), '[cmd]') # /qlik/qrs/app/app dimension ls.md



        

    qHelp['tree']['parent'] = parent_path
    qHelp['tree']['self'] = self_path
    qHelp['tree']['child'] = child_path

    response=subprocess.check_output(cli_params).decode('utf-8')
    out = response.split('\n\n')


    

    for i in range(len(out)):

        if i == 0 and 'Usage:' not in out[i]:
            qHelp['description'] = out[i]
        elif 'Usage:' in out[i]:
            usage_list = out[i].split('\n')
            usage = [s.strip() for s in usage_list]
            usage.pop(0)

            qHelp['usage'] = usage
        elif 'Commands:' in out[i]:
            command_block = out[i].split('\n') 
            commands = []
            for i in range(len(command_block)):
                if i == 0:
                    topic = command_block[i].replace('Commands:','').strip()
                else:
                    cmd_txt = command_block[i].strip()
                    cmd_words = cmd_txt.split(' ')
                    cmd = cmd_words[0]
                    cmd_words.pop(0)
                    cmd_details = ' '.join(cmd_words)

                    cmd = {"topic": topic.strip(), "name": cmd, "description": cmd_details.strip()}
                    commands.append(cmd)
            qHelp['commands'].append(commands)
        elif 'Flags:' in out[i]:

            if 'Global Flags:' in out[i]:
                flag_type = 'global'
            elif 'Flags:' in out[i]:
                flag_type = 'local'


            flag_block = out[i].split('\n')
            flag_block.pop(0)

            for i in range(len(flag_block)):

                content_check = flag_block[i].strip()

                if len(content_check) == 0:
                    continue
                
                flag = {}
                flag_details = flag_block[i].split('   ')
                f = flag_block[i]

                if ',' in f[:5]:
                    flag['shorthand'] = f[:4].strip()
                    f = f[6:len(f)]

                f = f.lstrip()

                flag['name'] = f[0:f.find(' ')]

                f = f.replace(flag['name']+' ','',1)

                if f[:1] != ' ':
                    flag['type'] = f[:f.find(' ',1)]
                    f = f.replace(flag['type'],'',1)
                
                flag['description'] = f.strip()


                qHelp['flags'][flag_type].append(flag)
                

    qHelp['commands'] = [j for i in qHelp['commands'] for j in i]

    has_child = False

    parent_command = []
    child_command = []

    for use in qHelp['usage']:
    
        if '[command]' in use:
            parent_command = use.split(' ')
            parent_command.pop(-1)
            has_child = True
    
    if has_child:

        for c in range(len(qHelp['commands'])):
            child_command = []
            child = qHelp['commands'][c]
            param = child['name']
            # child_command = [row[:] for row in params]
            # child_command.append(param)
            child_help = qHelpBuild(parent_command+[param])
            qHelp['commands'][c]['qHelp'] = child_help

    return qHelp



