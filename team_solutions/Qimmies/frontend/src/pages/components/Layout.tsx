import Head from "next/head";
import Link from "next/link";
import Image from "next/image";
import { ReactNode } from "react";

interface Props {
    children: ReactNode
  }

export default function Layout({ children }: Props) {
    return (
        <>
        <Head>
            <title>inQuiry</title>
            <meta name="description" content="inQuiry: Effortlessly explore collective opinion, powered by quantum hardware." />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <link rel="icon" href="/favicon.ico" />
            <link rel="stylesheet" href="https://use.typekit.net/fwi5qbj.css"></link>
        </Head>
        <div className="min-h-screen">
            <header className="flex flex-col md:flex-row w-screen justify-between px-28 pt-12 pb=4">
                <Link href='/'>
                    <Image src='/logo.png' alt='logo' width={150} height={100}/>
                </Link>
                <nav className="flex flex-col md:flex-row">
                    <Link className="md:mx-8 hover:text-[#876AFB] hover:underline" href='/tools'>Tools</Link>
                    {/* <Link className="md:mx-8 hover:text-[#876AFB] hover:underline" href='/pricing'>Pricing</Link> */}
                    <Link className="md:mx-8 hover:text-[#876AFB] hover:underline" href='/about'>About</Link>
                </nav>
            </header>
            <div className="flex flex-col justify-center items-center py-24 px-12 lg:px-36">
                {children}
            </div>
            <footer className="text-center">
                <div className="text-[#ffffff66]"> © 2023 inQuiry</div>
            </footer>
        </div>
        </>
    )
}