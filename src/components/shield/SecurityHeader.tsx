import { Shield, Activity, Bell, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

export default function SecurityHeader() {
  return (
    <header className="bg-gradient-to-r from-purple-900 via-purple-800 to-blue-900 text-white">
      <div className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-white/10 rounded-lg backdrop-blur-sm">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">AI Shield Sentinel</h1>
              <p className="text-purple-200">Complete Cybersecurity Command Center</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" className="text-white hover:bg-white/10">
              <Bell className="w-5 h-5" />
            </Button>
            <Button variant="ghost" size="icon" className="text-white hover:bg-white/10">
              <Activity className="w-5 h-5" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-4 gap-4 mb-8">
          <Badge className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2">
            15+ Billion Records
          </Badge>
          <Badge className="bg-green-600 hover:bg-green-700 text-white px-4 py-2">
            50+ Social Platforms
          </Badge>
          <Badge className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2">
            AI-Powered Analysis
          </Badge>
          <Badge className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2">
            Real-time Monitoring
          </Badge>
        </div>
      </div>
    </header>
  );
}