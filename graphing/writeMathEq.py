import subprocess
from graphing.data import *

# Program to test rendering of LaTeX equation into a .svg file

def renderMath(eqn, name):
    # Rendering equation
    
    template = open(root + "graphing/template.tex")
    f = open("tex-files/" + name + ".tex", "w")
    line = ""
    
    while (not (r"\begin{document}" in line)):
        line = template.readline()
        f.write(line)
    
    f.write(eqn)
    
    for line in template:
        f.write(line)
    
    template.close()
    f.close()
    
    # Render .tex into .dvi
    
    subprocess.run(['latex', '-output-directory', 'tex-files', name + ".tex"])
    
    # Render .dvi into .svg
    
    subprocess.run(['dvipng', '-bg', 'Transparent',  'tex-files/' + name + ".dvi", "-o", 'tex-files/' + name + ".png"])
