import React, { useEffect, useState } from 'react';
import { taskList, reportJob } from '../api/api';

// DjangoサーバーのベースURLを定義
const BASE_URL = 'http://127.0.0.1:8000'; // DjangoサーバーのURLに変更してください

interface Job {
    id: number;
    job_name: string;
    money: number;
    job_image: string;  // 画像パス
}

const ReportJobPage: React.FC = () => {
    const [jobs, setJobs] = useState<Job[]>([]);
    const AuthToken = localStorage.getItem('token') || '';
    const [token, setToken] = useState<string>(AuthToken);

    useEffect(() => {
        const fetchJobList = async () => {
            try {
                const data = await taskList(token);
                if (data && Array.isArray(data.job_cards)) {
                    setJobs(data.job_cards);
                } else {
                    console.error('データ形式が正しくありません:', data);
                    setJobs([]);
                }
            } catch (error) {
                console.error('Error getting job card:', error);
                setJobs([]);
            }
        };

        fetchJobList();
    }, [token]);

    const handleReportJob = async (job_id: number) => {
        try {
            await reportJob(token, job_id);
            alert('報告しました');
        } catch (error) {
            alert('報告に失敗しました');
        }
    };

    return (
        <div>
            <h1>おてつだいのほうこく</h1>
            <p><a href='/children_dashboard'>ホームに戻る</a></p>
            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                {jobs.map(job => (
                    <div key={job.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '16px', margin: '8px', width: '300px' }}>
                        <h2>{job.job_name}</h2>
                        <p>報酬: {job.money} 円</p>
                        <div>
                            <img
                                src={`${BASE_URL}${job.job_image}`}  // ベースURLと相対パスを結合
                                alt={job.job_name}
                                style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
                                onError={(e) => { e.currentTarget.src = '/default-image.png'; }} // デフォルト画像を設定
                            />
                        </div>
                        <button onClick={() => handleReportJob(job.id)}>報告</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ReportJobPage;
