import React, { useState } from 'react';
import { createUserAccount } from '../api/api';
import { useNavigate } from 'react-router-dom';

const CreateUserAccount: React.FC = () => {
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        password: '',
        role: 'child', // デフォルト値を 'child' に設定
    });
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        const token = localStorage.getItem('token'); // トークンをローカルストレージから取得
        if (!token) {
            setError('You must be logged in to create a user account.');
            return;
        }

        try {
            const data = await createUserAccount(token, formData);
            console.log('User account created:', data);
            navigate('/parents_dashboard'); // 成功後のリダイレクト先を指定
        } catch (err) {
            console.error('Failed to create user account:', err);
            setError('Failed to create user account. Please check the input.');
        }
    };

    return (
        <div>
            <h2>Create User Account</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>First Name:</label>
                    <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Role:</label>
                    <select name="role" value={formData.role} onChange={handleChange}>
                        <option value="parent">Parent</option>
                        <option value="child">Child</option>
                    </select>
                </div>
                <button type="submit">Create Account</button>
            </form>
        </div>
    );
};

export default CreateUserAccount;
