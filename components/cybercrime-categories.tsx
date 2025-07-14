"use client"

import {
  Heart,
  Phone,
  ShoppingCart,
  Briefcase,
  GraduationCap,
  Home,
  Coins,
  Users,
  Mail,
  Wifi,
  Lock,
  AlertTriangle,
  TrendingUp,
  BarChart3,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

export function CybercrimeCategories() {
  const crimeCategories = [
    {
      id: "romance",
      name: "Romance Scams",
      icon: Heart,
      description: "Fake dating profiles and emotional manipulation for financial gain",
      riskLevel: "High",
      commonTargets: ["Seniors", "Divorced individuals", "Lonely people"],
      averageLoss: "$15,000",
      recentTrend: "up",
      indicators: ["Quick declarations of love", "Avoids video calls", "Requests money for emergencies"],
    },
    {
      id: "investment",
      name: "Investment Fraud",
      icon: TrendingUp,
      description: "Fake investment opportunities and Ponzi schemes",
      riskLevel: "Critical",
      commonTargets: ["Retirees", "High-income earners", "Inexperienced investors"],
      averageLoss: "$45,000",
      recentTrend: "up",
      indicators: ["Guaranteed high returns", "Pressure to invest quickly", "Unregistered investments"],
    },
    {
      id: "tech-support",
      name: "Tech Support Scams",
      icon: Phone,
      description: "Fake technical support claiming computer problems",
      riskLevel: "High",
      commonTargets: ["Seniors", "Non-tech savvy users", "Small businesses"],
      averageLoss: "$1,200",
      recentTrend: "stable",
      indicators: ["Unsolicited calls", "Claims of virus infection", "Requests remote access"],
    },
    {
      id: "cryptocurrency",
      name: "Cryptocurrency Scams",
      icon: Coins,
      description: "Fake crypto investments and wallet theft",
      riskLevel: "Critical",
      commonTargets: ["Young adults", "Crypto enthusiasts", "FOMO investors"],
      averageLoss: "$25,000",
      recentTrend: "up",
      indicators: ["Celebrity endorsements", "Get-rich-quick promises", "Fake trading platforms"],
    },
    {
      id: "identity-theft",
      name: "Identity Theft",
      icon: Lock,
      description: "Stealing personal information for fraudulent use",
      riskLevel: "Critical",
      commonTargets: ["All demographics", "Online shoppers", "Social media users"],
      averageLoss: "$5,000",
      recentTrend: "up",
      indicators: ["Phishing emails", "Fake websites", "Data breach notifications"],
    },
    {
      id: "online-shopping",
      name: "Online Shopping Fraud",
      icon: ShoppingCart,
      description: "Fake online stores and non-delivery scams",
      riskLevel: "Medium",
      commonTargets: ["Bargain hunters", "Holiday shoppers", "Social media users"],
      averageLoss: "$800",
      recentTrend: "stable",
      indicators: ["Too-good-to-be-true prices", "No contact information", "Poor website quality"],
    },
    {
      id: "employment",
      name: "Employment Scams",
      icon: Briefcase,
      description: "Fake job offers and work-from-home schemes",
      riskLevel: "Medium",
      commonTargets: ["Job seekers", "Students", "Stay-at-home parents"],
      averageLoss: "$2,000",
      recentTrend: "up",
      indicators: ["Upfront fees required", "Vague job descriptions", "Too-easy requirements"],
    },
    {
      id: "education",
      name: "Education Scams",
      icon: GraduationCap,
      description: "Fake degrees and fraudulent educational institutions",
      riskLevel: "Medium",
      commonTargets: ["Students", "Career changers", "Professionals seeking advancement"],
      averageLoss: "$3,500",
      recentTrend: "stable",
      indicators: ["Unaccredited institutions", "Guaranteed degrees", "No coursework required"],
    },
    {
      id: "real-estate",
      name: "Real Estate Fraud",
      icon: Home,
      description: "Rental scams and fake property investments",
      riskLevel: "High",
      commonTargets: ["Renters", "First-time buyers", "Investors"],
      averageLoss: "$8,000",
      recentTrend: "up",
      indicators: ["Requests for deposits before viewing", "Below-market prices", "Pressure to act quickly"],
    },
    {
      id: "charity",
      name: "Charity Fraud",
      icon: Users,
      description: "Fake charities exploiting disasters and causes",
      riskLevel: "Medium",
      commonTargets: ["Generous individuals", "Disaster victims", "Religious communities"],
      averageLoss: "$500",
      recentTrend: "seasonal",
      indicators: ["High-pressure tactics", "Vague about fund usage", "Similar names to real charities"],
    },
    {
      id: "phishing",
      name: "Phishing Attacks",
      icon: Mail,
      description: "Fake emails and websites to steal credentials",
      riskLevel: "High",
      commonTargets: ["All internet users", "Business employees", "Bank customers"],
      averageLoss: "$3,000",
      recentTrend: "up",
      indicators: ["Urgent action required", "Suspicious links", "Generic greetings"],
    },
    {
      id: "wifi",
      name: "Wi-Fi & Network Scams",
      icon: Wifi,
      description: "Fake hotspots and network intrusions",
      riskLevel: "Medium",
      commonTargets: ["Public Wi-Fi users", "Travelers", "Remote workers"],
      averageLoss: "$1,500",
      recentTrend: "stable",
      indicators: ["Unsecured networks", "Fake hotspot names", "Unexpected network requests"],
    },
  ]

  const getRiskColor = (level: string) => {
    switch (level) {
      case "Critical":
        return "bg-red-600 text-white"
      case "High":
        return "bg-shield-orange text-white"
      case "Medium":
        return "bg-yellow-500 text-white"
      case "Low":
        return "bg-blue-500 text-white"
      default:
        return "bg-gray-500 text-white"
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return <TrendingUp className="h-4 w-4 text-red-500" />
      case "down":
        return <BarChart3 className="h-4 w-4 text-green-500 rotate-180" />
      case "stable":
        return <BarChart3 className="h-4 w-4 text-gray-500" />
      case "seasonal":
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      default:
        return <BarChart3 className="h-4 w-4 text-gray-500" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center py-4">
        <h2 className="text-3xl font-bold text-shield-blue mb-2">Cybercrime Categories</h2>
        <p className="text-lg text-gray-600">Comprehensive protection against all types of digital fraud</p>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {crimeCategories.map((category) => (
          <Card key={category.id} className="hover:shadow-lg transition-shadow border-2">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-3 rounded-full bg-shield-blue/10">
                    <category.icon className="h-6 w-6 text-shield-blue" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{category.name}</CardTitle>
                    <div className="flex items-center space-x-2 mt-1">
                      <Badge className={getRiskColor(category.riskLevel)}>{category.riskLevel}</Badge>
                      {getTrendIcon(category.recentTrend)}
                    </div>
                  </div>
                </div>
              </div>
              <CardDescription className="text-base mt-2">{category.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-600">Avg. Loss:</span>
                  <p className="font-semibold text-shield-orange">{category.averageLoss}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-600">Trend:</span>
                  <p className="font-semibold capitalize">{category.recentTrend}</p>
                </div>
              </div>

              <div>
                <span className="font-medium text-gray-600 text-sm">Common Targets:</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {category.commonTargets.map((target, i) => (
                    <Badge key={i} variant="outline" className="text-xs">
                      {target}
                    </Badge>
                  ))}
                </div>
              </div>

              <div>
                <span className="font-medium text-gray-600 text-sm">Warning Signs:</span>
                <ul className="mt-1 space-y-1">
                  {category.indicators.slice(0, 2).map((indicator, i) => (
                    <li key={i} className="flex items-start space-x-2 text-xs">
                      <AlertTriangle className="h-3 w-3 text-shield-orange mt-0.5 flex-shrink-0" />
                      <span>{indicator}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <Button className="w-full bg-shield-blue hover:bg-shield-blue/90 text-white text-sm py-2" size="sm">
                Learn Protection Tips
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Summary Statistics */}
      <Card className="bg-gradient-to-r from-shield-blue/10 to-shield-green/10">
        <CardHeader>
          <CardTitle className="text-xl text-center">Protection Coverage</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-shield-blue">{crimeCategories.length}</p>
              <p className="text-sm text-gray-600">Threat Categories</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-shield-orange">
                {crimeCategories.filter((c) => c.riskLevel === "Critical").length}
              </p>
              <p className="text-sm text-gray-600">Critical Threats</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-shield-green">24/7</p>
              <p className="text-sm text-gray-600">Monitoring</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-purple-600">98.7%</p>
              <p className="text-sm text-gray-600">Detection Rate</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
