"use client"

import { useState, useEffect } from "react"
import { Layout } from "./components/layout"
import { Dashboard } from "./components/dashboard"
import { UserProfile } from "./components/user-profile"
import { LearningHub } from "./components/learning-hub"
import { AdminPortal } from "./components/admin-portal"
// Import the enhanced scam detection component
import { EnhancedScamDetection } from "./components/enhanced-scam-detection"
// Add import for cybercrime categories
import { CybercrimeCategories } from "./components/cybercrime-categories"
import { useRouter } from "next/navigation";
import ReportScamForm from "./components/report";

export default function App() {
  const [currentPage, setCurrentPage] = useState("dashboard")
  const router = useRouter();
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
    const path = window.location.pathname;
    if (!token && path !== "/login" && path !== "/signup") {
      router.replace("/login");
    } else {
      setAuthChecked(true);
    }
  }, []);

  if (!authChecked && typeof window !== "undefined" && window.location.pathname !== "/login" && window.location.pathname !== "/signup") {
    return null; // Or a loading spinner
  }

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return <Dashboard onNavigate={setCurrentPage}/>
      case "detection":
        return <EnhancedScamDetection />
      case "profile":
        return <UserProfile />
      case "learning":
        return <LearningHub />
      case "admin":
        return <AdminPortal />
      case "categories":
        return <CybercrimeCategories />
      case "report":
        return <ReportScamForm onBack={() => setCurrentPage("dashboard")} />
      default:
        return <Dashboard onNavigate={setCurrentPage}/>
    }
  }

  return <Layout currentPage={currentPage}>{renderPage()}</Layout>
}
