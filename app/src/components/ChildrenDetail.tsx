import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchChildPocketMoney } from '../api/api';

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${year}/${month}/${day} ${hours}:${minutes}`;
};

const ChildPocketMoneyComponent = () => {
    const { child_id } = useParams<{ child_id: string }>();
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    
    useEffect(() => {
        const getData = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                setError("トークンが見つかりません。");
                return;
            }

            if (child_id) {
                try {
                    const result = await fetchChildPocketMoney(parseInt(child_id), token);
                    setData(result);
                } catch (err) {
                    setError("データの取得に失敗しました。");
                }
            } else {
                setError("child_id が見つかりません。");
            }
        };

        getData();
    }, [child_id]);

    if (error) {
        return <p>{error}</p>;
    }

    if (!data) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h1>{data.child.username}のポケットマネー</h1>
            <p>合計金額: {data.total_amount}</p>

            {/* ポケットマネー履歴の表示 */}
            <h2>ポケットマネー履歴</h2>
            {data.pocket_money_records.length > 0 ? (
                <ul>
                    {data.pocket_money_records.map((record: any, index: number) => (
                        <li key={index}>
                            日付: {formatDateTime(record.date)}, 金額: {record.amount}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>ポケットマネー履歴がありません。</p>
            )}

            {/* ジョブカードの表示 */}
            <h2>ジョブカードのリスト</h2>
            {data.job_cards.length > 0 ? (
                <ul>
                    {data.job_cards.map((job: any, index: number) => (
                        <li key={index}>
                            仕事名: {job.job_name}, 金額: {job.money}円
                        </li>
                    ))}
                </ul>
            ) : (
                <p>ジョブカードがありません。</p>
            )}

            {/* ジョブレポートの表示 */}
            <h2>ジョブレポート</h2>
            {data.job_reports.length > 0 ? (
                <ul>
                    {data.job_reports.map((report: any, index: number) => (
                        <li key={index}>
                            レポート名: {report.job_name}, 金額: {report.money}, 日付: {formatDateTime(report.reported_at)}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>ジョブレポートがありません。</p>
            )}

            {/* 引き出しリクエストの表示 */}
            <h2>引き出しリクエスト</h2>
            {data.withdrawal_requests.length > 0 ? (
                <ul>
                    {data.withdrawal_requests.map((request: any, index: number) => (
                        <li key={index}>
                            タイトル: {request.title}, 金額: {request.money}円, リクエスト日: {formatDateTime(request.reported_at)}, ステータス: {request.status}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>引き出しリクエストがありません。</p>
            )}
          <div>
            <p><Link to={"/children_list"}>戻る</Link></p>
          </div>
        </div>

    );
};

export default ChildPocketMoneyComponent;
