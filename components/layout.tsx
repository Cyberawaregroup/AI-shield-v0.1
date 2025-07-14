"use client"

import type React from "react"

import { useState } from "react"
import { Shield, Home, Scan, User, BookOpen, Users, Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface LayoutProps {
  children: React.ReactNode
  currentPage: string
}

const navigation = [
  { name: "Dashboard", href: "#", icon: Home, id: "dashboard" },
  { name: "Scam Detection", href: "#", icon: Scan, id: "detection" },
  { name: "Threat Categories", href: "#", icon: Shield, id: "categories" },
  { name: "My Profile", href: "#", icon: User, id: "profile" },
  { name: "Learning Hub", href: "#", icon: BookOpen, id: "learning" },
  { name: "Admin Portal", href: "#", icon: Users, id: "admin" },
]

export function Layout({ children, currentPage }: LayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-shield-light">
      {/* Header */}
      <header className="bg-shield-blue text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <Shield className="h-8 w-8 text-shield-green" />
              <h1 className="text-xl font-bold">AI Shield</h1>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-1">
              {navigation.map((item) => (
                <Button
                  key={item.name}
                  variant={currentPage === item.id ? "secondary" : "ghost"}
                  className={cn(
                    "text-white hover:bg-white/10 text-base px-4 py-2",
                    currentPage === item.id && "bg-white/20",
                  )}
                >
                  <item.icon className="h-5 w-5 mr-2" />
                  {item.name}
                </Button>
              ))}
            </nav>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              className="md:hidden text-white hover:bg-white/10"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-shield-blue border-t border-white/20">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navigation.map((item) => (
                <Button
                  key={item.name}
                  variant="ghost"
                  className={cn(
                    "w-full justify-start text-white hover:bg-white/10 text-lg py-3",
                    currentPage === item.id && "bg-white/20",
                  )}
                >
                  <item.icon className="h-6 w-6 mr-3" />
                  {item.name}
                </Button>
              ))}
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">{children}</main>
    </div>
  )
}
