"use client"

import { useState } from "react"
import { Layout } from "./components/layout"
import { Dashboard } from "./components/dashboard"
import { UserProfile } from "./components/user-profile"
import { LearningHub } from "./components/learning-hub"
import { AdminPortal } from "./components/admin-portal"
// Import the enhanced scam detection component
import { EnhancedScamDetection } from "./components/enhanced-scam-detection"
// Add import for cybercrime categories
import { CybercrimeCategories } from "./components/cybercrime-categories"

export default function App() {
  const [currentPage, setCurrentPage] = useState("dashboard")

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return <Dashboard />
      case "detection":
        return <EnhancedScamDetection />
      case "profile":
        return <UserProfile />
      case "learning":
        return <LearningHub />
      case "admin":
        return <AdminPortal />
      // Add the new case in renderPage function:
      case "categories":
        return <CybercrimeCategories />
      default:
        return <Dashboard />
    }
  }

  return <Layout currentPage={currentPage}>{renderPage()}</Layout>
}
