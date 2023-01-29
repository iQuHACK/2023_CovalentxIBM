import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import Layout from "./components/Layout";

export default function Tools() {
  return (
    <>
      <Layout>
      <h1 className="font-bitcount font-medium text-4xl lg:text-6xl mx-8 xl:mx-44 text-center">
        Advanced Tools: 
        <span className="bg-gradient-to-tr font-medium from-[#FF71BE] via-[#B871FF] to-[#3183FF] bg-clip-text text-transparent"> Coming Soon</span> 
        </h1>
      </Layout>
    </>
  );
}
