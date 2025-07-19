import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { AuthProvider, useAuth } from './hooks/useAuth.jsx';
import Layout from './components/Layout';
import LoginForm from './components/LoginForm';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

// React Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// App-Inhalt mit Auth-Context
const AppContent = () => {
  const { isAuthenticated, loading } = useAuth();
  const { t } = useTranslation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{t('loading_application')}</p>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      {/* Öffentliche Routen */}
      <Route 
        path="/login" 
        element={
          isAuthenticated ? <Navigate to="/" replace /> : <LoginForm />
        } 
      />
      
      {/* Geschützte Routen */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/servers"
        element={
          <ProtectedRoute>
            <Layout>
              <div className="text-center py-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{t('server_management')}</h2>
                <p className="text-gray-600">{t('page_coming_soon')}</p>
              </div>
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/users"
        element={
          <ProtectedRoute requireAdmin>
            <Layout>
              <div className="text-center py-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{t('user_management')}</h2>
                <p className="text-gray-600">{t('page_coming_soon')}</p>
              </div>
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/settings"
        element={
          <ProtectedRoute requireAdmin>
            <Layout>
              <div className="text-center py-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{t('settings')}</h2>
                <p className="text-gray-600">{t('page_coming_soon')}</p>
              </div>
            </Layout>
          </ProtectedRoute>
        }
      />
      
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
