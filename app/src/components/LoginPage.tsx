import React, { useState } from 'react';
import { LoginUser } from '../api/api'; // `api.ts` から LoginUser 関数をインポート
import { useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const token = await LoginUser({ username, password });
            localStorage.setItem('token', token); // トークンをローカルストレージに保存
            navigate('/dashboard'); // ログイン後のリダイレクト先
        } catch (err) {
            setError('ログインに失敗しました。ユーザー名またはパスワードを確認してください。');
        }
    };

    return (
        <div>
            <h2>ログイン</h2>
            <form onSubmit={handleLogin}>
                <div>
                    <label>ユーザー名:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>パスワード:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p>{error}</p>}
                <button type="submit">ログイン</button>
            </form>
        </div>
    );
};

export default LoginPage;
