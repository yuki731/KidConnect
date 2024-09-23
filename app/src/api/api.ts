import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const signupUser = async (data: { family_name: string; first_name: string; username: string; password: string; }) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/signup/`, data);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail || 'Error during signup');
        } else {
            throw new Error('Unexpected error occurred');
        }
    }
};

export const LoginUser = async (data: { username: string; password: string }) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/signin/`, data);
        return response.data.token; // tokenを返す
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            throw error.response?.data || "Error during login";
        } else {
            throw new Error("Unexpected error occurred");
        }
    }
};

export const getUserDetails = async (token: string) => {
    try {
        console.log('Sending request with token:', token);
        const response = await axios.get(`${API_BASE_URL}/user/`, {
            headers: {
                Authorization: `Token ${token}`,
            },
        });
        console.log('Response data:', response.data);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error('Error response:', error.response);
            console.error('Error message:', error.message);
            console.error('Error config:', error.config);
        } else {
            console.error('Unexpected error:', error);
        }
        throw error;
    }
};

export const createUserAccount = async (token: string, userData: any) => {
    const response = await axios.post(`${API_BASE_URL}create-user/`, userData, {
        headers: {
            Authorization: `Token ${token}`,
        },
    });
    return response.data;
};

export interface PocketMoneyResponse {
    total_amount: number;
}

export const getPocketMoney = async (token: string): Promise<PocketMoneyResponse> => {
    const response = await fetch(`${API_BASE_URL}/child-dashboard/`, {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch pocket money data');
    }
    return response.json();
};

export const createJobCard = async (token: string, formData: FormData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/create-job-card/`, {  // 正しいエンドポイント
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating job card:', error);  // エラーの詳細を出力
    throw error;  // 呼び出し元にエラーを渡す
  }
};


export const fetchChildren = async (token: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/family/children/`, {  // エンドポイントを確認
      method: 'GET',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching children:', error);  // エラーの詳細を出力
    throw error;  // 呼び出し元にエラーを渡す
  }
};

export const taskList = async (token: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/task-view/`, {  // エンドポイントを確認
      method: 'GET',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching children:', error);  // エラーの詳細を出力
    throw error;  // 呼び出し元にエラーを渡す
  }
};

export const reportJob = async (token: string, jobID: number) => {
  const response = await axios.post(
      `${API_BASE_URL}/report-job/${jobID}/`, 
      {},
      {
          headers: {
              Authorization: `Token ${token}`,
      },
  });
  return response.data;
};

export const RequestWithdrawal = async (token: string, formData: FormData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/create-withdrawal-request/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating withdrawal:', error);  // エラーの詳細を出力
    throw error;  // 呼び出し元にエラーを渡す
  }
};

export const fetchChildrenInFamily = async (token: string) => {
  try {
      const response = await axios.get(`${API_BASE_URL}/family/children/`, {
          headers: {
              'Authorization': `Token ${token}`  // 認証トークンをヘッダーに追加
          }
      });
      return response.data;  // 子供の情報を返す
  } catch (error) {
      console.error('Error fetching children in family:', error);
      throw error;
  }
};