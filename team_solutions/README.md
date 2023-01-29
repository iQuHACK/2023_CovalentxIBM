# MRI classification using Quanvolutional layer and QNN
*Members*: *Chinmay Tompe, Joshua B., Kevin Tang, Max Huber, Zain Mughal*

v0.0 Submission for iQuHack 2023

![team logo](https://github.com/chinmaytompe/2023_CovalentxIBM/blob/main/team_solutions/images/figure1.png) 



CMD TO RUN FRONTEND:
$ expo start

CMD TO RUN BACKEND:
$ flask run -h 10.189.37.233

Our approach to the ColvalentxIBM challenge'c call for internet and people driven applications includes providing a quantum assisted and quantum enabled Neural Network to classify MRI brain scans with some and no artificates realted to Alzeihmer's (non, mild and moderate). We implemented an existing solution for image classification ( https://ieeexplore.ieee.org/abstract/document/9643516 ) that reviews various configurations of models for image classfication on the MNIST and Fashion MNIST datasets.

The authors of the paper used max pooling and dimension reduction on the MNIST data images to redeuce it down to 14x14 from 28x28, however, given our applicationn in medical diagnosis, resolution was essential to be preserved. 

*Description of files*

![architecture](https://github.com/chinmaytompe/2023_CovalentxIBM/blob/main/team_solutions/images/figure0.png)

For **Training**: run  '''bash python run.py ''' trains the QNN and saves the model in results.

*Backends tested on*: 

1. IBM QASM simulator 
2. IBM_OSLO
3. Pennylane default simulator

