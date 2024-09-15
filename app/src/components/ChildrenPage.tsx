import React, { useEffect, useState } from 'react';
import { getUserDetails, getPocketMoney } from '../api/api';

interface User {
    username: string;
    family_name: string;
    first_name: string;
}

interface PocketMoneyResponse {
    total_amount: number;
}

const ChildrenPage: React.FC = () => {
    const [user, setUser] = useState<User | null>(null);
    const [pocketMoney, setPocketMoney] = useState<number | null>(null);

    useEffect(() => {
        const token = localStorage.getItem('token'); // ローカルストレージからトークンを取得
        if (token) {
            getUserDetails(token)
                .then(data => {
                    setUser(data);

                    // ユーザー情報取得後にポケットマネーを取得
                    return getPocketMoney(token);
                })
                .then((data: PocketMoneyResponse) => {
                    setPocketMoney(data.total_amount); // total_amountをセット
                })
                .catch(error => {
                    console.error('Failed to fetch data:', error);
                });
        }
    }, []);

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Welcome, {user.username}!</h1>
            <p>おこづかい : {pocketMoney !== null ? pocketMoney : 'Loading...'}</p>
            <p>Family Name: {user.family_name}</p>
            <p>First Name: {user.first_name}</p>
            <p><a href='/report-job'>仕事の報告</a></p>
            <p><a href='/request-withdrawal'>おこづかいの引き出し</a></p>
            <p><a href='/logout'>ログアウト</a></p>
        </div>
    );
};

export default ChildrenPage;
