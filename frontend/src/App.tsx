import Navbar from "./components/Navbar";
import Footer from "./components/sections/Footer";
import Hero from "./components/sections/Hero";
import LeadForm from "./components/sections/LeadForm";
import Pricing from "./components/sections/Pricing";
import Reviews from "./components/sections/Reviews";
import Teachers from "./components/sections/Teachers";
import TestWizard from "./components/sections/TestWizard";
import { LeadProvider } from "./store";

export default function App() {
  return (
    <LeadProvider>
      <Navbar />
      <main>
        <Hero />
        <Teachers />
        <Reviews />
        <Pricing />
        <TestWizard />
        <LeadForm />
      </main>
      <Footer />
    </LeadProvider>
  );
}
