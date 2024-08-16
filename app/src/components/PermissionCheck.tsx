import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserDetails } from '../api/api'; // API関数をインポート

const PermissionCheck: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token'); // ローカルストレージからトークンを取得

    if (token) {
      getUserDetails(token)
        .then(data => {
          setUser(data);
        })
        .catch(error => {
          console.error('Failed to fetch user details:', error);
          setError('Failed to fetch user details');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
      setError('No token found');
    }
  }, []);

  useEffect(() => {
    if (!loading && user) {
      // デバッグ情報を出力して、user.groups の内容を確認
      console.log('User groups:', user.groups);

      const redirectTo = () => {
        if (Array.isArray(user.groups)) {
          if (user.groups.includes('Parents')) {
            return '/parents_dashboard';
          } else if (user.groups.includes('Children')) {
            return '/children_dashboard';
          }
        }
        return '/default-dashboard'; // 適切なデフォルトのリダイレクト先
      };

      // リダイレクト先の URL をデバッグ出力
      const redirectUrl = redirectTo();
      console.log('Redirecting to:', redirectUrl);
      navigate(redirectUrl);
    }
  }, [user, loading, navigate]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return null; // ここには何も表示しません
};

export default PermissionCheck;
