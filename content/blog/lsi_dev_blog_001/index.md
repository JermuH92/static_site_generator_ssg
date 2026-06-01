# DevLog 001: Planting the First Seed of Lakeside Interactive Studios

[< Back Home](/)

`June 1st, 2026 - Author: Jere Kukkohovi`

Today, I started experimenting more with 3D Web Development by finally deciding to take a step towards the goal on building a visually stunning and technically demanding homepage and asset playground for my upcoming game studio - _Lakeside Interactive Nordic_. 

The first objective for the day was to see if I still have some 3D-dev skills remaining from nearly 10 years ago using 3DSMax back in the day. **Spoiler: Well I sort of did, but it did take most of the day to just implement one single 3D model**

So I booted up Blender in the morning, checked a few tutorials and used some AI-assistance to get myself comfortable with the basic controls and primitive modeling again.

`But it never is that simple, is it?`

## First Asset for the Website and Actual Footwork

After playing around with primitive sylinders for a bit and trying to get the form of the tree model that I wanted for the final scene on the website, I learned about using the add-on `Sapling Tree Gen` for procedural sapling and tree generation inside Blender itself so I used that to sculpt the skeleton for the tree and its branches.

**Then came the first hiccup, perhaps out of my own perfectionism. I needed the nettles for the tree branches too, so I'd need a PNG-image with transparent background out of a Pine Tree branch...**

Now while 3D Asset Libraries and Stock Image Websites are Dime a Dozen nowadays, I quickly noticed after nearly 3 hours of scouring the internet that good quality free images are pretty scarce. So I decided to become a nature photographer for a brief moment in time, went out and took a few pictures with my phone out of a pine tree close to my apartment, removed its background and used that to model the nettles on growing from the tree branch.

![image of a pine tree branch](/images/pine_ssg.jpg)

## Stepping into the Node Maze: Geometry Nodes

With my homemade pine branch texture ready, it was time to scatter it across the tree. Enter Blender’s Geometry Nodes, which is basically visual programming. Data goes in, functions process it, and 3D geometry comes out. 

My initial "code" setup was simple: take the tree mesh, distribute points on the faces, instance my branch asterisk on those points, and output it. Simple, right? Well, the algorithm turned out to everything but that:

1. **The GPU Meltdown:** I initially cranked the density multiplier to 200. Because Geometry Nodes calculate density based on surface area, and my new tree trunk was thick, my graphics card fans immediately screamed into overdrive. I quickly dropped it below 70s range before my rig took flight.
2. **The Vanishing Trunk (The Narnia Incident):** Once the needles appeared, the entire trunk completely vanished. It turned out the scatter node was replacing the original geometry with points. Dropping a `Join Geometry` node at the end of the pipeline brought the trunk right back from the void.
3. **The "Tree Chewbacca" Problem:** The needles were spawning *everywhere*—including right on the thick lower trunk where it should just be bare bark. My first fix was a basic Z-axis height mask, but the trunk goes all the way to the top, so it still looked wrong. The elegant, code-like solution? A `Face Area` mask. Large faces (the trunk) got a hard zero density, while tiny faces (the branch tips) got 100% density. Chewbacca is shaved now.

![Final procedural pine tree asset in Blender viewport](/images/blender_day1.png)

## Shifting Gears: Baking and gltfjsx

Web browsers are fast, but they aren't smart enough to calculate Blender’s live node math on the fly. To bridge the gap to React, I dropped a `Realize Instances` node at the end of the chain to bake everything into hard vertices, and exported it as a `.glb` file.

Now, manually parsing a GLTF file in React Three Fiber is a chore. I know this because I tried to do it with my own portfolio website. For this reason learning to use a CLI tool called `gltfjsx`, previously on my 3D portfolio website made using it in this project easy from the get-go:

`npx gltfjsx public/models/pine_tree.glb -t`

This unpacked the binary file and generated a perfectly structured, type-safe React component (`PineTree.tsx`) where every single mesh and material became a declarative JSX tag.

## The Struggle of switching between JSX and TSX

Dropping the generated code into a fresh Vite + React + TypeScript lab environment immediately triggered some errors. 

First up was a tight TypeScript compilation error: the generated `JSX.IntrinsicElements['group']` was completely unrecognized by Vite’s strict layout. A surgical refactor solved it: I explicitly imported `React`, and swapped the prop type to `React.ComponentPropsWithoutRef<'group'>`.

Next, TypeScript refused to trust the GLTF hook's return value, so I had to use a override: force-casting the asset layout via `as unknown as GLTFResult`.

Then came the final, most confusing error in the browser console:
`Unexpected token '&lt;', "&lt;!doctype "... is not valid JSON`

The browser was looking for the model in the wrong folder path. Instead of finding the binary 3D data, Vite used the default `index.html` 404 page. When the GLTF loader tried to parse a standard HTML document as 3D data, it blew up. Fixing the pathing for useGLTF was enough to fix the issue.

## The Branch is Alive!

With some `&lt;ambientLight /&gt;`, an `&lt;Environment preset="forest" /&gt;` for global illumination, and `&lt;OrbitControls /&gt;` dropped into the `&lt;Canvas&gt;`, the tree finally popped up on the screen.

![Completed pine tree rendering on a blank white canvas with browser devtools console open](/images/day1_final.png)

It's not a full forest yet, but even seeing a single optimized procedural asset ready, rotatable and scaled correctly in the browser window was the victory I needed for today. 

Next up: figuring out how to duplicate this instance into a massive forest and lake scene without melting the browser.

**Until next time.**

**Jere Kukkohovi**

[< Back Home](/)