def br(style="-"):
    println(f"\n{style * 100}")
    
def println(text):
    print(f"{text}\n")
    
def info(text):
    println(text)

level = False
def debug(text):
    if level == True:
        println(text)

def debug_br():
    if level == True:
        br()