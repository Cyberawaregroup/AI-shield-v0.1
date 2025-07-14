"use client"

import { User, Shield, TrendingUp, Share2, CheckCircle, AlertCircle } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"

export function UserProfile() {
  const userProfile = {
    name: "Sarah Johnson",
    riskScore: 25, // Out of 100, lower is better
    completedModules: 8,
    totalModules: 12,
    scamHistory: [
      { date: "2024-01-15", type: "Romance Scam Attempt", status: "Avoided", severity: "high" },
      { date: "2024-01-10", type: "Phishing Email", status: "Reported", severity: "medium" },
      { date: "2024-01-05", type: "Fake Tech Support", status: "Avoided", severity: "high" },
    ],
    trustedContacts: ["John Johnson (Son)", "Mary Smith (Neighbor)"],
    alertsEnabled: true,
  }

  const getRiskLevel = (score: number) => {
    if (score <= 30) return { level: "Low Risk", color: "text-shield-green", bgColor: "bg-shield-green/10" }
    if (score <= 60) return { level: "Medium Risk", color: "text-yellow-600", bgColor: "bg-yellow-100" }
    return { level: "High Risk", color: "text-shield-orange", bgColor: "bg-shield-orange/10" }
  }

  const risk = getRiskLevel(userProfile.riskScore)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center py-4">
        <h2 className="text-3xl font-bold text-shield-blue mb-2">My Security Profile</h2>
        <p className="text-lg text-gray-600">Track your protection level and learning progress</p>
      </div>

      {/* Profile Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Score Card */}
        <Card className={`border-2 ${risk.bgColor}`}>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className={`p-4 rounded-full ${risk.bgColor}`}>
                <Shield className={`h-8 w-8 ${risk.color}`} />
              </div>
            </div>
            <CardTitle className={`text-2xl ${risk.color}`}>Risk Score: {userProfile.riskScore}/100</CardTitle>
            <CardDescription className="text-lg">{risk.level}</CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={100 - userProfile.riskScore} className="h-3" />
            <p className="text-sm text-gray-600 mt-2 text-center">Lower scores mean better protection</p>
          </CardContent>
        </Card>

        {/* Learning Progress */}
        <Card>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className="p-4 rounded-full bg-shield-blue/10">
                <TrendingUp className="h-8 w-8 text-shield-blue" />
              </div>
            </div>
            <CardTitle className="text-2xl text-shield-blue">Learning Progress</CardTitle>
            <CardDescription className="text-lg">
              {userProfile.completedModules} of {userProfile.totalModules} modules completed
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={(userProfile.completedModules / userProfile.totalModules) * 100} className="h-3" />
            <p className="text-sm text-gray-600 mt-2 text-center">
              {Math.round((userProfile.completedModules / userProfile.totalModules) * 100)}% Complete
            </p>
          </CardContent>
        </Card>

        {/* Trusted Contacts */}
        <Card>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className="p-4 rounded-full bg-shield-green/10">
                <Share2 className="h-8 w-8 text-shield-green" />
              </div>
            </div>
            <CardTitle className="text-2xl text-shield-green">Trusted Network</CardTitle>
            <CardDescription className="text-lg">{userProfile.trustedContacts.length} trusted contacts</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {userProfile.trustedContacts.map((contact, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <User className="h-4 w-4 text-shield-green" />
                  <span className="text-sm">{contact}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Scam History */}
      <Card>
        <CardHeader>
          <CardTitle className="text-xl flex items-center">
            <Shield className="h-6 w-6 mr-2 text-shield-blue" />
            Recent Security Events
          </CardTitle>
          <CardDescription className="text-base">Your recent encounters with potential scams</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {userProfile.scamHistory.map((event, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-4">
                  {event.status === "Avoided" ? (
                    <CheckCircle className="h-6 w-6 text-shield-green" />
                  ) : (
                    <AlertCircle className="h-6 w-6 text-shield-blue" />
                  )}
                  <div>
                    <p className="font-semibold text-base">{event.type}</p>
                    <p className="text-sm text-gray-600">{event.date}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Badge variant={event.status === "Avoided" ? "default" : "secondary"} className="text-sm">
                    {event.status}
                  </Badge>
                  <Badge variant={event.severity === "high" ? "destructive" : "secondary"} className="text-sm">
                    {event.severity.toUpperCase()}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Alert Settings</CardTitle>
          <CardDescription className="text-base">Manage how you receive security notifications</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold text-base">Share alerts with trusted contacts</p>
              <p className="text-sm text-gray-600">Allow trusted contacts to see your security alerts</p>
            </div>
            <Switch checked={userProfile.alertsEnabled} />
          </div>

          <div className="pt-4 border-t">
            <Button className="w-full md:w-auto bg-shield-blue hover:bg-shield-blue/90 text-white text-lg py-3 px-6">
              Update Emergency Contacts
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
