import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // useNavigate フックをインポート
import { signupUser } from '../api/api';

const SignupPage: React.FC = () => {
    const [familyName, setFamilyName] = useState('');
    const [firstName, setFirstName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const navigate = useNavigate(); // useNavigate フックを使用して navigate 関数を取得

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);
        setSuccess(null);

        try {
            await signupUser({
                family_name: familyName,
                first_name: firstName,
                username,
                password
            });
            setSuccess('User created successfully!');
            // サインアップ成功後にリダイレクト
            navigate('/login'); // 適切なリダイレクト先に変更してください
        } catch (error) {
            setError('Failed to create user. Please try again.');
        }
    };

    return (
        <div>
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="familyName">Family Name:</label>
                    <input
                        type="text"
                        id="familyName"
                        value={familyName}
                        onChange={(e) => setFamilyName(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="firstName">First Name:</label>
                    <input
                        type="text"
                        id="firstName"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Sign Up</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
        </div>
    );
};

export default SignupPage;
