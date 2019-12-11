# Noised Randomize

Addon for randomize location, rotation and scale for group of objects

Blender version: 2.80.

## Installation
- copy `noisedRandomize.py` in the blender scripts/addons folder on your system (linux: ~/.config/blender/2.81/scripts/addons/)
- in blender go to `Edit > Preferences > Add-ons`, and enable "Scene: Noised Randomize"

## Use
- select some objects
- in tab Scene Properties there is a new panel "Noised Randomize": click on `Activate`
- play with values, even with animation


## How the addon works
The activate button create a new collection (disabled), and link selected objects: the addon will act on all the objects in this collection.

The addon use [mathutils.noise.noise(position, noise_basis)](https://docs.blender.org/api/current/mathutils.noise.html#mathutils.noise.noise) to get random values: these values are applied to *delta transformation* of each object with the strength set in  "Multiplier for transformation".

Act as a Displace modifier controlled by procedural texture (noise), but not deform objects, just move, rotate, scale.

### Values
- **noise scale**: the scale for the "procedural image"
- **locX, locY, locZ**: the position of the "procedural image"
- **Noise type**: the type of the "procedural image" ("Random" is a pure random value: always different)
- **Multiplier for transformation**: the strength of transformation: the random value will be multiplied by this number and then applied to the relative (delta) transformation 
- **Hide**: hide temporarily the transformations
- **Copy to transform**: copy all values from the delta transformation to main transformation
- **Copy to transform and remove** : delete collection, reset all delta transformation to 0 (1 for the scale) and deactivate the addon
- **Select all objects**: select all objects in collection
- **Remove**: delete collection, reset all delta transformation to 0 (1 for the scale) and deactivate the addon
- **Activate**: create collection, or add object to

## License

Noise Randomize is distributed under the terms of the GNU General Public License, version 2 or later. See the LICENSE.txt file for details.




