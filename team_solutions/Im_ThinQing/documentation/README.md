# iQuHACK- Quantum Travel Website

Every traveller is different and with so many options, planning a vacation nowadays is a complex mathematical problem. Variables range from the quality of the hotel to the time of flights. In this project, we have explored the possible use of quantum computing in customizing the perfect vacation according to user input. Travelers now can spend that time relaxing instead of constantly Googling all the small details

img1

## Over-arching Idea

* The main idea behind our design is to map values of properties of flights, hotels, and restaurants separately to different bit-strings

* Create three bit-strings from the users selected options: one for the flight choices, one for the hotel choices, and one for the restaurant choices

* Use Grover’s search algorithm to filter features to return an option for the traveler from the criteria by matching such bit strings

* The advantage is only computing the data once and then having a square root speed-up when searching

## Example using Hotel Values mapped to bit-strings

img2


## Workflow

img3

## Packages and Tools

We used the following packages and tools to implement our website/app:
* Html + css (front end for user input and displaying results

* Skyscanner API for python (for webscraping)

* Covalent and IBM Qiskit for quantum computing backend.
* Flask to turn backend python code into a server to interact with front-end.

## Results - Frontend
We implemented the front-end using drop-down menus for the start location and destination.

img4

## Results - Webscraping
We used a skyscanner API to extract information on flights and saved it to a csv file.

img 5

## Results - Quantum Backend
We used covalent to access the IBM qasm simulators and Nairobi backends. We defined a python function to accept an input bit string (could be related to flight data, hotel data, and restaurant data), and generate a quantum circuit corresponding to Grover’s search algorithm for this particular string.

img 6

Then we used Flask to run the backend python code as a server which accepts an input bit-string from the front-end html website, and return its results back to the website. The flask code also loads the webscraped flight, hotel, and restaurant data to be filtered, and computes other useful parameters such as the cheapest item in each category.

img 7

## Runtime Information

We used the two following backends:
* “Ibmq_qasm_simulator”
* Total jobs run: 55
* Shots per job: 100

and

* “Ibm_nairobi”
* Total jobs run: 5
* Shots per job: 100


## Future Considerations

* Expanding the destinations to all over the world utilizing better APIs or web-scraping the data ourselves

* Adding additional criteria (ex: free-breakfast, wifi, prices, etc.) and additional features (ex: tourist destinations) and optimizing our searching algorithm through enhancing Grover’s in some way so that even with more options, it’s still fast.

* Optimize based on distance as well so for example, hotels and restaurants are close to one another

* Add a map so that users may have better visualizations


Thanks for listening!



