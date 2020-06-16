### EXECUTE THIS SCRIPT FOR ALL OUTPUT

length=7
width=7
num=10000

python tests.py $length $width $num basic SandPile
python tests.py $length $width $num basic SandPileEXT1
python tests.py $length $width $num basic SandPileEXT2

python tests.py $length $width $num centre_of_grid SandPile
python tests.py $length $width $num centre_of_grid SandPileEXT1
python tests.py $length $width $num centre_of_grid SandPileEXT2

python tests.py $length $width $num tlq_cells SandPile
python tests.py $length $width $num tlq_cells SandPileEXT1
python tests.py $length $width $num tlq_cells SandPileEXT2

python tests.py $length $width $num four_grains SandPile
python tests.py $length $width $num four_grains SandPileEXT1
python tests.py $length $width $num four_grains SandPileEXT2

python tests.py $length $width $num random_grains SandPile
python tests.py $length $width $num random_grains SandPileEXT1
python tests.py $length $width $num random_grains SandPileEXT2
