import axios from 'axios';

export const signupUser = async (data: { family_name: string; first_name: string; username: string; password: string; }) => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/signup/', data);
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
        const response = await axios.post('http://127.0.0.1:8000/api/signin/', data);
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
        const response = await axios.get('http://127.0.0.1:8000/api/user/', {
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
