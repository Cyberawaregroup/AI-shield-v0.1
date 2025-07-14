"use client"

import { Shield, AlertTriangle, MapPin, Phone, MessageSquare, TrendingUp } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function Dashboard() {
  const riskLevel = "Safe" // Could be "Safe", "Medium Risk", or "Urgent"
  const recentAlerts = [
    { id: 1, type: "Romance Scam", location: "Downtown Area", time: "2 hours ago", severity: "high" },
    { id: 2, type: "Bank Impersonation", location: "Suburb North", time: "5 hours ago", severity: "medium" },
    { id: 3, type: "Courier Scam", location: "City Center", time: "1 day ago", severity: "low" },
  ]

  const getRiskColor = (level: string) => {
    switch (level) {
      case "Safe":
        return "text-shield-green"
      case "Medium Risk":
        return "text-yellow-600"
      case "Urgent":
        return "text-shield-orange"
      default:
        return "text-gray-600"
    }
  }

  const getRiskIcon = (level: string) => {
    switch (level) {
      case "Safe":
        return <Shield className="h-8 w-8 text-shield-green" />
      case "Medium Risk":
        return <AlertTriangle className="h-8 w-8 text-yellow-600" />
      case "Urgent":
        return <AlertTriangle className="h-8 w-8 text-shield-orange" />
      default:
        return <Shield className="h-8 w-8 text-gray-600" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="text-center py-4">
        <h2 className="text-3xl font-bold text-shield-blue mb-2">Welcome to AI Shield</h2>
        <p className="text-lg text-gray-600">Your personal protection against AI-powered scams</p>
      </div>

      {/* Risk Status Card */}
      <Card className="border-2 shadow-lg">
        <CardHeader className="text-center pb-4">
          <div className="flex justify-center mb-4">{getRiskIcon(riskLevel)}</div>
          <CardTitle className={`text-2xl ${getRiskColor(riskLevel)}`}>Current Status: {riskLevel}</CardTitle>
          <CardDescription className="text-lg">
            {riskLevel === "Safe" && "No immediate threats detected in your area"}
            {riskLevel === "Medium Risk" && "Some scam activity reported nearby"}
            {riskLevel === "Urgent" && "High scam activity - please be extra cautious"}
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Button size="lg" className="h-20 text-xl bg-shield-orange hover:bg-shield-orange/90 text-white">
          <Phone className="h-8 w-8 mr-3" />
          Report Scam Now
        </Button>
        <Button
          size="lg"
          variant="outline"
          className="h-20 text-xl border-2 border-shield-blue text-shield-blue hover:bg-shield-blue hover:text-white bg-transparent"
        >
          <MessageSquare className="h-8 w-8 mr-3" />
          Check Message Safety
        </Button>
      </div>

      {/* Recent Alerts */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-xl">
            <MapPin className="h-6 w-6 mr-2 text-shield-blue" />
            Recent Scam Alerts in Your Area
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentAlerts.map((alert) => (
              <Alert key={alert.id} className="border-l-4 border-l-shield-orange">
                <AlertTriangle className="h-5 w-5" />
                <AlertDescription className="text-base">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold text-shield-blue">{alert.type}</p>
                      <p className="text-gray-600">
                        {alert.location} • {alert.time}
                      </p>
                    </div>
                    <Badge
                      variant={
                        alert.severity === "high"
                          ? "destructive"
                          : alert.severity === "medium"
                            ? "default"
                            : "secondary"
                      }
                      className="text-sm"
                    >
                      {alert.severity.toUpperCase()}
                    </Badge>
                  </div>
                </AlertDescription>
              </Alert>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Access to Learning */}
      <Card className="bg-gradient-to-r from-shield-green/10 to-shield-blue/10">
        <CardHeader>
          <CardTitle className="flex items-center text-xl">
            <TrendingUp className="h-6 w-6 mr-2 text-shield-green" />
            Awareness Center
          </CardTitle>
          <CardDescription className="text-base">
            Learn how to protect yourself with our interactive guides
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button className="w-full md:w-auto bg-shield-green hover:bg-shield-green/90 text-white text-lg py-3 px-6">
            Start Learning Now
          </Button>
        </CardContent>
      </Card>

      {/* Cybercrime Categories Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-xl">
            <Shield className="h-6 w-6 mr-2 text-shield-blue" />
            Threat Categories We Protect Against
          </CardTitle>
          <CardDescription className="text-base">
            Comprehensive coverage across all major cybercrime types
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center p-3 bg-red-50 rounded-lg">
              <p className="text-2xl font-bold text-red-600">4</p>
              <p className="text-sm text-gray-600">Critical Threats</p>
            </div>
            <div className="text-center p-3 bg-orange-50 rounded-lg">
              <p className="text-2xl font-bold text-shield-orange">5</p>
              <p className="text-sm text-gray-600">High Risk</p>
            </div>
            <div className="text-center p-3 bg-yellow-50 rounded-lg">
              <p className="text-2xl font-bold text-yellow-600">3</p>
              <p className="text-sm text-gray-600">Medium Risk</p>
            </div>
            <div className="text-center p-3 bg-shield-green/10 rounded-lg">
              <p className="text-2xl font-bold text-shield-green">12</p>
              <p className="text-sm text-gray-600">Total Categories</p>
            </div>
          </div>
          <Button className="w-full md:w-auto bg-shield-blue hover:bg-shield-blue/90 text-white text-lg py-3 px-6">
            View All Threat Categories
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
