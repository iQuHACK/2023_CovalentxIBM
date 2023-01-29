import Head from "next/head";
import Link from "next/link";
import Image from "next/image";
import { ReactNode } from "react";
import useSWR from 'swr'

const fetcher = (...args: any[]) => fetch(...args).then(res => res.json())

export default function ResultsData() {
    const { data, error, isLoading } = useSWR('127.0.0.1:5000', fetcher)
    if (error) return <div>failed to load</div>
    if (isLoading) return <div>loading...</div>

    if (data) {
        let sum = 0
        data.foreach(entry => {
            sum += entry['sentiment']
        })
    
        let average_sentiment = sum / data.length
        let average_sentiment_percent = (sum / data.length) * 100
        return (
            <>
                <div className="pt-14 w-full px-24">
                    <div className="w-full bg-gray-200 rounded-full dark:bg-gray-700">
                        <div className="bg-gradient-to-tl from-[#FF71BE] via-[#B871FF] to-[#3183FF] text-xs font-lg text-blue-100 text-center p-0.5 py-6 leading-none rounded-full" style={{width: "73%"}}></div>
                    </div>
                    <div className={`relative ml-[calc(${average_sentiment_percent}%)]`}>
                        <div className="absolute bg-gray-300 h-8 w-8 rounded-sm rotate-45" ></div>
                        <div className="relative top-2 right-12 bg-gray-300 h-14 w-32 rounded-lg flex items-center justify-center" >
                            <h2 className="text-black font-semibold">{average_sentiment_percent}% positive</h2>
                        </div>
                    </div>
                </div>
                <h2 className="mt-12 mb-8 text-center text-4xl font-medium">Keyword Analysis</h2>
                <ul>
                    {data.map(entry => (
                        <li className="text-2xl py-4">{entry['keyword']} <span className="font-bitcount ml-8"><span className="bg-gradient-to-tr from-[#FF71BE] via-[#B871FF] to-[#3183FF] bg-clip-text text-transparent font-bold">{entry['sentiment'] * 100}%</span> positive</span></li>
                    ))}
                </ul>
            </>
        )
    }
}