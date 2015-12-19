# MotionPlanningWithDNN

Maps seen from the top are similar to images, and deep neural networks are good at classifying images. So I thought : why not classify a map, a starting point, and a goal with a deep neural network ? The nice result is to have the network answer: from this point, go LEFT, LEFT, LEFT, then TOP, and then LEFT : you have reached your destination.

## Results
This is a map seen from the top, of 10x10 cells, with obstacles in black, reachable areas in white, the starting location in red, and the goal in green. At each step, the network says which direction to take, until the goal is reached:

<img src="https://raw.github.com/matthieudelaro/MotionPlanningWithDNN/master/results/success_avoid_wall_001442/asGif_200x200px.gif" width="200"> 

(images for each step are available in directory ./results/success_avoid_wall_001442/)


## References
The network has been trained with Lasagne : https://github.com/Lasagne/Lasagne


## The MIT License (MIT)

Copyright (c) 2015 matthieudelaro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
