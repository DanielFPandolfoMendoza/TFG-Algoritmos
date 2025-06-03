<h1>DAY 1</h1>

<p>This is the first day of development, and before starting, I need to define the structure that this project will follow. Since the objective of this project is to determine the best way to solve the MTVRP problem, I will divide the development into multiple stages, each one introducing more restrictions than the previous one, until all the constraints of the original problem are met. I want to follow this structure so that everyone can track the progress I make throughout the project.</p>

<p>I have created the proyect structure and the method to get the information from the files that are given</p>

<h1>DAY 2</h1>

<p>I need to solve some issues related to the initial version of the method used to extract information from the files, as it did not consider the depot location.

To address this, I have developed a basic algorithm to solve the first relaxed version of the MTVRP. This algorithm starts at the depot and iteratively selects the nearest point using the Euclidean distance. It repeats this process, continuously finding and moving to the closest unvisited point, until all points have been reached. Finally, it returns the path followed to visit all the points and the total time taken.

This first relaxed version is hardly an MTVRP, as it does not include multiple vehicles and lacks any constraints. However, I wanted to develop this initial version to create a basic algorithm and use it as a baseline for future improvements.</p>

<h1>DAY 3</h1>
<p>Today, several changes were made to improve and adapt the routing algorithm according to problem constraints:</p>

<h2>Routing Strategy Updated</h2>
<p>The original nearest-point (greedy) approach using Euclidean distance was replaced with a random coordinate selector.
This was done to better align with the problem constraints.</p>

<h2>Truck Capacity & Distance Constraint</h2>
<p>The truck now has a limited capacity and dsitance.It continues visiting random delivery points until it runs out of capacity, once the capacity is reached and no further deliveries can be made, the truck returns to the depot.</p>

<p>Then it will search for another random point to keep delivering.
In the next version i will include various trucks to achive all the restrictions and conditions of the MVRTP problem</p>

<h1>DAY 4</h1> 
<p>This week, significant changes have been implemented as I have met all the restrictions of the MVRTP.</p> 
.
<p>I have modified the algorithm to support multiple vehicles, among other improvements. Let’s take a closer look:</p> 

<h2>Algorithm Overview</h2> 

<h3>Step 1:</h3> <p>The truck identifies all the points it can reach, considering both distance and capacity constraints. It cannot go to a point if it would be unable to satisfy the demand, or if returning to the depot would exceed the distance limit.</p> 
<h3>Step 2:</h3> <p>The truck then randomly selects one of the valid points. After that, the used capacity and distance are deducted from the remaining available resources.</p> 
<h3>Step 3:</h3> <p>The truck checks again if it can reach any other point with the remaining capacity and distance. If it cannot reach any other point, it returns to the depot.</p> 
<h3>Step 4:</h3> <p>Once back at the depot, the truck’s capacity is fully replenished. The algorithm then searches again for any reachable point that does not violate the constraints. If none is found, a new truck—with full capacity and distance—is deployed.</p> 
<h3>Step 5:</h3> <p>This process is repeated until all points have been visited. Finally, the algorithm outputs the route followed, the total distance traveled, the remaining capacity, and the number of trucks used.</p> 

<p>In addition to the algorithm modifications, I have updated the script to read all the necessary data from the various files.</p> 

<p>Lastly, I will upload the results of this algorithm to compare them with those from the second part of this TFG, where I will develop a new version of the algorithm.</p>

<h1>DAY 5</h1>

<p>Today I obtained the results of the Phase 1 algorithm and created an Excel file to store them. I haven't created a tag yet, as these results might be incorrect or incomplete. Once I review them with my professor and make any necessary adjustments, I will update the file and assign a proper tag.</p>

<h1>DAY 6</h1>

<p>Over the past two days, I've been making changes to the code so that it can perform 100 executions of the algorithm and automatically store the best result. After that, I also improved and reorganized the Excel file containing the results.
I have posted the updated version in the project's Markdown for documentation and review.</p>

<h1>DAY 7<7h1>

<p>After a few weeks of pause, I’ve begun the second phase of this thesis project, which involves implementing a sweep algorithm to determine the optimal order for making deliveries.

The first step in this process is to calculate the angle between each delivery point and the depot (the starting location). This is essential because the priority of each delivery point will be based on its angle relative to the depot.

To perform this calculation, a method called calculate_angle has been developed. It takes two inputs: the origin point (the depot) and a delivery point. The method uses the atan2 function to compute the angle between these two points.

The atan2 function determines the direction of one point in relation to another by calculating the angle between the positive x-axis and the vector formed by drawing a line from the depot to the delivery point. This allows the delivery points to be sorted in ascending order of their angles, enabling a clockwise sweep pattern.
</p>
