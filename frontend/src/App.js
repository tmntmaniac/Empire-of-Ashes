import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "@/components/Layout";
import Landing from "@/pages/Landing";
import ArmyManager from "@/pages/ArmyManager";
import Builder from "@/pages/Builder";
import PrintView from "@/pages/PrintView";
import Impressum from "@/pages/legal/Impressum";
import Datenschutz from "@/pages/legal/Datenschutz";
import { Toaster } from "sonner";

export default function App() {
    return (
        <BrowserRouter>
            <Toaster position="top-right" theme="dark" />
            <Routes>
                <Route path="/print/:id" element={<PrintView />} />
                <Route element={<Layout />}>
                    <Route path="/" element={<Landing />} />
                    <Route path="/armies" element={<ArmyManager />} />
                    <Route path="/builder/:id" element={<Builder />} />
                    <Route path="/legal/impressum" element={<Impressum />} />
                    <Route path="/legal/datenschutz" element={<Datenschutz />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}
