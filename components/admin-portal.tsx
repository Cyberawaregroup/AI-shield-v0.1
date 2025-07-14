"use client"

import { Users, TrendingUp, AlertTriangle, MessageSquare, BarChart3, Shield } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function AdminPortal() {
  const managedUsers = [
    { id: 1, name: "Sarah Johnson", riskLevel: "Low", lastActive: "2 hours ago", alerts: 0 },
    { id: 2, name: "Robert Chen", riskLevel: "Medium", lastActive: "1 day ago", alerts: 2 },
    { id: 3, name: "Maria Garcia", riskLevel: "High", lastActive: "3 days ago", alerts: 5 },
    { id: 4, name: "James Wilson", riskLevel: "Low", lastActive: "5 hours ago", alerts: 1 },
  ]

  const analytics = {
    totalUsers: 24,
    activeThisWeek: 18,
    scamReports: 12,
    topScamTypes: [
      { type: "Romance Scam", count: 5, trend: "up" },
      { type: "Phone Scam", count: 4, trend: "down" },
      { type: "Email Phishing", count: 3, trend: "up" },
    ],
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case "Low":
        return "bg-shield-green text-white"
      case "Medium":
        return "bg-yellow-500 text-white"
      case "High":
        return "bg-shield-orange text-white"
      default:
        return "bg-gray-500 text-white"
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center py-4">
        <h2 className="text-3xl font-bold text-shield-blue mb-2">Admin & Community Portal</h2>
        <p className="text-lg text-gray-600">Manage users and monitor community safety</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Users</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <Users className="h-8 w-8 text-shield-blue" />
              <span className="text-3xl font-bold text-shield-blue">{analytics.totalUsers}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Active This Week</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-8 w-8 text-shield-green" />
              <span className="text-3xl font-bold text-shield-green">{analytics.activeThisWeek}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Scam Reports</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-8 w-8 text-shield-orange" />
              <span className="text-3xl font-bold text-shield-orange">{analytics.scamReports}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Engagement Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-8 w-8 text-shield-blue" />
              <span className="text-3xl font-bold text-shield-blue">75%</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="users" className="w-full">
        <TabsList className="grid w-full grid-cols-2 h-14 text-base">
          <TabsTrigger value="users" className="text-lg">
            Manage Users
          </TabsTrigger>
          <TabsTrigger value="analytics" className="text-lg">
            Analytics
          </TabsTrigger>
        </TabsList>

        {/* User Management */}
        <TabsContent value="users" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl flex items-center">
                <Users className="h-6 w-6 mr-2 text-shield-blue" />
                Managed Users
              </CardTitle>
              <CardDescription className="text-base">Monitor and support users in your care</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {managedUsers.map((user) => (
                  <div
                    key={user.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="p-2 rounded-full bg-shield-blue/10">
                        <Users className="h-6 w-6 text-shield-blue" />
                      </div>
                      <div>
                        <p className="font-semibold text-base">{user.name}</p>
                        <p className="text-sm text-gray-600">Last active: {user.lastActive}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Badge className={getRiskColor(user.riskLevel)}>{user.riskLevel} Risk</Badge>
                      {user.alerts > 0 && (
                        <Badge variant="destructive">
                          {user.alerts} Alert{user.alerts > 1 ? "s" : ""}
                        </Badge>
                      )}
                      <div className="flex space-x-2">
                        <Button size="sm" variant="outline" className="text-sm bg-transparent">
                          <MessageSquare className="h-4 w-4 mr-1" />
                          Check-in
                        </Button>
                        <Button size="sm" className="bg-shield-blue hover:bg-shield-blue/90 text-white text-sm">
                          View Profile
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button className="h-16 text-lg bg-shield-blue hover:bg-shield-blue/90 text-white">
              <Users className="h-6 w-6 mr-2" />
              Add New User
            </Button>
            <Button className="h-16 text-lg bg-shield-orange hover:bg-shield-orange/90 text-white">
              <AlertTriangle className="h-6 w-6 mr-2" />
              Send Alert
            </Button>
            <Button className="h-16 text-lg bg-shield-green hover:bg-shield-green/90 text-white">
              <MessageSquare className="h-6 w-6 mr-2" />
              Bulk Check-in
            </Button>
          </div>
        </TabsContent>

        {/* Analytics */}
        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Scam Types */}
            <Card>
              <CardHeader>
                <CardTitle className="text-xl flex items-center">
                  <BarChart3 className="h-6 w-6 mr-2 text-shield-blue" />
                  Top Scam Types
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analytics.topScamTypes.map((scam, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div>
                        <p className="font-semibold text-base">{scam.type}</p>
                        <p className="text-sm text-gray-600">{scam.count} reports</p>
                      </div>
                      <Badge variant={scam.trend === "up" ? "destructive" : "secondary"} className="text-sm">
                        {scam.trend === "up" ? "↑ Rising" : "↓ Declining"}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* User Engagement */}
            <Card>
              <CardHeader>
                <CardTitle className="text-xl flex items-center">
                  <TrendingUp className="h-6 w-6 mr-2 text-shield-green" />
                  User Engagement
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-base">Learning Modules Completed</span>
                    <span className="font-semibold text-shield-green">156</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-base">Scam Reports Submitted</span>
                    <span className="font-semibold text-shield-blue">23</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-base">Messages Analyzed</span>
                    <span className="font-semibold text-shield-orange">89</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-base">Weekly Active Users</span>
                    <span className="font-semibold text-gray-700">18/24</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Community Safety Status */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl flex items-center">
                <Shield className="h-6 w-6 mr-2 text-shield-green" />
                Community Safety Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div className="p-4 bg-shield-green/10 rounded-lg">
                  <p className="text-2xl font-bold text-shield-green">18</p>
                  <p className="text-sm text-gray-600">Users at Low Risk</p>
                </div>
                <div className="p-4 bg-yellow-100 rounded-lg">
                  <p className="text-2xl font-bold text-yellow-600">4</p>
                  <p className="text-sm text-gray-600">Users at Medium Risk</p>
                </div>
                <div className="p-4 bg-shield-orange/10 rounded-lg">
                  <p className="text-2xl font-bold text-shield-orange">2</p>
                  <p className="text-sm text-gray-600">Users at High Risk</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
