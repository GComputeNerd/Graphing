import subprocess
import os

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

# Program to test rendering of LaTeX equation into a .svg file

def renderMath(eqn, name):
    # Rendering equation
    
    template = resources.open_text("graphing","template.tex")
    
    try :
        f = open("tex-files/" + name + ".tex", "w")
    except FileNotFoundError:
        os.mkdir("tex-files")
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
