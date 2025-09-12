import { TrendingUp, Calculator, BarChart3, Shield, Globe, AlertTriangle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function AdvancedAnalytics() {
  const analyticsCards = [
    {
      icon: Calculator,
      title: "Advanced Fraud Score",
      description: "Comprehensive fraud risk calculation",
      color: "bg-gradient-to-r from-purple-600 to-indigo-600"
    },
    {
      icon: BarChart3,
      title: "Comprehensive Dashboard",
      description: "Executive security overview",
      color: "bg-gradient-to-r from-teal-500 to-cyan-500"
    }
  ];

  const platformStats = [
    {
      icon: Shield,
      label: "Breach Records",
      value: "15B+",
      color: "text-blue-400"
    },
    {
      icon: Globe,
      label: "Social Platforms",
      value: "50+",
      color: "text-green-400"
    },
    {
      icon: AlertTriangle,
      label: "AI Models",
      value: "Advanced",
      color: "text-purple-400"
    },
    {
      icon: TrendingUp,
      label: "Threat Detection",
      value: "Real-time",
      color: "text-orange-400"
    }
  ];

  return (
    <div className="space-y-6">
      <Card className="bg-gradient-to-br from-indigo-900/20 to-purple-900/20 border-indigo-300/20 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <CardTitle className="text-xl text-white">Advanced Analytics</CardTitle>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-4">
          {analyticsCards.map((card, index) => (
            <div key={index} className={`${card.color} p-4 rounded-lg shadow-lg`}>
              <div className="flex items-center gap-3">
                <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                  <card.icon className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">{card.title}</h3>
                  <p className="text-white/80 text-sm">{card.description}</p>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="bg-gradient-to-br from-gray-900/40 to-purple-900/20 border-gray-300/20 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-r from-gray-600 to-purple-600 rounded-lg">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <CardTitle className="text-xl text-white">Platform Stats</CardTitle>
          </div>
        </CardHeader>
        
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            {platformStats.map((stat, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                <div className="flex items-center gap-3">
                  <stat.icon className={`w-4 h-4 ${stat.color}`} />
                  <span className="text-gray-300 text-sm">{stat.label}</span>
                </div>
                <span className="text-white font-semibold">{stat.value}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}