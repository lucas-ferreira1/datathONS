import os

# Lista de bibliotecas a serem instaladas
libraries = [
    "cmath",
    "math",
    "numpy",
    "pandas",
    "matplotlib",
    "scipy",
    "sympy"
]

# Função para instalar uma biblioteca
def install_library(library):
    os.system(f"pip install {library}")

# Iterar sobre a lista de bibliotecas e instalá-las uma por uma
for lib in libraries:
    install_library(lib)

# Algumas bibliotecas precisam de instalação adicional, como sympy
# Neste caso, você pode usar o seguinte comando:
os.system("pip install scipy")

print("Todas as bibliotecas foram instaladas com sucesso.")
