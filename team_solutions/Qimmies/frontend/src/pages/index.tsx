import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import Layout from "./components/Layout";
import Search from "./components/Search";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <>
      <Layout>
        <h1 className="font-bitcount font-medium text-4xl lg:text-6xl mx-8 xl:mx-44 text-center">
          Effortlessly <span className="bg-gradient-to-tr font-medium from-[#FF71BE] via-[#B871FF] to-[#3183FF] bg-clip-text text-transparent">explore collective opinion</span>, powered by scalable quantum hardware.
        </h1>
        
        <Search searchTerm=""/>
        <div className="text-md md:text-xl text-center">
          Feeling stuck? Try <a href='/results/cats' className="text-[#876AFB] underline">cats</a>, <a href='/results/quantum%20computing' className="text-[#876AFB] underline">quantum computing</a>, or experiment with our <a href='/tools' className="text-[#876AFB] underline">rapid iteration tool</a>.
          </div>
      </Layout>
    </>
  );
}
