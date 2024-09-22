import { useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const CreateTask = () => {
    const { projectId } = useParams<{ projectId: string }>();

    const ref = useRef(null);
    const navigate = useNavigate();

    const navigateToReadProject = () => {
        navigate(`/projects/${projectId}`);
    };

    useEffect(() => {
        if (ref.current) {
            FRM.listen(
                ref.current,
                navigateToReadProject,
                true,
                {
                    "completed": false,
                    "subtasks": [],
                },
            );
        }
    }, []);

    return (
        <form
            ref={ref}
            action={`${import.meta.env.VITE_API_URL}/projects/${projectId}/tasks`}
            method="POST"
            encType="multipart/form-data"
        >
            <label htmlFor="description">Description:</label>
            <textarea id="description" name="description" placeholder="Task Description"></textarea>
            <button type="submit">Create Task</button>
        </form>
    );
};

export default CreateTask;
