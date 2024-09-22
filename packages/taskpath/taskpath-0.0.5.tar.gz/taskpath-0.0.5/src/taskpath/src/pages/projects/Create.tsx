import { useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const CreateProject = () => {
    const ref = useRef(null);
    const navigate = useNavigate();

    const navigateToProjectList = () => {
        navigate('/projects');
    };

    useEffect(() => {
        if (ref.current) {
            FRM.listen(ref.current, navigateToProjectList, true);
        }
    }, []);

    return (
        <>
            <form
                ref={ref}
                action={`${import.meta.env.VITE_API_URL}/projects`}
                method="POST"
                encType="multipart/form-data"
            >
                <label htmlFor="title">Title:</label>
                <input id="title" type="text" name="title" placeholder="Task Title" required />
                <label htmlFor="description">Description:</label>
                <textarea id="description" name="description" placeholder="Task Description"></textarea>
                <button type="submit">Create Task</button>
            </form>
        </>
    );
};

export default CreateProject;
