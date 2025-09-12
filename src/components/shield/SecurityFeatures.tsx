import { useState } from "react";
import { Shield, AlertTriangle, CheckCircle, Globe, Link, Loader2, Eye, EyeOff } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useIPReputationCheck, usePhishingCheck } from "@/lib/api";
import { toast } from "sonner";

export default function SecurityFeatures() {
  const [ipAddress, setIpAddress] = useState("");
  const [url, setUrl] = useState("");
  const [isCheckingIP, setIsCheckingIP] = useState(false);
  const [isCheckingURL, setIsCheckingURL] = useState(false);

  const { data: ipReputation, isLoading: ipLoading, error: ipError, refetch: refetchIP } = useIPReputationCheck(ipAddress, isCheckingIP);
  const { mutate: checkPhishing, isPending: phishingPending } = usePhishingCheck();

  const securityFeatures = [
    {
      icon: Shield,
      title: "Advanced Phishing Test",
      description: "Real-time URL analysis against known phishing databases",
      status: "Active",
      color: "text-green-400"
    },
    {
      icon: Globe,
      title: "IP Reputation Check",
      description: "Comprehensive IP threat analysis and reputation scoring",
      status: "Active",
      color: "text-blue-400"
    },
    {
      icon: Eye,
      title: "Security Dashboard",
      description: "Real-time threat monitoring and response system",
      status: "Active",
      color: "text-purple-400"
    }
  ];

  const handleIPCheck = async () => {
    if (!ipAddress || !ipAddress.match(/^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/)) {
      toast.error("Please enter a valid IP address");
      return;
    }
    
    setIsCheckingIP(true);
    try {
      await refetchIP();
      if (ipReputation && ipReputation.abuse_confidence_score > 50) {
        toast.warning(`IP ${ipAddress} has a high abuse confidence score!`);
      } else {
        toast.success(`IP ${ipAddress} appears to be safe.`);
      }
    } catch (error) {
      toast.error("Failed to check IP reputation. Please try again.");
    } finally {
      setIsCheckingIP(false);
    }
  };

  const handleURLCheck = async () => {
    if (!url || !url.includes('http')) {
      toast.error("Please enter a valid URL starting with http:// or https://");
      return;
    }
    
    setIsCheckingURL(true);
    checkPhishing({ url }, {
      onSuccess: (data) => {
        if (data.is_phishing) {
          toast.error(`⚠️ PHISHING DETECTED! This URL is malicious.`);
        } else {
          toast.success(`✅ URL appears safe. No threats detected.`);
        }
        setIsCheckingURL(false);
      },
      onError: (error) => {
        toast.error("Failed to check URL. Please try again.");
        setIsCheckingURL(false);
      }
    });
  };

  const getAbuseScoreColor = (score: number) => {
    if (score >= 80) return 'text-red-400';
    if (score >= 50) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getAbuseScoreBadge = (score: number) => {
    if (score >= 80) return 'bg-red-500/20 border-red-500/50 text-red-400';
    if (score >= 50) return 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400';
    return 'bg-green-500/20 border-green-500/50 text-green-400';
  };

  return (
    <Card className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border-purple-300/20 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-r from-green-600 to-blue-600 rounded-lg">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <CardTitle className="text-xl text-white">Security Features</CardTitle>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Feature Status */}
        <div className="space-y-3">
          {securityFeatures.map((feature, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
              <div className="flex items-center gap-3">
                <feature.icon className={`w-5 h-5 ${feature.color}`} />
                <div>
                  <p className="text-white font-medium text-sm">{feature.title}</p>
                  <p className="text-gray-400 text-xs">{feature.description}</p>
                </div>
              </div>
              <Badge variant="outline" className="border-green-500/50 text-green-400 bg-green-500/10">
                {feature.status}
              </Badge>
            </div>
          ))}
        </div>

        {/* IP Reputation Check */}
        <div className="p-4 bg-white/5 rounded-lg border border-white/10">
          <h3 className="text-white font-medium mb-3">IP Reputation Check</h3>
          <div className="flex gap-2 mb-3">
            <Input
              type="text"
              value={ipAddress}
              onChange={(e) => setIpAddress(e.target.value)}
              placeholder="Enter IP address (e.g., 192.168.1.1)"
              className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              onKeyPress={(e) => e.key === 'Enter' && handleIPCheck()}
            />
            <Button 
              onClick={handleIPCheck}
              disabled={ipLoading || isCheckingIP}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
            >
              {ipLoading || isCheckingIP ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Eye className="w-4 h-4" />
              )}
            </Button>
          </div>

          {/* IP Results */}
          {ipLoading && (
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
              <p className="text-gray-300">Checking IP reputation...</p>
            </div>
          )}

          {ipError && (
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-red-400" />
              <p className="text-red-300">Failed to check IP reputation</p>
            </div>
          )}

          {ipReputation && (
            <div className="space-y-3 p-3 bg-white/5 rounded-lg">
              <div className="flex items-center justify-between">
                <h4 className="text-white font-medium">IP: {ipReputation.ip_address}</h4>
                <Badge className={getAbuseScoreBadge(ipReputation.abuse_confidence_score)}>
                  {ipReputation.abuse_confidence_score}% Abuse Score
                </Badge>
              </div>
              
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-400">Country</p>
                  <p className="text-white">{ipReputation.country_code || 'Unknown'}</p>
                </div>
                <div>
                  <p className="text-gray-400">ISP</p>
                  <p className="text-white">{ipReputation.isp || 'Unknown'}</p>
                </div>
                <div>
                  <p className="text-gray-400">Usage Type</p>
                  <p className="text-white">{ipReputation.usage_type || 'Unknown'}</p>
                </div>
                <div>
                  <p className="text-gray-400">Total Reports</p>
                  <p className="text-white">{ipReputation.total_reports || 0}</p>
                </div>
              </div>

              {ipReputation.abuse_confidence_score > 50 && (
                <div className="p-2 bg-red-500/20 rounded-lg border border-red-500/30">
                  <p className="text-red-300 text-sm">
                    ⚠️ This IP has been reported multiple times and may be associated with malicious activity.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Phishing URL Check */}
        <div className="p-4 bg-white/5 rounded-lg border border-white/10">
          <h3 className="text-white font-medium mb-3">Phishing URL Detection</h3>
          <div className="flex gap-2 mb-3">
            <Input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter URL to check (e.g., https://example.com)"
              className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              onKeyPress={(e) => e.key === 'Enter' && handleURLCheck()}
            />
            <Button 
              onClick={handleURLCheck}
              disabled={phishingPending || isCheckingURL}
              className="bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white"
            >
              {phishingPending || isCheckingURL ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Link className="w-4 h-4" />
              )}
            </Button>
          </div>

          {isCheckingURL && (
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 animate-spin text-orange-400" />
              <p className="text-gray-300">Analyzing URL for threats...</p>
            </div>
          )}
        </div>

        {/* Advanced Analytics */}
        <div className="p-4 bg-white/5 rounded-lg border border-white/10">
          <h3 className="text-white font-medium mb-3">Advanced Analytics</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 bg-white/5 rounded-lg">
              <div className="text-2xl font-bold text-green-400">99.9%</div>
              <div className="text-gray-300 text-sm">Threat Detection Rate</div>
            </div>
            <div className="text-center p-3 bg-white/5 rounded-lg">
              <div className="text-2xl font-bold text-blue-400">&lt; 5min</div>
              <div className="text-gray-300 text-sm">Average Response Time</div>
            </div>
          </div>
        </div>

        {/* Platform Stats */}
        <div className="p-4 bg-white/5 rounded-lg border border-white/10">
          <h3 className="text-white font-medium mb-3">Platform Stats</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 bg-white/5 rounded-lg">
              <div className="text-xl font-bold text-purple-400">15B+</div>
              <div className="text-gray-300 text-sm">Breach Records</div>
            </div>
            <div className="text-center p-3 bg-white/5 rounded-lg">
              <div className="text-xl font-bold text-blue-400">50+</div>
              <div className="text-gray-300 text-sm">Social Platforms</div>
            </div>
            <div className="text-center p-3 bg-white/5 rounded-lg">
              <div className="text-xl font-bold text-green-400">24/7</div>
              <div className="text-gray-300 text-sm">AI Models</div>
            </div>
            <div className="text-center p-3 bg-white/5 rounded-lg">
              <div className="text-xl font-bold text-orange-400">Real-time</div>
              <div className="text-gray-300 text-sm">Threat Detection</div>
            </div>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex gap-2 flex-wrap">
          <Badge variant="outline" className="border-green-500/50 text-green-400 bg-green-500/10">
            <CheckCircle className="w-3 h-3 mr-1" />
            All Systems Active
          </Badge>
          <Badge variant="outline" className="border-blue-500/50 text-blue-400 bg-blue-500/10">
            <Shield className="w-3 h-3 mr-1" />
            Real-time Protection
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