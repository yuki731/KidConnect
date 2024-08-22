import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutPage: React.FC = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // ローカルストレージからトークンを削除
        localStorage.removeItem('token');

        // リダイレクトする
        navigate('/login');  // リダイレクト先のパスを指定
    }, [navigate]);

    return <div>Logging out...</div>;
};

export default LogoutPage;
