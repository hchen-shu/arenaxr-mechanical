## Introduction
This python tool enables you to upload a glTF model to arenaXR as a collection of its parts. A part is a component of the original glTf model. The part should have a separate mesh and is mechanically recognized as an one piece object. 

Spliting a single model into multiple parts before uploading into A-FRAME based environment like arenaXR has advantages when a designer wants to deal with the individual animation for each part for a responsive event such as a mouse click. For example, a calculator model (which contains a base and a set of buttons moving against the base) can be processed using this tool to simulate the real calculator's motion when a user' mouse click event is detected on each button. In contrast, if the calculator model is imported as one piece, then the animation under A-FRAME can only be assigned to the entire model as one piece, which loses the ability to see the motion of the components.

## design 

This tool takes an entire 3d model in glTF (which contains components as child nodes), then split each part (node) into a independent glTF/glb file, while recording the relative position of all the parts for the reconstruction of all the parts back in the A-FRAME environment. A parent part will be assgined to represent the base (the non moving part), and all other parts will be assigned as children so that their animiated motions referenced to the base

