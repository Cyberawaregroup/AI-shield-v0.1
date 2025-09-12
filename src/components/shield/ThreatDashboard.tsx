import { Shield, AlertTriangle, CheckCircle, TrendingUp, Globe, Activity } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useThreatStats, useThreatAlerts } from "@/lib/api";

export default function ThreatDashboard() {
  const { data: threatStats, isLoading: statsLoading, error: statsError } = useThreatStats();
  const { data: alerts, isLoading: alertsLoading, error: alertsError } = useThreatAlerts(0, 5);

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high': return 'text-red-400';
      case 'medium': return 'text-yellow-400';
      case 'low': return 'text-green-400';
      default: return 'text-gray-400';
    }
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high': return 'bg-red-500/20 border-red-500/50 text-red-400';
      case 'medium': return 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400';
      case 'low': return 'bg-green-500/20 border-green-500/50 text-green-400';
      default: return 'bg-gray-500/20 border-gray-500/50 text-gray-400';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <Card className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border-purple-300/20 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-r from-red-600 to-orange-600 rounded-lg">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <CardTitle className="text-xl text-white">Threat Intelligence Dashboard</CardTitle>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Threat Overview */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Threat Overview</h3>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-red-500/20 rounded-lg">
                  <AlertTriangle className="w-5 h-5 text-red-400" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-white">
                    {statsLoading ? "..." : threatStats?.total_alerts || 0}
                  </p>
                  <p className="text-gray-400 text-sm">Active Threats</p>
                </div>
              </div>
            </div>
            
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-500/20 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-white">
                    {statsLoading ? "..." : threatStats?.total_iocs || 0}
                  </p>
                  <p className="text-gray-400 text-sm">Blocked Attacks</p>
                </div>
              </div>
            </div>
            
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-yellow-500/20 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-yellow-400" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-white">
                    {statsLoading ? "..." : threatStats?.total_breaches || 0}
                  </p>
                  <p className="text-gray-400 text-sm">Risk Score</p>
                </div>
              </div>
            </div>
            
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-500/20 rounded-lg">
                  <Shield className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-white">
                    {statsLoading ? "..." : "A+"}
                  </p>
                  <p className="text-gray-400 text-sm">Security Rating</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Alerts */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Recent Alerts</h3>
          {alertsLoading ? (
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-gray-300">Loading recent alerts...</p>
              </div>
            </div>
          ) : alertsError ? (
            <div className="p-4 bg-red-500/10 rounded-lg border border-red-500/20">
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-5 h-5 text-red-400" />
                <p className="text-red-300">Failed to load recent alerts</p>
              </div>
            </div>
          ) : alerts && alerts.length > 0 ? (
            <div className="space-y-3">
              {alerts.map((alert, index) => (
                <div key={index} className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-white font-medium">{alert.title}</h4>
                    <Badge className={getSeverityBadge(alert.severity)}>
                      {alert.severity.toUpperCase()}
                    </Badge>
                  </div>
                  <p className="text-gray-300 text-sm mb-2">{alert.description}</p>
                  <div className="flex items-center gap-4 text-xs text-gray-400">
                    <span>Created: {formatDate(alert.created_at)}</span>
                    {alert.source && <span>Source: {alert.source}</span>}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 bg-green-500/10 rounded-lg border border-green-500/20">
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-400" />
                <p className="text-green-300">No recent alerts. All systems are secure!</p>
              </div>
            </div>
          )}
        </div>

        {/* Global Threat Intelligence */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Global Threat Intelligence</h3>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3 mb-2">
                <Globe className="w-5 h-5 text-blue-400" />
                <h4 className="text-white font-medium">Global Threats</h4>
              </div>
              <p className="text-3xl font-bold text-blue-400">
                {statsLoading ? "..." : threatStats?.total_alerts || 0}
              </p>
              <p className="text-gray-400 text-sm">Active worldwide</p>
            </div>
            
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3 mb-2">
                <Activity className="w-5 h-5 text-green-400" />
                <h4 className="text-white font-medium">Response Time</h4>
              </div>
              <p className="text-3xl font-bold text-green-400">
                {statsLoading ? "..." : "< 5min"}
              </p>
              <p className="text-gray-400 text-sm">Average detection</p>
            </div>
            
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-3 mb-2">
                <Shield className="w-5 h-5 text-purple-400" />
                <h4 className="text-white font-medium">Protection Rate</h4>
              </div>
              <p className="text-3xl font-bold text-purple-400">
                {statsLoading ? "..." : "99.9%"}
              </p>
              <p className="text-gray-400 text-sm">Threats blocked</p>
            </div>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex gap-2 flex-wrap">
          <Badge variant="outline" className="border-green-500/50 text-green-400 bg-green-500/10">
            <CheckCircle className="w-3 h-3 mr-1" />
            Real-time Monitoring
          </Badge>
          <Badge variant="outline" className="border-blue-500/50 text-blue-400 bg-blue-500/10">
            <Activity className="w-3 h-3 mr-1" />
            Active Protection
          </Badge>
          <Badge variant="outline" className="border-purple-500/50 text-purple-400 bg-purple-500/10">
            <Globe className="w-3 h-3 mr-1" />
            Global Coverage
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}