import React, { useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { RequestWithdrawal } from '../api/api';  // API関数をインポート

const RequestWithdrawalPage: React.FC = () => {
  const [title, setTitle] = useState<string>('');
  const [money, setMoney] = useState<string>('');
  const token = localStorage.getItem('token') || '';
  const navigate = useNavigate();


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // FormDataを作成してAPI呼び出し
    const formData = new FormData();
    formData.append('title', title);
    formData.append('money', money.toString());

    try {
      const response = await RequestWithdrawal(token, formData);
      console.log('Aplication successful:', response);
      alert('出金申請に成功しました！');
      navigate('/parents_dashboard');
    } catch (error) {
      console.error('Error request:', error);
      alert('出金申請にに失敗しました。');
    }

  };
  return (
    <div>
      <h1>おこづかいの引き出し</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>引き出し理由:</label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>金額:</label>
          <input
            type="number"
            value={money}
            onChange={(e) => setMoney(e.target.value)}
          />
        </div>
        <button type="submit">引き出し申請</button>
      </form>
    </div>
  );
};

export default RequestWithdrawalPage;
