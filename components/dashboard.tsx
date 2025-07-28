"use client"

import { Shield, AlertTriangle, MapPin, Phone, MessageSquare, TrendingUp } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function Dashboard({ onNavigate }: { onNavigate: (page: string) => void }) {
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
        return <Shield className="h-4 w-4 text-shield-green" />
      case "Medium Risk":
        return <AlertTriangle className="h-4 w-4 text-yellow-600" />
      case "Urgent":
        return <AlertTriangle className="h-4 w-4 text-shield-orange" />
      default:
        return <Shield className="h-4 w-4 text-gray-600" />
    }
  }

  // REMOVE THIS PLACEHOLDER FUNCTION:
  // function setCurrentPage(arg0: string): void {
  //   throw new Error("Function not implemented.")
  // }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Your personal protection against AI-powered scams</p>
        </div>
        <div className="flex items-center space-x-2">
          {getRiskIcon(riskLevel)}
          <span className={`font-medium ${getRiskColor(riskLevel)}`}>{riskLevel}</span>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Threats</CardTitle>
            <AlertTriangle className="h-4 w-4 text-shield-orange" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">High Risk</CardTitle>
            <AlertTriangle className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Medium Risk</CardTitle>
            <Shield className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Categories</CardTitle>
            <TrendingUp className="h-4 w-4 text-shield-green" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Alerts</CardTitle>
            <CardDescription>Latest scam activities in your area</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentAlerts.map((alert) => (
              <div key={alert.id} className="flex items-center space-x-4">
                <AlertTriangle className={`h-4 w-4 ${
                  alert.severity === 'high' ? 'text-shield-orange' :
                  alert.severity === 'medium' ? 'text-yellow-600' :
                  'text-blue-600'
                }`} />
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-medium">{alert.type}</p>
                  <p className="text-sm text-muted-foreground">
                    {alert.location} • {alert.time}
                  </p>
                </div>
                <Badge variant={
                  alert.severity === 'high' ? 'destructive' :
                  alert.severity === 'medium' ? 'secondary' :
                  'outline'
                }>
                  {alert.severity}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks and reports</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {/* FIX: Use onNavigate instead of setCurrentPage */}
            <Button onClick={() => onNavigate("report")} className="w-full">
              <AlertTriangle className="mr-2 h-4 w-4" /> Report a Scam
            </Button>
            <Button onClick={() => onNavigate("detection")} className="w-full" variant="outline">
              <Shield className="mr-2 h-4 w-4" /> Scan for Threats
            </Button>
            <Button onClick={() => onNavigate("learning")} className="w-full" variant="outline">
              <MessageSquare className="mr-2 h-4 w-4" /> Learning Hub
            </Button>
          </CardContent>
        </Card>
      </div>

      <Alert>
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>
          Stay vigilant! New AI-powered romance scams have been reported in your area. 
          Always verify identities through video calls before sharing personal information.
        </AlertDescription>
      </Alert>
    </div>
  )
}
