import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import Layout from "./components/Layout";

const inter = Inter({ subsets: ["latin"] });

export default function Page404() {
  return (
    <>
      <Layout>
      <h1 className="font-bitcount font-medium text-4xl lg:text-6xl mx-8 xl:mx-44 text-center">
        <span className="bg-gradient-to-tr font-medium from-[#FF71BE] via-[#B871FF] to-[#3183FF] bg-clip-text text-transparent">404</span> Page Not Found
        </h1>
      </Layout>
    </>
  );
}
