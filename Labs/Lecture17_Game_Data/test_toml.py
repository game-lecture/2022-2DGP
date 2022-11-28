import tomllib

toml_str = """
simple_int = 3.5
simple_str = 'Simple'
'name "inside"' = 'lee dae hyun'
physics.color = 'RED'
fruit.apple.smooth = true
''.name = 'nayeon'
"""


toml_str = """
[table]
name = 'nayeon'
height = 186


[table2]

"""

toml_str = """
nayeon.x = 3
nayeon.y = 4

"""
toml_str = """
zombies = [
   {name = 'nayeon', height = 186},
   {name = 'hj', height=170}
]
zombie.name = 'test'
"""

toml_str = """
data = {a=1,b=2}
"""


data = tomllib.loads(toml_str)
print(data)
with open('zombie_data.toml', 'rb') as f:
    data = tomllib.load(f)
    zombie_list = data['zombie']['data']
    print(zombie_list)


