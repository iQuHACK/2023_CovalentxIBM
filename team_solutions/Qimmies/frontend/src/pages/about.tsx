import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import Layout from "./components/Layout";

const inter = Inter({ subsets: ["latin"] });

export default function About() {
  return (
    <>
      <Layout>
        <h1 className="mb-10 font-bitcount font-medium text-4xl lg:text-6xl mx-8 xl:mx-44 text-center">About <span className="bg-gradient-to-tr font-medium from-[#FF71BE] via-[#B871FF] to-[#3183FF] bg-clip-text text-transparent">inQuiry</span></h1>
        <p className="mb-6 text-lg">
            InQuiry is a web app that utilizes quantum machine learning to perform sentiment analysis on Reddit data, allowing users to explore public opinion on a variety of topics. Ideally it is used for company and startup market research. When users enter a search phrase, inQuiry scrapes the top 20 reddit posts and generates a list of keywords that appear in the results. Our quantum sentiment analysis algorithm then considers these keywords in context to assess public opinion regarding the topic. The app also displays related words, phrases, and sentiments to the user’s input to give more insights on their topic. In a revision of inQuiry, our sentiment analysis algorithm would consider other social media sites to get a more holistic view of the sentiment surrounding a topic.
        </p>
        <p className="mb-6 text-lg">
            Our algorithm uses QSVC to train quantum kernels for sentiment analysis, inspired by <a className="text-[#876AFB] underline" href='https://covalent.readthedocs.io/en/latest/tutorials/1_QuantumMachineLearning/quantum_embedding_kernel/source.html'>this tutorial</a>. Starting with a dataset from Sentiment140, we then use the Natural Language Toolkit and scikit-learn to vectorize phrases for use in the model. The ansatz used in the circuit encodes the model’s parameters in the angles of Z gates and contains as many layers as necessary to encode all features in the input vectors. The quantum circuit is expressed using Pennylane and the pennylane-qiskit plugin with scikit-learn for the SVC algorithm. We ran the training through a local covalent instance to visualize processes.
        </p>
        <p className="mb-6 text-lg">
            We were able to run tests of the QSVC algorithm on IBM’s quantum hardware, but we found that the training was very slow on both quantum hardware and simulators when we introduced the real training data. This was likely due to the high number of features in the vectorized phrases, which meant that the circuit needed hundreds of layers. While we are confident that this algorithm would work given more time (and better quantum computers), QSVC is more ideal for vectors with less features. We ultimately ended up training the model classically for our demo.
        </p>
        <p className="mb-6 text-lg text-left">
            This project was submitted for <a className="text-[#876AFB] underline" href="https://github.com/iQuHACK/2023_CovalentxIBM">Covalent x IBM</a> Challenge at MIT iQuHACK 2023.
        </p>
      </Layout>
    </>
  );
}
