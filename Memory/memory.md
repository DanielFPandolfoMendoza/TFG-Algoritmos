<h1>DAY 1</h1>

<p>This is the first day of development, and before starting, I need to define the structure that this project will follow. Since the objective of this project is to determine the best way to solve the MTVRP problem, I will divide the development into multiple stages, each one introducing more restrictions than the previous one, until all the constraints of the original problem are met. I want to follow this structure so that everyone can track the progress I make throughout the project.</p>

<p>I have created the proyect structure and the method to get the information from the files that are given</p>

<h1>DAY 2</h1>

<p>I need to solve some issues related to the initial version of the method used to extract information from the files, as it did not consider the depot location.

To address this, I have developed a basic algorithm to solve the first relaxed version of the MTVRP. This algorithm starts at the depot and iteratively selects the nearest point using the Euclidean distance. It repeats this process, continuously finding and moving to the closest unvisited point, until all points have been reached. Finally, it returns the path followed to visit all the points and the total time taken.

This first relaxed version is hardly an MTVRP, as it does not include multiple vehicles and lacks any constraints. However, I wanted to develop this initial version to create a basic algorithm and use it as a baseline for future improvements.</p>