# MRI classification using Quanvolutional layer and QNN
v0.0 Submission for iQuHack 2023

CMD TO RUN FRONTEND:
$ expo start

CMD TO RUN BACKEND:
$ flask run -h 10.189.37.233

Our approach to the ColvalentxIBM challenge'c call for internet and people driven applications includes providing a quantum assisted and quantum enabled Neural Network to classify MRI brain scans with some and no artificates realted to Alzeihmer's (non, mild and moderate). We implemented an existing solution for image classification ( https://ieeexplore.ieee.org/abstract/document/9643516 ) that reviews various configurations of models for image classfication on the MNIST and Fashion MNIST datasets.

The authors of the paper used max pooling and dimension reduction on the MNIST data images to redeuce it down to 14x14 from 28x28, however, given our applicationn in medical diagnosis, resolution was essential to be preserved. 




