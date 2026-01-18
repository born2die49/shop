import type { Metadata } from "next";
import Image from "next/image";
import shop from "@/../public/assets/images/shop.jpg"

export const metadata:Metadata = {
  title: "Shop Home",
  description: "Shop homepage. Shop anything, ship fast, lock & load." 
}

export default function Home() {
  return (
    <div className="relative h-screen">
      <div className="absolute inset-0 z-0">
        <Image src={shop} alt="Shop" fill style={{objectFit: "cover", objectPosition: "center"}}/>
      </div>
      <main className="flex-center relative h-full bg-black/50">
        <div className="text-center">
          <h1 className="font-googleSans text-5xl text-amber-200">
            Welcome to Shop!
          </h1>
          <p className="font-roboto text-3xl text-amber-100">
            Shop anything!!
          </p>
        </div>
      </main>
    </div>
  );
}
