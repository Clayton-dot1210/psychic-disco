import Navbar from "@/components/navbar";
import Hero from "@/components/hero";
import Services from "@/components/services";
import Portfolio from "@/components/portfolio";
import Packages from "@/components/packages";
import Shoots from "@/components/shoots";
import Process from "@/components/process";
import Contact from "@/components/contact";
import Footer from "@/components/footer";

export default function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <Services />
      <Portfolio />
      <Packages />
      <Shoots />
      <Process />
      <Contact />
      <Footer />
    </>
  );
}
