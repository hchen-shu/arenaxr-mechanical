# introduction
Arenaxr-mechnical, axrmech, is a python tool that enables designers to upload a glTF object as a set of parts to arenaXR's persistant database. A part is a component of a larger glTf model. Separation into the parts enables designers to assign animations and event triggers individually to each part, which further enables the simulation of real world objects. The purpose of this tool is to overcome a limitation of arenaxr: it dose not support mouse event emission at a sub-component level on an object ([see the mqtt event message](https://arena.conix.io/content/messaging/definitions.html)). This means an multi-part object cannot know which part is clicked, thus is unable to response with an animation of that part. 

When parts are separated, arenaxr-mechnical first determines the root parent object. This object is used as the base or foundation to assemble all other parts as children.  In order to let arenaxr-mechnical *automatically add the parent-child relationship in the .asm json document,* a model designer needs to carefully *gourp* parts in a glTF-capable editor (such as Unity with Platter plug-in) to build a heirarchy which assigns the parent part as the root.

For example, Part_A in Unity Hierarchy window will be designated as parent for Part_B and Part_C.
```
Part_A
    |-Part_B
    |-Part_C
```

ArenaXR-mechanical initially supports Unity-generated glTF files. Other modeling tools will be supported in the following updates.

# prep
* Install dependencies including pygltflib and arena-py using
```
pip install gltflib arena-py
```
* Replace a dependency package with its older version. This step is required to resolve errors raised from `_TypedDictMeta`. First use 
```
pip uninstall typing-inspect
```
then use 
```
pip install typing-inspect==0.6.0
```
* Have a dropbox account for sharing `.glb` files
* In Unity, group parts properly so that a child part is movable against a parent stationary part. A child part may stay stationary to its parent as well. In the following example, Part_A is a stationary part, and Part_B and Part_C are child parts that may or may not move against Part_A.
```
Part_A
    |-Part_B
    |-Part_C
```
* A complex model may have multiple parts move against different stationary parts. Use nested children to represent this model. In the following example, Part_B and _C move against Part_A, while Part_D moves against Part_C.
```
Part_A
    |-Part_B
    |-Part_C
        |-Part_D
```
* use Unity 2019 LTS + platter glTF exporter (support for other modeling tools will be available in the future release)

# workflow

1. create a model using a glTF-capable editor (Unity <2019 LTS> with Platter is the only supported editor at this moment), export the model as glTF zip via Platter. Lastly, unzip it into a **Dropbox** folder, go to the folder and copy the path for a `.gltf` file as *your_path*. 
2. In a console, run the following code to produce `parts` subfolder in place containing `config.json` along with all the parts as `.glb` files.
```
python axrmech.py --disassemble your_path
```  
3. edit `config.json` to give each `.glb` part a Dropbox sharelink, as well as other attributes including triggers or animations. 
4. run the following command to populate the parts in to a scene. This registors the parts to the database, but dose not dispatch click reaction or animation to the parts.
```
python axrmech.py --upload your_path/parts/config.json
``` 
5. run the following command to make the parts responsive to user clicks
```
python axrmech.py --activate  your_path/parts/config.json
```

# limitation
* the following gltf components will be ignored: camera, skin, animation
* material support will be included in the next release.

