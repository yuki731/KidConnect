import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getUserDetails } from '../api/api';

interface User {
    username: string;
    family_name: string;
    first_name: string;
}

const ParentsPage: React.FC = () => {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const token = localStorage.getItem('token'); // ローカルストレージからトークンを取得
        if (token) {
            getUserDetails(token)
                .then(data => {
                    setUser(data);
                })
                .catch(error => {
                    console.error('Failed to fetch user details:', error);
                });
        }
    }, []);

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Welcome, {user.username}!</h1>
            
            <p>Family Name: {user.family_name}</p>
            <p>First Name: {user.first_name}</p>
            <p><Link to={'/children_list'}>子供のアカウントを管理</Link></p>
            <p><Link to={'/create-user'}>ほかの家族アカウントを作成</Link></p>
            <p><Link to={'/create-job-card'}>お手伝いを作成</Link></p>
            <p><Link to={'/logout'}>ログアウト</Link></p>
        </div>
    );
};

export default ParentsPage;
