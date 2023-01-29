import Head from "next/head";
import Link from "next/link";
import { ReactNode } from "react";
import { useState } from 'react'

interface Props {
    searchTerm: string
  }

export default function Layout({ searchTerm }: Props) {
    const [term, setTerm] = useState(searchTerm)
    return (
        <form className="flex items-center py-14">   
            <label className="sr-only">Search</label>
            <div className="relative w-full">
                <div className="absolute inset-y-0 left-1 flex items-center pl-4 pointer-events-none">
                    <svg aria-hidden="true" className="w-5 h-5 text-[#ffffffAA]" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path></svg>
                </div>
                <input type="text" onChange={(val) => setTerm(val.target.value)} id="simple-search" className="bg-[#ffffff22] text-[#ffffffAA] text-[1.25rem] outline-none ring-transparent rounded-lg block w-full lg:mr-[40rem] md:mr-[20rem] sm:mr-[10rem] py-3 pl-12" placeholder="How does the internet feel about..." defaultValue={term} required/>
            </div>
            <a href={`/results/${term}`}>
            <button type="button" className="p-3 ml-2 text-xl font-medium text-white bg-[#603BF4] rounded-lg border border-transparent hover:bg-[#4A28D2] focus:ring-4 focus:outline-none focus:ring-[#876AFB]">
                <svg className="w-[1.75rem] h-[1.75rem]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                <span className="sr-only">Search</span>
            </button>
            </a>
            
        </form>
    )
}