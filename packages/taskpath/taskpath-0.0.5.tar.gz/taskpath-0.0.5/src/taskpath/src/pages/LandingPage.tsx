import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
    return (
        <>
            <div id="hero">
                <div id="text-box">
                    <p>Turn your big ideas into actionable steps with TaskPath.</p>
                    <p><Link className="button" id="get-started" to="/sign-up">Get Started</Link></p>
                </div>
                <div id="image-box">
                    <img src="/taskpath-logo.webp"/>
                </div>
            </div>
        </>
    );
};

export default LandingPage;
