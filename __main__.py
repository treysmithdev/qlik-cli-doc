import os
import json
from src.help_build import qHelpBuild, qGetVersion
from src.doc_build import docBuild 
from src.build_nav import buildNav 

version = '1.0.0'

def main():
    
    dirname = os.path.dirname(__file__)

    # Scrape qlik-cli for help documentation and build JSON object
    output = os.path.join(dirname, 'data/qlik-cli-help.json')
    qlik = {"qVersion": qGetVersion(), "qHelp": qHelpBuild(["qlik"])}
    qJSON = json.dumps(qlik,indent=4)
    with open(output,'w') as j:       
        j.write(qJSON)

    # Use JSON object to create relevant markdown documents
    input_file = os.path.join(dirname, 'data/qlik-cli-help.json')
    with open(input_file,'r') as d:
        data = json.load(d)

    
    docBuild(version, data['qVersion'], data['qHelp'])

    # Build mkdocs nav tree for qlik-cli markdown documents
    buildNav()


if __name__ == '__main__':
    main()