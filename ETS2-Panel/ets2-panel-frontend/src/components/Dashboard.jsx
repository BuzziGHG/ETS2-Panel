import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.jsx';
import { serverAPI } from '../lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Server,
  Users,
  Play,
  Square,
  RotateCcw,
  Plus,
  Activity,
  Truck,
  AlertCircle,
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchServers();
  }, []);

  const fetchServers = async () => {
    try {
      setLoading(true);
      const response = await serverAPI.getServers();
      setServers(response.data.servers);
    } catch (err) {
      setError('Fehler beim Laden der Server');
      console.error('Error fetching servers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleServerAction = async (serverId, action) => {
    try {
      let response;
      switch (action) {
        case 'start':
          response = await serverAPI.startServer(serverId);
          break;
        case 'stop':
          response = await serverAPI.stopServer(serverId);
          break;
        case 'restart':
          response = await serverAPI.restartServer(serverId);
          break;
        default:
          return;
      }
      
      // Server-Liste aktualisieren
      await fetchServers();
    } catch (err) {
      console.error(`Error ${action}ing server:`, err);
      setError(`Fehler beim ${action === 'start' ? 'Starten' : action === 'stop' ? 'Stoppen' : 'Neustarten'} des Servers`);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'running':
        return <Badge className="bg-green-100 text-green-800">Läuft</Badge>;
      case 'stopped':
        return <Badge variant="secondary">Gestoppt</Badge>;
      case 'starting':
        return <Badge className="bg-yellow-100 text-yellow-800">Startet</Badge>;
      case 'stopping':
        return <Badge className="bg-orange-100 text-orange-800">Stoppt</Badge>;
      default:
        return <Badge variant="outline">Unbekannt</Badge>;
    }
  };

  const runningServers = servers.filter(server => server.status === 'running').length;
  const totalServers = servers.length;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Activity className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Lade Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Willkommen zurück, {user?.username}!</p>
        </div>
        <Link to="/servers/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Neuer Server
          </Button>
        </Link>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Gesamt Server</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalServers}</div>
            <p className="text-xs text-muted-foreground">
              Alle Ihre ETS2 Server
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Aktive Server</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{runningServers}</div>
            <p className="text-xs text-muted-foreground">
              Derzeit laufende Server
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Benutzerrolle</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold capitalize">{user?.role}</div>
            <p className="text-xs text-muted-foreground">
              Ihre Berechtigung
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Server List */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Truck className="mr-2 h-5 w-5" />
            Ihre Server
          </CardTitle>
          <CardDescription>
            Verwalten Sie Ihre ETS2 Dedicated Server
          </CardDescription>
        </CardHeader>
        <CardContent>
          {servers.length === 0 ? (
            <div className="text-center py-8">
              <Truck className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Keine Server vorhanden
              </h3>
              <p className="text-gray-600 mb-4">
                Erstellen Sie Ihren ersten ETS2 Server, um zu beginnen.
              </p>
              <Link to="/servers/new">
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  Server erstellen
                </Button>
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {servers.map((server) => (
                <div
                  key={server.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <h3 className="text-lg font-medium text-gray-900">
                        {server.name}
                      </h3>
                      {getStatusBadge(server.status)}
                    </div>
                    <p className="text-sm text-gray-600 mt-1">
                      {server.description || 'Keine Beschreibung'}
                    </p>
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                      <span>Port: {server.port}</span>
                      <span>Max. Spieler: {server.max_players}</span>
                      {server.owner && (
                        <span>Besitzer: {server.owner}</span>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {server.status === 'stopped' && (
                      <Button
                        size="sm"
                        onClick={() => handleServerAction(server.id, 'start')}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <Play className="h-4 w-4" />
                      </Button>
                    )}
                    
                    {server.status === 'running' && (
                      <>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleServerAction(server.id, 'restart')}
                        >
                          <RotateCcw className="h-4 w-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleServerAction(server.id, 'stop')}
                        >
                          <Square className="h-4 w-4" />
                        </Button>
                      </>
                    )}
                    
                    <Link to={`/servers/${server.id}`}>
                      <Button size="sm" variant="outline">
                        Details
                      </Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;

