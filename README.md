# Synthetic Cerebral Blood Vessel Generator for Training Anatomically Plausible Deep Learning Models<img width="3560" alt="image" src="https://github.com/user-attachments/assets/712f1903-8490-4233-a8d4-253e0f6a691c">

Synthetic Vessel Generator for the generation of synthetic cerebral vessel labels. 

(A) The vessel generator is designed to be adaptable to produce anatomically plausible vessels and implausible vessels, that do not obey, to a controllable degree, the known literature rules.

(B) The generator then produces a score image, of the same label image dimension to represent the location of the implausibility and the scale of inaccuracy. 


(1) INITIALISATION OF PARTICLES 

Acts as a realistic starting point for vessel growth. Initial vessel segments are traced out with specific attributes: 
  1) Particle’s initial velocity 
  2) Particle’s initial location (location of the Internal Carotid Artery)
  3) Length and radius of the vessel (Rai, 2013)
  4) Distance to a branching event - determines the next branching point. 



(2) THE ENGINE OF THE SIMULATION 
  1) Iteratively updates the properties of all current particles, tracing out the continuous vessel structures. 
Speed and resolution of image generation optimization using reduced iteration ‘step-size’ with reduced vessel radii.
  2) A vessel length update function adjusts new vessel branch lengths using empirical data to maintain a realistic length-radius ratio (LR).
  3) Vessel growth direction: influenced by repulsive forces from nearby vessels and brain structures.
       - Each iteration uses the current velocity vectors and repulsive forces to move the particles to simulate vessel geometry and the shape of vessels between branch points.  
      - Amount of repulsion ensures that the vessels do not intersect unnaturally and remain within the boundaries of the brain. 


(3) ONCE A BRANCH POINT IS REACHED
  1) The number of new branches is initialized to determine if the branch has a bifurcation, trifurcation or no branching – 70%, 30% and 20% probability. 
  2) Dynamically establishes the new radii of the daughter branches dependent on the parent and daughter branch characteristics. 
  3) Branching angles between daughter vessels are adjusted, by calculating the vector components of the new branches based on the parent vessel's direction- obeying Murray's law. 

(4) PARTIAL VOLUME RENDERING

- The simulator renders a 3D skeleton image of the vascular network, where each voxel in the vessel image stores the vessel radius at that point,
- Voxel radii are used to linearly interpolate partial volume contributions (pre-calculated numerically for a range of cylinders of different sizes and locations within the voxel) to accurately reflect the volumetric contributions of the vessels.
<img width="2838" alt="image" src="https://github.com/user-attachments/assets/ff1f094b-3809-42bb-946b-81c4bdfe335c">


