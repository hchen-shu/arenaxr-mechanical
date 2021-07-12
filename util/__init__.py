from pygltflib import *
from collections import deque

def makeParts(filepath):
    '''take a .gltf object and separate its parts into independent .glb object. A part is a node with a mesh attached. Sometimes a part could also contain multipe nodes  be a node with no mesh, but has child nodes with mesh.'''
    
    whole = GLTF2().load(filepath)
    
    parts = [] #holds dissembled gltf parts, as well as 
    
    leaf_deque = deque() #will hold leaf node index from whole.nodes. A leaf node is the one without a child

    #re-map nodes to include 'parent' for each node
    tree= {i:{'children':[], 'parent':None, 'mesh':False} for i in range(len(whole.nodes))}
    for i, n in enumerate(whole.nodes):
        tree[i]['children'].extend(n.children)
        if n.mesh is not None:
            tree[i]['mesh'] = True
        for j in n.children:
            tree[j]['parent']=i


    #find initial leafs
    for k in tree.keys():
        if not tree[k]['children']:
            leaf_deque.appendleft(k)
    
    #cut the leaf and copy every of its ancestors as long as the ancestorss are nodes without a mesh. Discard the leaf if it has no mesh. Update leaf_deque when leaf removal produces more leafs
    while leaf_deque:

        #pop the right most leaf
        leaf_key = leaf_deque.pop()

        #update related parent node
        if tree[leaf_key]['parent']:
            parent_key = tree[leaf_key]['parent']
            tree[parent_key]['children'].remove(leaf_key)

            #if a parent node loses all children, it becomes a leaf
            if not tree[parent_key]['children']:
                leaf_deque.appendleft(parent_key)
        
        #preserve meshed leaf and all its adjacent meshless ancestors. Discard meshless leaf.
        if tree[leaf_key]['mesh']:
            parts.append(_makePart(leaf_key, whole, tree))

    return parts


def _makePart(leaf_key:int, whole:GLTF2, tree:dict)->tuple:
    
    #initiate a part, p, with a scene which directs to node
    p = GLTF2()
    p.scene = 0
    s = Scene()
    s.nodes.append(0)
    p.scenes.append(s)
    p.asset = whole.asset

    #add leaf and its meshless parents as nested nodes
    node_to_add = [whole.nodes[leaf_key]]
    parent_key = tree[leaf_key]['parent']
    while parent_key is not None:
        if not tree[parent_key]['mesh']:
            node_to_add.insert(0, whole.nodes[parent_key])
            parent_key=tree[parent_key]['parent']
        else:
            break
    
    for i, n in enumerate(node_to_add[:-1]):
        n.children=[i+1]

    p.nodes.extend(node_to_add)
    p.meshes.append(whole.meshes[p.nodes[-1].mesh])

    
    return (p, parent_key, leaf_key) # the keys are used later to reconstruct parent gltf object




makeParts('samples/boxes/twoboxes.gltf')


