import { FC } from 'react';
import './Task.css';

interface ITask {
    id: string;
    description: string;
    completed: boolean;
    subtasks: ITask[];
}

interface Props extends ITask {
    level: number;
}

const Task: FC<Props> = ({ id, description, completed, subtasks, level }) => {
    let className = "description";
    if (completed) {
        className += " completed";
    }
    return (
        <>
            <div className="task" style={{ paddingLeft: `${level}em` }}>
                <span className={className}>{description}</span>
                <div className="controls">
                    <button className="link" onClick={() => console.log('Task completed:', id)}>Done</button>
                    <button className="link" onClick={() => console.log('Edit task:', id)}>Edit</button>
                    <button className="link" onClick={() => console.log("Expand task", id)}>Expand</button>
                </div>
            </div>
            {subtasks && subtasks.map(subtask => (
                <Task key={subtask.id} {...subtask} level={level+1} />
            ))}
        </>
    );
};

export default Task;
