import ListProjects from './pages/projects/List';
import CreateProject from './pages/projects/Create';
import ReadProject from './pages/projects/Read';

export default [
    {
        path: "/projects",
        element: <ListProjects />,
    },
    {
        path: "/projects/create",
        element: <CreateProject />,
    },
    {
        path: "/projects/:projectId",
        element: <ReadProject />,
    },
];
