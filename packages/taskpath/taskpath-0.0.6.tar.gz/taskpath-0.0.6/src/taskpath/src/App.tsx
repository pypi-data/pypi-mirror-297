import { HashRouter as Router, Routes, Route } from 'react-router-dom';

import PrivateRoute from './components/PrivateRoute';
import PublicRoute from './components/PublicRoute';

import Layout from './Layout';

import LandingPage from './pages/LandingPage';
import HowItWorks from './pages/HowItWorks';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';
import CheckEmail from './pages/CheckEmail';
import SignedIn from './pages/SignedIn';
import ListProjects from './pages/projects/List';
import CreateProject from './pages/projects/Create';
import ReadProject from './pages/projects/Read';
import CreateTask from './pages/tasks/Create';
import ContactUs from './pages/ContactUs';
import PrivacyPolicy from './pages/PrivacyPolicy';

import { AuthProvider } from './AuthContext';
import './global.css';

const App = () => {
    return (
        <Router>
            <AuthProvider>
                <Layout>
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/how-it-works" element={<HowItWorks />} />
                        <Route path="/sign-in" element={<PublicRoute element={<SignIn />} />} />
                        <Route path="/sign-up" element={<PublicRoute element={<SignUp />} />} />
                        <Route path="/check-email/:type" element={<PublicRoute element={<CheckEmail />} />} />
                        <Route path="/signed-in" element={<SignedIn />} />
                        <Route path="/projects" element={<PrivateRoute element={<ListProjects />} />} />
                        <Route path="/projects/create" element={<PrivateRoute element={<CreateProject />} />} />
                        <Route path="/projects/:projectId" element={<PrivateRoute element={<ReadProject />} />} />
                        <Route path="/projects/:projectId/tasks/create" element={<PrivateRoute element={<CreateTask />} />} />
                        <Route path="/contact-us" element={<ContactUs />} />
                        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
                    </Routes>
                </Layout>
            </AuthProvider>
        </Router>
  );
};

export default App;
