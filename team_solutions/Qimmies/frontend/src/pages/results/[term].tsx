import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import Layout from "../components/Layout";
import Search from "../components/Search";
import { useRouter } from 'next/router'
import ResultsData from "../components/ResultsData";



export default function Results() {
const router = useRouter()
const { term } = router.query
  return (
    <>
        <Layout>
            <Search searchTerm={''} />
            <h1 className="font-bitcount font-medium text-4xl lg:text-6xl mx-8 xl:mx-44 text-center mb-10">Showing results for <span className="bg-gradient-to-tr font-medium from-[#FF71BE] via-[#B871FF] to-[#3183FF] bg-clip-text text-transparent">{term}</span></h1>
            <ResultsData/>
        </Layout>
    </>
  );
}
